import pygame
from sprite import *
from room import *
from gameObject import *

def main():
    running = True
    pygame.init()
    screen = pygame.display.set_mode([1024, 720], pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    player = Sprite('player.txt', 500, 250, (255, 255, 255), 30, .5, screen)
    hello = Text('i can now/display/sprites', 0, 0, (255, 255, 255), 5, screen)
    colorSpr = ColorSprite('colorTest.txt', 100, 100, [(255, 0, 0), (0, 255, 0), (0, 0, 255)], -1, 5, screen)
    p1 = Player(500, 250, screen)
    block = GameObject(Sprite('block.txt', 400, 200, (255, 255, 255), -1,5, screen), True, 1)
    room1 = Room('Manifest\\RoomManifest.txt', 0, (0, 0, 0), screen)
    room1.setDoors(True, True, True, True)
    count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    running = False
        p1.takeInput(pygame.key.get_pressed())
        room1.update()
        p1.update(room1.returnAll())
        if p1.getRoomChange() != 0:
            disp = Text('Touching', 0, 612, (255, 255, 255), 2, screen)
        else:
            disp = Text('Not Touching', 0, 612, (255, 255, 255), 2, screen)
        disp.update()
        pygame.display.update()
        clock.tick(60)

main()