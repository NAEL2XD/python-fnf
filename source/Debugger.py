import inspect
import os
import pygame
import psutil

# The debug function is also ai generated
# dude make your own code :sob: - intel

pygame.init()
screen = pygame.display.set_mode((1280,720), pygame.RESIZABLE)
clock = pygame.time.Clock()
fps1 = pygame.font.Font('assets/fonts/vcr.ttf', 16)
fps2 = pygame.font.Font('assets/fonts/vcr.ttf', 16)
process = psutil.Process()

cpu = 0
frame = 0
def tick():
    global frame, cpu
    e = fps1.render(f'FPS: {int(clock.get_fps())}', True, (255, 255, 255))
    ram = (process.memory_info().rss)/1000000
    ram = "{:.2f}".format(round(ram, 2))
    frame += 1
    if frame == 15:
        cpu = psutil.cpu_percent()
        frame = 0
    f = fps2.render(f'RAM: {ram} MB | CPU: {cpu}%', True, (255, 255, 255))
    screen.blit(e, (0, 0))
    screen.blit(f, (0, 16))
    pygame.display.flip()
    clock.tick(60)

def trace(*args):
    frame = inspect.currentframe().f_back
    filename = frame.f_code.co_filename
    filename_only = os.path.basename(filename)
    line_number = frame.f_lineno

    vscode_link = f"vscode://file/{filename}:{line_number}"
    clickable_link = f"\033[90m\033]8;;{vscode_link}\033\\{filename_only}:{line_number}\033]8;;\033\\\033[0m"
    output = f"{' '.join(map(str, args))}".rstrip()
    print(f"{output:<{100}}{clickable_link}")

def getHSContents():
    try:
        with open('assets/saves/highscore.txt', 'r') as file:
            lines = file.readlines()

        tables = []
        cT = []

        for line in lines:
            line = line.strip()
            if line:
                key, value = line.split(':')
                cT.append((key, value))
            else:
                tables.append(cT)
                cT = []

        if cT:
            tables.append(cT)

        return tables
    except FileNotFoundError:
        trace('FILE NOT FOUND: assets/saves/highscore.txt')
        return []
