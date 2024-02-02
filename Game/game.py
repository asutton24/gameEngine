import pygame
from room import *
from gameObject import *

def getLevel(x, scr):
    if x == 1:
        return Level([5, .05, .1, .5, .25, 10, 2], '', 1, .5, (0, 0, 0), scr)

def run(screen):
    running = True
    p1 = Player(500, 250, screen)
    currentLevel = 1
    isLevelComplete = False
    clock = pygame.time.Clock()
    level = getLevel(1, screen)
    p1.giveWeapon(Projectile(Sprite('block.txt', 0, 0, (255, 0, 0), -1, 1, screen), 12, 10, 1, False, True, False, 5, 10))
    tickClock = 0
    while running:
        p1.updatePos(500, 250)
        while not isLevelComplete:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    isLevelComplete = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        running = False
                        isLevelComplete = True
                    if event.key == pygame.K_r:
                        p1.map = level.getMap()
                    if event.key == pygame.K_u:
                        p1.flipWasd()
            p1.takeInput(pygame.key.get_pressed())
            level.update(p1)
            p1.update(level.returnAll())
            p1.drawHealthBar(64, 620, screen)
            p1.drawAutoMap(800, 620, screen)
            tickClock += 1
            if tickClock == 60:
                tickClock = 0
                p1.damage(0)
            if p1.exitRoom:
                p1.exitRoom = False
                isLevelComplete = True
            pygame.display.update()
            clock.tick(60)
        currentLevel += 1
        level = getLevel(currentLevel, screen)
