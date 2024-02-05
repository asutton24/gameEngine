import pygame
import game

def main():
    running = True
    pygame.init()
    screen = pygame.display.set_mode([1024, 720], pygame.FULLSCREEN)
    game.run(screen)


main()
