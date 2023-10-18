import pygame
from sprite import *
from gameObject import *

def main():
    running = True
    pygame.init()
    screen = pygame.display.set_mode([640, 480])
    clock = pygame.time.Clock()
    player = Sprite('player.txt', 100, 100, (255, 255, 255), 30, 10, screen)
    hello = Text('i can now/display/sprites', 0, 0, (255, 255, 255), 5, screen)
    colorSpr = ColorSprite('colorTest.txt', 100, 100, [(255, 0, 0), (0, 255, 0), (0, 0, 255)], -1, 5, screen)
    gameObj = GameObject(player, False, 100, False)
    vel = 5
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0,0,0))
        colorSpr.update()
        if colorSpr.getPos()[0] >= 600:
            vel = -5
        elif colorSpr.getPos()[0] <= 0:
            vel = 5
        colorSpr.move(vel, 0)
        pygame.display.update()
        clock.tick(60)

main()