import pygame
from room import *
from gameObject import *


def getLevel(x, scr):
    if x == 1:
        return Level([5, .05, .1, .5, .25, 10, 4, 14], 'Level1', 1, .5, (0, 0, 0), 1, 1,1, scr)
    return 0


def run(screen):
    running = True
    p1 = Player(500, 250, screen)
    currentLevel = 1
    isLevelComplete = False
    clock = pygame.time.Clock()
    level = getLevel(1, screen)
    p1.giveWeapon(Projectile(Sprite('block.spr', 0, 0, (255, 0, 0), -1, 1, screen), 12, 10, 10, False, True, False, 5, 10))
    tickClock = 0
    mCount = 1
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
                        p1.map = level.getCoords()
                    if event.key == pygame.K_u:
                        p1.flipWasd()
                    if event.key == pygame.K_m:
                        p1.addMessage('message {}'.format(mCount))
                        mCount += 1
                    if event.key == pygame.K_p:
                        pause = True
                        while pause:
                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    pause = False
                                    isLevelComplete = True
                                    running = False
                                elif e.type == pygame.KEYDOWN:
                                    if e.key == pygame.K_p:
                                        pause = False
                            clock.tick(60)
            flags = p1.getFlags()
            if flags[0]:
                p1.map = level.getCoords()
            if flags[1]:
                level.roomArr.currentRoom.enemiesBackup = '[]'
            p1.takeInput(pygame.key.get_pressed())
            level.update(p1)
            p1.update(level.returnAll())
            p1.drawHealthBar(64, 620, screen)
            p1.drawAutoMap(800, 620, screen)
            p1.drawMoneyCount(360, 660, screen)
            p1.drawCurrentItem(680, 620, screen)
            p1.drawMessage(64, 680, screen)
            # p1.drawPos(360, 630, screen)
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
        if currentLevel == 2:
            running = False
