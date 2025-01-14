import pygame
import FPS
import Freeplay
import Settings
from Debugger import debugPrint

def playSound(sound):
    lmao = pygame.mixer.Sound(f"assets/sounds/{sound}.ogg")
    pygame.mixer.Sound.play(lmao)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()
    menuBG = pygame.image.load('assets/image/menuBG.png')

    options = [
        ['Freeplay', pygame.font.Font('assets/fonts/vcr.ttf', 80)],
        ['Settings', pygame.font.Font('assets/fonts/vcr.ttf', 80)],
    ]
    optionsChosen = 0

    while True:
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    playSound("scrollMenu")
                    optionsChosen += 1
                    if optionsChosen == 1:
                        optionsChosen = -len(options)+1
                if event.key == pygame.K_DOWN:
                    playSound("scrollMenu")
                    optionsChosen -= 1
                    if optionsChosen == -len(options):
                        optionsChosen = 0
                if event.key == pygame.K_RETURN:
                    py = abs(optionsChosen)
                    debugPrint(py)
                    if py == 0:
                        Freeplay.main()
                    elif py == 1:
                        Settings.main()
            
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("assets/music/freakyMenu.ogg")
            pygame.mixer.music.play()
            
        screen.blit(menuBG, (0, 0))

        for i in range(len(options)):
            piss = options[i][1].render(options[i][0], True, (255, 255, 255) if -i == optionsChosen else (50, 50, 50))
            screen.blit(piss, (75, 120+(80*i)))

        FPS.tick()
        pygame.display.flip()
        clock.tick(60)

main()