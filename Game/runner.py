import pygame
from sprite import *
from room import *
from gameObject import *

def main():
    running = True
    pygame.init()
    screen = pygame.display.set_mode([1024, 720])
    clock = pygame.time.Clock()
    player = Sprite('player.txt', 500, 250, (255, 255, 255), 30, .5, screen)
    hello = Text('i can now/display/sprites', 0, 0, (255, 255, 255), 5, screen)
    colorSpr = ColorSprite('colorTest.txt', 100, 100, [(255, 0, 0), (0, 255, 0), (0, 0, 255)], -1, 5, screen)
    p1 = Player(500, 250, screen)
    room1 = Room('Manifest\\RoomManifest.txt', 0, (0, 0, 0), screen)
    room1.setDoors(True, True, True, True)
    testEnemy = Enemy([Sprite('enemyR.txt', 500, 300, (255, 0, 0), 10, 6, screen), Sprite('enemyL.txt', 100, 100, (255, 0, 0), 10, 6, screen)], 2, 0, 3, 128, False, 100, [], 0, [4, Projectile(Sprite('block.txt', 0, 0, (0, 255, 0), -1, 1, screen), 60, 5, 1, False, False, False, 5, 10), 1, .9999], [], 30)
    #faceTest = Enemy([Sprite('d.txt', 300, 200, (0, 255, 0), -1, 8, screen), Sprite('l.txt', 100, 100, (0, 255, 0), -1, 8, screen), Sprite('u.txt', 100, 100, (0, 255, 0), -1, 8, screen), Sprite('r.txt', 100, 100, (0, 255, 0), -1, 8, screen)], 4, 4, 1, 1, False, 1, [], 0, [], [[300, 200], [400, 200], [400, 300], [300, 300], 1], 0)
    count = 0
    p1.giveWeapon(Projectile(Sprite('block.txt', 0, 0, (255, 0, 0), -1, 1, screen), 60, 5, 1, False, True, False, 5, 10))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    running = False
        p1.takeInput(pygame.key.get_pressed())
        room1.update()
        p1.update(room1.returnAll() + [testEnemy])
        testEnemy.update(p1, room1.returnAll())
        #faceTest.update(p1, room1.returnAll())
        if p1.getRoomChange() != 0:
            disp = Text('Touching', 0, 612, (255, 255, 255), 2, screen)
        else:
            disp = Text('Not Touching', 0, 612, (255, 255, 255), 2, screen)
        disp.update()
        pygame.display.update()
        clock.tick(60)

main()