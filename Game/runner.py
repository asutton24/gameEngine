import pygame
from sprite import *
from gameObject import *

def main():
    running = True
    pygame.init()
    screen = pygame.display.set_mode([1024, 720], pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    player = Sprite('player.txt', 100, 100, (255, 255, 255), 30, .5, screen)
    hello = Text('i can now/display/sprites', 0, 0, (255, 255, 255), 5, screen)
    colorSpr = ColorSprite('colorTest.txt', 100, 100, [(255, 0, 0), (0, 255, 0), (0, 0, 255)], -1, 5, screen)
    p1 = Player(0, 0, screen)
    block = GameObject(Sprite('block.txt', 400, 200, (255, 255, 255), -1,5, screen), True, 1)
    count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((100,100,100))
        p1.takeInput(pygame.key.get_pressed())
        p1.update([block])
        block.update([])
        player.update()
        pygame.display.update()
        clock.tick(60)

main()