import pygame
import ctypes
import glob
import json
import os.path
import FPS
import time

def popup(title, text, style=0):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def playSound(sound):
    lmao = pygame.mixer.Sound(f"assets/sounds/{sound}.ogg")
    pygame.mixer.Sound.play(lmao)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()
    menuBG = pygame.image.load('assets/image/menuBG.png')

    jsons = glob.glob("assets/weeks/*.json")
    freeplayText = []
    for i in range(len(jsons)):
        read = open(jsons[i])
        read = read.read()
        read = json.loads(read)
        for j in range(len(read['songs'])):
            iconName = "face"
            if os.path.exists(f"assets/image/icons/icon-{read['songs'][j][1]}.png"):
                iconName = read['songs'][j][1]
            freeplayText.append([read['songs'][j][0], pygame.font.Font("assets/fonts/vcr.ttf", 90), pygame.image.load(f'assets/image/icons/icon-{iconName}.png')])

    chosenSong = 0
    insideSong = False
    currentPlaying = ""
    bpm = 0
    curBeat = 0
    beatPower = 0
    freeplay = True
    curSec = -time.time()
    while freeplay:
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                s = freeplayText[abs(chosenSong)][0]
                if event.key == pygame.K_UP:
                    playSound("scrollMenu")
                    chosenSong += 1
                    if chosenSong == 1:
                        chosenSong = -len(freeplayText)+1
                if event.key == pygame.K_DOWN:
                    playSound("scrollMenu")
                    chosenSong -= 1
                    if chosenSong == -len(freeplayText):
                        chosenSong = 0
                if event.key == pygame.K_RETURN:
                    insideSong = True
                    pygame.mixer.music.stop()
                    import Play
                    Play.play(freeplayText[abs(chosenSong)][0])
                    return 0
                if event.key == pygame.K_SPACE and currentPlaying != freeplayText[abs(chosenSong)][0]:
                    currentPlaying = freeplayText[abs(chosenSong)][0]
                    jsonBabyCry = open(f"assets/data/{s}/{s.lower()}.json", 'r')
                    jsonBabyCry = jsonBabyCry.read()
                    jsonBabyCry = json.loads(jsonBabyCry)
                    bpm = jsonBabyCry['song']['bpm']
                    curBeat = 1
                    pygame.mixer.music.stop() 
                    pygame.mixer.music.load(f"assets/songs/{s}/Inst.ogg")
                    pygame.mixer.music.play()
                    print(bpm)
                if event.key == pygame.K_BACKSPACE:
                    import Main
                    return 0
                
        if currentPlaying != "":
            timeNow = curSec+time.time()
            if timeNow > (60/bpm)*curBeat:
                curBeat += 1
                beatPower = 35

        if not insideSong:
            screen.blit(menuBG, (0, 0))
            beatPower = beatPower/1.2
            for i in range(len(freeplayText)):
                hahaFunny = freeplayText[i][1].render(freeplayText[i][0], True, (255, 255, 255) if -i == chosenSong else (50, 50, 50))
                screen.blit(hahaFunny, (200+(25*(i+chosenSong)), 280+(100*(i+chosenSong))))
                screen.blit(freeplayText[i][2], (50+(25*(i+chosenSong)), 275+(100*(i+chosenSong))), (0, 0, 150, 150))

        if not pygame.mixer.music.get_busy():
            currentPlaying = ""
            pygame.mixer.music.load("assets/music/freakyMenu.ogg")
            pygame.mixer.music.play()

        FPS.tick()
        pygame.display.flip()
        clock.tick(60)

main()