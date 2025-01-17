import pygame
import source.Freeplay as Freeplay
from source.Debugger import trace, tick, getHSContents
import xml.etree.ElementTree as ET
from json import loads
from time import time
from decimal import Decimal
from random import randint
from os.path import exists as checkFileExists

# The TextureAtlas xml was infact AI generated since there was NO ONE that have make this before

nspath = 'assets/image/noteSkin/'
texture = pygame.image.load(f"{nspath}NOTE_assets.png")
tree = ET.parse(f"{nspath}NOTE_assets.xml")
root = tree.getroot()
subtextures = {}

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
width, height = pygame.display.get_window_size()

for subtexture in root.findall(".//SubTexture"):
    name = subtexture.get("name")
    x = int(subtexture.get("x"))
    y = int(subtexture.get("y"))
    width = int(subtexture.get("width"))
    height = int(subtexture.get("height"))
    subtextures[name] = pygame.Rect(x, y, width, height)

class NSTextureAtlas:
    def __init__(self, x, y, animation_name):
        self.x = x
        self.y = y
        self.animation_name = animation_name
        self.size = (112, 112)
        self.frame_names = [name for name in subtextures if name.startswith(animation_name)]
        
        if not self.frame_names:
            self.frame_names = [f"{animation_name} 0000"] if f"{animation_name} 0000" in subtextures else []
        
        self.current_frame = 0
        self.last_frame_time = time()
        self.update()


    def update(self, frame_delay=1/24):
        current_frame_name = self.frame_names[self.current_frame]
        if "confirm" in current_frame_name:
            self.size = (150, 150)
        else:
            self.size = (112, 112)

        if time() - self.last_frame_time >= frame_delay:
            if self.frame_names:
                self.current_frame = (self.current_frame + 1) % len(self.frame_names)
                self.last_frame_time = time()


    def draw(self):
        if self.frame_names:
            subtexture_name = self.frame_names[self.current_frame]
            if subtexture_name in subtextures:
                subrect = subtextures[subtexture_name]
                subtexture = texture.subsurface(subrect)
                scaled_subtexture = pygame.transform.scale(subtexture, self.size)
                adjusted_x = self.x + 2 if "confirm" in subtexture_name else self.x
                scaled_rect = scaled_subtexture.get_rect(center=(adjusted_x, self.y))
                screen.blit(scaled_subtexture, scaled_rect.topleft)

def checkForKey(key, notes, time):
    for i in range(len(notes)):
        if notes[i][2]-4 == key:
            ms = (notes[i][1]-time)*1000
            if abs(ms) < 180:
                return [True, i, ms]
    return [False]

def recalcAcc(acc, hit):
    return "{:.2f}".format(round((acc/hit), 5)) + "%"

def playSound(sound):
    lmao = pygame.mixer.Sound(f"assets/sounds/{sound}.ogg")
    pygame.mixer.Sound.play(lmao)
    
