import pygame
from sprite import *

def main():
    running = True
    pygame.init()
    screen = pygame.display.set_mode([640, 480])
    clock = pygame.time.Clock()
    player = Sprite('player.txt', 100, 100, (255, 255, 255), 30, 10, screen)
    hello = Text('i can now/display/sprites', 0, 0, (255, 255, 255), 5, screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0,0,0))
        hello.update()
        pygame.display.update()
        clock.tick(60)

main()