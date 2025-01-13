import pygame
import json
import time
import decimal
import random
import FPS

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
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()
    width, height = pygame.display.get_window_size()

    keybinds = [["a", 'LEFT'], ["s", 'DOWN'], ["w", 'UP'], ["d", 'RIGHT']]

    stupidPath = 'assets/image/noteSkin/'
    noteAssets = [
        [pygame.image.load(f'{stupidPath}arrow.png'), 0],
        [pygame.image.load(f'{stupidPath}arrow.png'), 90],
        [pygame.image.load(f'{stupidPath}arrow.png'), -90],
        [pygame.image.load(f'{stupidPath}arrow.png'), 180],
        [pygame.image.load(f'{stupidPath}arrow.png')],
        [pygame.image.load(f'{stupidPath}arrow.png')],
        [pygame.image.load(f'{stupidPath}arrow.png')],
        [pygame.image.load(f'{stupidPath}arrow.png')]
    ]
    noteDirs = ['Left', 'Down', 'Up', 'Right']
    for i in range(len(noteAssets)):
        nData = i
        if nData < 4:
            dirlol = nData
        else:
            dirlol = nData-4
        noteAssets[i][0] = pygame.transform.scale(noteAssets[i][0], (112, 112))
        noteAssets[i][0] = pygame.transform.rotate(noteAssets[i][0], noteAssets[dirlol][1])

    # Json LOL
    song = f"assets/songs/{jsonFile}/Inst.ogg"
    voices = f"assets/songs/{jsonFile}/Voices.ogg"
    jsonFile = f"assets/data/{jsonFile}/{jsonFile.lower()}"
    jsonFile = open(f"{jsonFile}.json", "r")
    jsonFile = jsonFile.read()
    jsonFile = json.loads(jsonFile)
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
                    v = decimal.Decimal(v)
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

    # Default JSON Values and Text
    scrollSpeed = jsonFile['song']['speed']
    scoreTxt = pygame.font.Font("assets/fonts/vcr.ttf", 24)

    # Music
    pygame.mixer.music.load(song)
    try:
        lmao = pygame.mixer.Sound(voices)
        pygame.mixer.Sound.play(lmao)
    except:
        print(f'SOUND NOT FOUND: {voices}')
    pygame.mixer.music.play()

    # Playstate
    score = 0
    combo = 0
    playerNoteRem = 0
    accuracyOld = 0
    accuracyNew = "???"

    # Game Funnies
    zoomForce = 0
    curSection = 0
    bpm = jsonFile['song']['bpm']

    # Saves Only
    save = open('assets/saves/save.txt', 'r')
    save = save.read()
    save = save.splitlines()

    try:
        cpuControlled = True if save[0] == "1" else False
    except:
        cpuControlled = False

    noteLoaded = 0
    spawnedNotes = []
    noMoreSpawn = False
    songTime = -time.time()
    ratingSpawn = []
    while True:
        screen.fill((0, 0, 0))
        timeNow = (songTime+time.time())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                for i in range(len(keybinds)):
                    for j in range(len(keybinds[i])):
                        if event.key == getattr(pygame, f"K_{keybinds[i][j]}") and not cpuControlled:
                            thingyMaBob = checkForKey(i, spawnedNotes, timeNow)
                            if thingyMaBob[0]:
                                spawnedNotes.pop(thingyMaBob[1])
                                lolW = ['sick', 'good', 'bad', 'shit']
                                whatSpawn = 0
                                m = abs(thingyMaBob[2]+22.5)
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
                                    [random.randint(-50, 50), -random.randint(300, 400), random.randint(100, 150)],
                                    255,
                                    len(comboStr),
                                    []
                                ])
                                length = len(ratingSpawn)-1
                                for i in range(len(comboStr)):
                                    ratingSpawn[length][5].append([
                                        pygame.image.load(f'assets/image/num{comboStr[i]}.png'),
                                        [500+(60*i), 540],
                                        [random.randint(-50, 50), -random.randint(300, 400), random.randint(100, 150)],
                                        255
                                    ])
                                    ratingSpawn[length][5][i][0] = pygame.transform.scale(ratingSpawn[length][5][i][0], (55, 70))
                            else:
                                combo = 0
                                playerNoteRem += 1
                                accuracyNew = recalcAcc(accuracyOld, playerNoteRem)
                                playSound(f'missnote{random.randint(1, 3)}')

        if cpuControlled:
            for i in range(4):
                thingyMaBob = checkForKey(i, spawnedNotes, timeNow)
                if thingyMaBob[0] and thingyMaBob[2] < 22.5:
                    spawnedNotes.pop(thingyMaBob[1])
                    lolW = ['sick', 'good', 'bad', 'shit']
                    whatSpawn = 0
                    m = abs(thingyMaBob[2]+22.5)
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
                        [random.randint(-50, 50), -random.randint(300, 400), random.randint(100, 150)],
                        255,
                        len(comboStr),
                        []
                    ])
                    length = len(ratingSpawn)-1
                    for i in range(len(comboStr)):
                        ratingSpawn[length][5].append([
                            pygame.image.load(f'assets/image/num{comboStr[i]}.png'),
                            [500+(60*i), 540],
                            [random.randint(-50, 50), -random.randint(300, 400), random.randint(100, 150)],
                            255
                        ])
                        ratingSpawn[length][5][i][0] = pygame.transform.scale(ratingSpawn[length][5][i][0], (55, 70))

        while timeNow+3 > notes[noteLoaded][0] and not noMoreSpawn:
            noteDir = notes[noteLoaded][1]-4 if notes[noteLoaded][1] > 3 else notes[noteLoaded][1]
            spawnedNotes.append([
                pygame.image.load(f'{stupidPath}/note{noteDirs[noteDir]}.png'),
                notes[noteLoaded][0],
                notes[noteLoaded][1]
            ])
            noteLoaded += 1
            spawnedNotes[len(spawnedNotes)-1][0] = pygame.transform.scale(spawnedNotes[len(spawnedNotes)-1][0], (112, 112))
            if noteLoaded+1 == len(notes):
                noMoreSpawn = True

        noteLoad = -1
        for i in range(len(ratingSpawn)):
            if i > 3:
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

        for i in range(len(noteAssets)):
            if i < 4:
                screen.blit(noteAssets[i][0], ((i*112)+92, 50))
            else:
                screen.blit(noteAssets[i][0], ((i*112)+240, 50))

        noteLoad = -1
        for i in range(len(spawnedNotes)):
            noteLoad += 1
            try:
                y = (((spawnedNotes[noteLoad][1]*750)-(timeNow*750))+50)*(scrollSpeed/2)
                if y < 832:
                    if spawnedNotes[noteLoad][2] < 4:
                        x = (spawnedNotes[noteLoad][2]*112)+92
                        screen.blit(spawnedNotes[noteLoad][0], (x, y))
                    else:
                        x = (spawnedNotes[noteLoad][2]*112)+240
                        screen.blit(spawnedNotes[noteLoad][0], (x, y))
                    if y < -112:
                        spawnedNotes.pop(noteLoad)
                        noteLoad -= 1
                        combo = 0
                        playerNoteRem += 1
                        accuracyNew = recalcAcc(accuracyOld, playerNoteRem)
                        playSound(f'missnote{random.randint(1, 3)}')
                    elif y < 50 and spawnedNotes[noteLoad][2] < 4:
                        spawnedNotes.pop(noteLoad)
                        noteLoad -= 1
            except:
                noteLoad -= 1

        if timeNow > (240/bpm)*curSection:
            curSection += 1
            zoomForce = 90

        stxt = f'Score: {score} | Accuracy: {accuracyNew}' if not cpuControlled else 'BOT'
        sset = scoreTxt.render(stxt, True, (255, 255, 255))
        screen.blit(sset, ((width/2)-((len(stxt)*12)/2),600))

        if not pygame.mixer.music.get_busy():
            import Freeplay
            Freeplay.main()
            return 0
        
        zoomed_screen = pygame.transform.smoothscale(screen, (1280+zoomForce, 720+(zoomForce/1.5)))
        screen.blit(zoomed_screen, (-(zoomForce/2), -(zoomForce/3.33)))
        zoomForce = (zoomForce/1.075)

        FPS.tick()
        pygame.display.flip()
        clock.tick(60)