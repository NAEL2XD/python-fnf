import pygame
from glob import glob
from json import loads
from os.path import exists
from time import time
from Debugger import trace, tick, getHSContents

class Icons:
    def __init__(self, image):
        self.ogImg = image

    def scale(self, scale_factor):
        ogWidth, ogHeight = self.ogImg.get_size()
        newW = int(ogWidth * scale_factor)
        newH = int(ogHeight * scale_factor)
        return pygame.transform.smoothscale(self.ogImg, (newW, newH))

def playSound(sound):
    lmao = pygame.mixer.Sound(f"assets/sounds/{sound}.ogg")
    pygame.mixer.Sound.play(lmao)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()
    menuBG = pygame.image.load('assets/image/menuBG.png')

    personal = pygame.font.Font('assets/fonts/vcr.ttf', 30)
    checks = getHSContents()
    highScores = []
    for i, table in enumerate(checks):
        for key, value in table:
            highScores.append([key, value])
    new = True

    jsons = glob("assets/weeks/*.json")
    freeplayText = []
    for i in range(len(jsons)):
        read = open(jsons[i])
        read = read.read()
        read = loads(read)
        for j in range(len(read['songs'])):
            iconName = "face"
            if exists(f"assets/image/icons/icon-{read['songs'][j][1]}.png"):
                iconName = read['songs'][j][1]
            sad = pygame.image.load(f'assets/image/icons/icon-{iconName}.png')
            freeplayText.append([
                read['songs'][j][0],
                pygame.font.Font("assets/fonts/vcr.ttf", 90),
                Icons(sad),
                sad
            ])

    chosenSong = 0
    insideSong = False
    currentPlaying = ""
    bpm = 0
    curBeat = 0
    beatPower = 0
    beatIcon = 0
    freeplay = True
    curSec = -time()
    while freeplay:
        def refreshHS():
            for i in range(len(highScores)):
                if highScores[i][0] == freeplayText[abs(chosenSong)][0]:
                    return highScores[i][1] if highScores[i][1] != None else 0
                
        if new:
            curPB = refreshHS()
            new = False

        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                s = freeplayText[abs(chosenSong)][0].lower().replace(' ', '-')
                r = False
                if event.key == pygame.K_UP:
                    playSound("scrollMenu")
                    chosenSong += 1
                    if chosenSong == 1:
                        chosenSong = -len(freeplayText)+1
                    r = True
                if event.key == pygame.K_DOWN:
                    playSound("scrollMenu")
                    chosenSong -= 1
                    if chosenSong == -len(freeplayText):
                        chosenSong = 0
                    r = True
                if r:
                    curPB = refreshHS()

                if event.key == pygame.K_RETURN:
                    insideSong = True
                    pygame.mixer.music.stop()
                    import Play
                    Play.play(freeplayText[abs(chosenSong)][0])
                    return 0
                if event.key == pygame.K_SPACE and currentPlaying != freeplayText[abs(chosenSong)][0]:
                    currentPlaying = freeplayText[abs(chosenSong)][0]
                    beatIcon = chosenSong
                    jsonBabyCry = open(f"assets/data/{s}/{s}.json", 'r')
                    jsonBabyCry = jsonBabyCry.read()
                    jsonBabyCry = loads(jsonBabyCry)
                    bpm = jsonBabyCry['song']['bpm']
                    curBeat = 1
                    pygame.mixer.music.stop() 
                    pygame.mixer.music.load(f"assets/songs/{s}/Inst.ogg")
                    pygame.mixer.music.play()
                    trace(bpm)
                if event.key == pygame.K_BACKSPACE:
                    import Main
                    return 0
                
        if currentPlaying != "":
            timeNow = curSec+time()
            while timeNow > (60/bpm)*curBeat:
                curBeat += 1
                beatPower = 0.25
        else: beatPower = 0

        if not insideSong:
            screen.blit(menuBG, (0, 0))
            for i in range(len(freeplayText)):
                x, y, s = 50+(25*(i+chosenSong)), 275+(100*(i+chosenSong)), 150
                if -i == beatIcon:
                    hi = freeplayText[i][2].scale(1+beatPower)
                    x -= beatPower*40
                    y -= beatPower*40
                hahaFunny = freeplayText[i][1].render(freeplayText[i][0], True, (255, 255, 255) if -i == chosenSong else (50, 50, 50))
                screen.blit(hahaFunny, (200+(25*(i+chosenSong)), 280+(100*(i+chosenSong))))
                screen.blit(freeplayText[i][3] if -i != beatIcon else hi, (x, y), (0, 0, s, s))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(880, 0, 400, 50))
            gay = personal.render(f'PERSONAL BEST: {curPB}', True, (255, 255, 255))
            screen.blit(gay, (890, 10))

        beatPower = beatPower/1.25

        if not pygame.mixer.music.get_busy():
            currentPlaying = ""
            pygame.mixer.music.load("assets/music/freakyMenu.ogg")
            pygame.mixer.music.play()

        tick()
        pygame.display.flip()
        clock.tick(60)