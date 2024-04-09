import pygame
import game


def main():
    running = True
    quickStart = True
    pygame.init()
    screen = pygame.display.set_mode([1024, 768], pygame.FULLSCREEN)
    status = 0
    if quickStart:
        running = False
        game.run(screen)
    while running:
        if game.home(screen) == 0 or game.run(screen) == 0:
            running = False



main()