def play(jsonFile):
    noteFrame = ["", "", "", "", "", "", "", ""]
    noteDirs = ['Left', 'Down', 'Up', 'Right']
    noteCols = ['purple', 'blue', 'green', 'red']
    noteBTN = [0, 0, 0, 0]

    for i in range(8):
        noteFrame[i] = NSTextureAtlas(x=112*(i+1)+(0 if i < 4 else 147)+35, y=100, animation_name=f"arrow{noteDirs[i if i < 4 else i-4].upper()}")

    # Json LOL
    songName = jsonFile
    jsonFile = jsonFile.lower().replace(' ', '-')
    song = f"assets/songs/{jsonFile}/Inst.ogg"
    voices = f"assets/songs/{jsonFile}/Voices.ogg"
    jsonFile = f"assets/data/{jsonFile}/{jsonFile.lower()}"
    jsonFile = open(f"{jsonFile}.json", "r")
    jsonFile = jsonFile.read()
    jsonFile = loads(jsonFile)
    loaded = []
    notes = []
    for i in range(len(jsonFile['song']['notes'])):
        loaded.append([jsonFile['song']['notes'][i]['mustHitSection'], []])
        for j in range(len(jsonFile['song']['notes'][i]['sectionNotes'])):
            add = []
            for k in range(3):
                v = float(jsonFile['song']['notes'][i]['sectionNotes'][j][k])
                if k == 0 or k == 2:
                    if k == 0:
                        v = v/1000
                    v = Decimal(v)
                    dec = abs(v.as_tuple().exponent)
                    if dec > 5:
                        v = "{:.5f}".format(round(v, 5))
                    v = float(v)
                elif k == 1:
                    noteData = int(v)
                    if loaded[i][0]:
                        noteData += 4
                    if noteData > 7:
                        noteData -= 8
                    v = int(noteData)
                add.append(v)
            notes.append(add)
    notes.append([0, 1, 0])
    trace(f"{len(notes)} notes and {len(jsonFile['song']['notes'])} sections loaded.")

    # Default JSON Values and Text
    scrollSpeed = jsonFile['song']['speed']
    scoreTxt = pygame.font.Font("assets/fonts/vcr.ttf", 24)

    # Playstate
    score = 0
    combo = 0
    playerNoteRem = 0
    accuracyOld = 0
    accuracyNew = "???"
    keybinds = [["q", 's'], ["d", 'f'], ["j", 'k'], ["l", 'm']]

    # Game Funnies
    zoomForce = 0
    curSection = 1
    bpm = jsonFile['song']['bpm']

    # Saves Only
    try:
        save = open('assets/saves/save.txt', 'r')
        save = save.read()
        save = save.splitlines()
        cpuControlled = True if save[0] == "1" else False
        ghostTap = True if save[1] == "1" else False
        missSfx = True if save[2] == "1" else False
    except:
        if not checkFileExists('assets/saves/save.txt'): trace('SAVE FILE NOT FOUND: assets/saves/save.txt')
        else: trace('SAVE FILE NOT UPDATED TO NEW OPTIONS VERSION.')
        cpuControlled = False
        ghostTap = False
        missSfx = True

    # Music
    pygame.mixer.music.load(song)
    try:
        lmao = pygame.mixer.Sound(voices)
        pygame.mixer.Sound.play(lmao)
    except:
        trace(f'SOUND NOT FOUND: {voices}')
    pygame.mixer.music.play()

    noteLoaded = 0
    spawnedNotes = []
    noMoreSpawn = False
    songTime = -time()
    ratingSpawn = []
    
    while 1:
        screen.fill((0, 0, 0))
        timeNow = (songTime+time())
        while timeNow > (240/bpm)*curSection:
            curSection += 1
            zoomForce += 50

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                for i in range(len(keybinds)):
                    for j in range(len(keybinds[i])):
                        if event.key == getattr(pygame, f"K_{keybinds[i][j]}") and not cpuControlled:
                            thingyMaBob = checkForKey(i, spawnedNotes, timeNow)
                            if thingyMaBob[0]:
                                noteFrame[i+4] = NSTextureAtlas(x=112*(i+5)+182, y=100, animation_name=f"{noteDirs[i].lower()} confirm")
                                noteBTN[i] = timeNow+((1/24)*4)
                                spawnedNotes.pop(thingyMaBob[1])
                                lolW = ['sick', 'good', 'bad', 'shit']
                                whatSpawn = 0
                                m = abs(thingyMaBob[2])
                                combo += 1
                                playerNoteRem += 1 
                                if m < 45:
                                    score += 25
                                    accuracyOld += 100
                                elif m < 90:
                                    score += 10
                                    whatSpawn = 1
                                    accuracyOld += 75
                                elif m < 135:
                                    score += 5
                                    whatSpawn = 2
                                    accuracyOld += 50
                                else:
                                    score += 1
                                    whatSpawn = 3
                                    accuracyOld += 25
                                accuracyNew = recalcAcc(accuracyOld, playerNoteRem)
                                comboStr = str(combo)
                                ratingSpawn.append([
                                    pygame.image.load(f'assets/image/{lolW[whatSpawn]}.png'),
                                    [520, 400],
                                    [randint(-50, 50), -randint(300, 400), randint(100, 150)],
                                    255,
                                    len(comboStr),
                                    []
                                ])
                                length = len(ratingSpawn)-1
                                for i in range(len(comboStr)):
                                    ratingSpawn[length][5].append([
                                        pygame.image.load(f'assets/image/num{comboStr[i]}.png'),
                                        [500+(60*i), 540],
                                        [randint(-50, 50), -randint(300, 400), randint(100, 150)],
                                        255
                                    ])
                                    ratingSpawn[length][5][i][0] = pygame.transform.scale(ratingSpawn[length][5][i][0], (55, 70))
                            elif not ghostTap:
                                combo = 0
                                playerNoteRem += 1
                                accuracyNew = recalcAcc(accuracyOld, playerNoteRem)
                                playSound(f'missnote{randint(1, 3)}')

        if cpuControlled:
            for i in range(4):
                thingyMaBob = checkForKey(i, spawnedNotes, timeNow)
                if thingyMaBob[0] and thingyMaBob[2] < 0:
                    spawnedNotes.pop(thingyMaBob[1])
                    noteFrame[i+4] = NSTextureAtlas(x=112*(i+5)+182, y=100, animation_name=f"{noteDirs[i].lower()} confirm")
                    noteBTN[i] = timeNow+((1/24)*4)
                    lolW = ['sick', 'good', 'bad', 'shit']
                    whatSpawn = 0
                    m = abs(thingyMaBob[2])
                    combo += 1
                    playerNoteRem += 1 
                    if m < 45:
                        score += 25
                        accuracyOld += 100
                    elif m < 90:
                        score += 10
                        whatSpawn = 1
                        accuracyOld += 75
                    elif m < 135:
                        score += 5
                        whatSpawn = 2
                        accuracyOld += 50
                    else:
                        score += 1
                        whatSpawn = 3
                        accuracyOld += 25
                    accuracyNew = recalcAcc(accuracyOld, playerNoteRem)
                    comboStr = str(combo)
                    ratingSpawn.append([
                        pygame.image.load(f'assets/image/{lolW[whatSpawn]}.png'),
                        [520, 400],
                        [randint(-50, 50), -randint(300, 400), randint(100, 150)],
                        255,
                        len(comboStr),
                        []
                    ])
                    length = len(ratingSpawn)-1
                    for i in range(len(comboStr)):
                        ratingSpawn[length][5].append([
                            pygame.image.load(f'assets/image/num{comboStr[i]}.png'),
                            [500+(60*i), 540],
                            [randint(-50, 50), -randint(300, 400), randint(100, 150)],
                            255
                        ])
                        ratingSpawn[length][5][i][0] = pygame.transform.scale(ratingSpawn[length][5][i][0], (55, 70))

        while timeNow+3 > notes[noteLoaded][0] and not noMoreSpawn:
            spawnedNotes.append([
                "",
                notes[noteLoaded][0],
                notes[noteLoaded][1]
            ])
            noteLoaded += 1
            if noteLoaded+1 == len(notes):
                noMoreSpawn = True

        noteLoad = -1
        for i in range(len(ratingSpawn)):
            if i > 4:
                ratingSpawn.pop(0)
            else:
                noteLoad += 1
                try:
                    for j in range(2):
                        ratingSpawn[noteLoad][1][j] += ratingSpawn[noteLoad][2][j]/100
                    ratingSpawn[noteLoad][2][1] += ratingSpawn[noteLoad][2][2]/10
                    ratingSpawn[noteLoad][0].fill((255, 255, 255, ratingSpawn[noteLoad][3]), None, pygame.BLEND_RGBA_MULT)
                    ratingSpawn[noteLoad][3] -= 0.25
                    screen.blit(ratingSpawn[noteLoad][0], (ratingSpawn[noteLoad][1][0], ratingSpawn[noteLoad][1][1]))
                    ratingNum = ratingSpawn[noteLoad][4]
                    for k in range(ratingNum):
                        for j in range(2):
                            ratingSpawn[noteLoad][5][k][1][j] += ratingSpawn[noteLoad][5][k][2][j]/100
                        ratingSpawn[noteLoad][5][k][2][1] += ratingSpawn[noteLoad][5][k][2][2]/10
                        ratingSpawn[noteLoad][5][k][0].fill((255, 255, 255, ratingSpawn[noteLoad][5][k][3]), None, pygame.BLEND_RGBA_MULT)
                        ratingSpawn[noteLoad][5][k][3] -= 0.25
                        screen.blit(ratingSpawn[noteLoad][5][k][0], (ratingSpawn[noteLoad][5][k][1][0], ratingSpawn[noteLoad][5][k][1][1]))
                    if ratingSpawn[noteLoad][3] == 0:
                        ratingSpawn.pop(noteLoad)
                        noteLoad -= 1
                except:
                    noteLoad -= 1

        for i in range(len(noteFrame)):
            noteFrame[i].update()
            noteFrame[i].draw()
            if i < 4:
                if noteBTN[i-4] < timeNow and noteBTN[i-4] != 0:
                    noteFrame[i-4] = NSTextureAtlas(x=112*(i+5)+182, y=100, animation_name=f"arrow{noteDirs[i-4].upper()}")
                    noteBTN[i-4] = 0

        noteLoad = -1
        for i in range(len(spawnedNotes)):
            noteLoad += 1
            try:
                y = (((spawnedNotes[noteLoad][1]*750)-(timeNow*750))+50)*(scrollSpeed/2)-50
                if y < 832:
                    x = (spawnedNotes[noteLoad][2]*112)+(92 if spawnedNotes[noteLoad][2] < 4 else 240)
                    nd = spawnedNotes[noteLoad][2]
                    spawnedNotes[noteLoad][0] = NSTextureAtlas(x=x+55, y=y+50, animation_name=f"{noteCols[nd if nd < 4 else nd-4]}0")
                    spawnedNotes[noteLoad][0].update()
                    spawnedNotes[noteLoad][0].draw()
                    if y < -112:
                        spawnedNotes.pop(noteLoad)
                        noteLoad -= 1
                        combo = 0
                        score -= 2
                        playerNoteRem += 1
                        accuracyNew = recalcAcc(accuracyOld, playerNoteRem)
                        if missSfx: playSound(f'missnote{randint(1, 3)}')
                    elif y < 50 and spawnedNotes[noteLoad][2] < 4:
                        spawnedNotes.pop(noteLoad)
                        noteLoad -= 1
            except:
                noteLoad -= 1

        if not pygame.mixer.music.get_busy():
            checks = getHSContents()
            highScores = []
            saveFile = ""
            exists, where = False, 0
            for i, table in enumerate(checks):
                for key, value in table:
                    highScores.append([key, value])
                    if highScores[len(highScores)-1][0] == songName: exists, where = True, len(highScores)-1
            if not cpuControlled:
                if not exists:
                    highScores.append([songName, score])
                elif score > int(highScores[where][1]):
                    highScores[where][1] = score
            for i in range(len(highScores)):
                saveFile += f"{highScores[i][0]}:{highScores[i][1]}\n"
            new = open('assets/saves/highscore.txt', 'w')
            new.write(saveFile)
            new.close()
            Freeplay.main()
            break

        stxt = f'Score: {score} | Accuracy: {accuracyNew}' if not cpuControlled else 'BOT'
        sset = scoreTxt.render(stxt, True, (255, 255, 255))
        screen.blit(sset, ((width/2)-((len(stxt)*12)/2)+600,600))
        
        zoomed_screen = pygame.transform.smoothscale(screen, (1280+zoomForce, 720+(zoomForce/1.5)))
        screen.blit(zoomed_screen, (-zoomForce/2, -zoomForce/3.33))
        zoomForce = (zoomForce/1.08)
        tick()
        pygame.display.flip()
        clock.tick(60)