import pygame
import FPS
from os.path import exists as checkFileExists
from os import remove as deleteFile
import time
from Debugger import debugPrint

def playSound(sound):
    lmao = pygame.mixer.Sound(f"assets/sounds/{sound}.ogg")
    pygame.mixer.Sound.play(lmao)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()

    coolOptions = [
        [
            "Bot Mode",
            "BOOL",
            "Cheat if you want, i don't care tho.",
            False
        ],
        [
            "Ghost Tapping",
            "BOOL",
            "If you wanna press without getting misses, this is for you.",
            False
        ]
    ]
    textMaker = []
    useSaveSettings = True
    choice = 0

    a = 'assets/saves/save.txt'
    if not checkFileExists(a):
        save = open(a, 'w')
        debugPrint(f'save file created at {a}')
    else:
        save = open(a, 'r')
        save = save.read()
        save = save.splitlines()
    for i in range(len(coolOptions)):
        textMaker.append([])
        try:
            if save[i] == "0":
                save[i] = False
            elif save[i] == "1":
                save[i] = True
        except IndexError:
            save.append(coolOptions[i][3])
            useSaveSettings = False
        for j in range(2):
            textMaker[i].append(pygame.font.Font('assets/fonts/vcr.ttf', 40))
    if useSaveSettings:
        for i in range(len(coolOptions)):
            coolOptions[i][3] = save[i]

    desc = pygame.font.Font('assets/fonts/vcr.ttf', 30)
    menuBGMagenta = pygame.image.load('assets/image/menuBGMagenta.png')
    pygame.mixer.music.load('assets/music/settings.ogg')
    pygame.mixer.music.play(-1)

    bpm = 99.1
    curBeat = 1
    zoomForce = 0
    timeOld = -time.time()

    while True:
        screen.fill('black')
        screen.blit(menuBGMagenta, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    playSound("scrollMenu")
                    choice += 1
                    if choice == 1:
                        choice = -len(coolOptions)+1
                if event.key == pygame.K_DOWN:
                    playSound("scrollMenu")
                    choice -= 1
                    if choice == -len(coolOptions):
                        choice = 0
                if event.key == pygame.K_RETURN:
                    if coolOptions[abs(choice)][1] == "BOOL":
                        save[abs(choice)] = not save[abs(choice)]
                    playSound("scrollMenu")
                if event.key == pygame.K_BACKSPACE:
                    if checkFileExists(a):
                        deleteFile(a)
                    file = ""
                    for i in range(len(save)):
                        if coolOptions[i][1] == "BOOL":
                            file += f"{1 if save[i] else 0}\n"
                    garbage = open(a, 'w')
                    garbage.write(file)
                    garbage.close()
                    debugPrint("Save file created in assets/saves/save.txt")
                    pygame.mixer.music.stop()
                    import Main
                    return 0
                
        for i in range(len(textMaker)):
            for j in range(2):
                stupit = textMaker[i][j].render((coolOptions[i][0] if j == 0 else str(save[i])), True, (255, 255, 255) if -i == choice else (50, 50, 50))
                screen.blit(stupit, ((350*(j+1)), 50+(60*i)))
                if -i == choice:
                    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(40, 610, 1200, 90))
                    cool = desc.render(coolOptions[i][2], True, (255, 255, 255))
                    screen.blit(cool, (640-(len(coolOptions[i][2])*9), 640))

        timeNow = timeOld+time.time()
        if timeNow > (60/bpm)*curBeat:
            curBeat += 1
            zoomForce = 40
        zoomed_screen = pygame.transform.smoothscale(screen, (1280+zoomForce, 720+(zoomForce/1.5)))
        screen.blit(zoomed_screen, (-zoomForce/2, -zoomForce/3.33))
        zoomForce = (zoomForce/1.125)

        FPS.tick()
        pygame.display.flip()
        clock.tick(60)