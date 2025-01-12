import pygame
import psutil

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
fps1 = pygame.font.Font('assets/fonts/vcr.ttf', 16)
fps2 = pygame.font.Font('assets/fonts/vcr.ttf', 16)
process = psutil.Process()

def tick():
    e = fps1.render(f'FPS: {int(clock.get_fps())}', True, (255, 255, 255))
    f = fps2.render(f'RAM: {(process.memory_info().rss)/1000000} MB', True, (255, 255, 255))
    screen.blit(e, (0, 0))
    screen.blit(f, (0, 16))
    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)