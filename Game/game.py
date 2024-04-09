import pygame
from room import *
from gameObject import *


def getLevel(x, scr):
    if x == 1:
        return Level([5, .05, .1, .5, .25, 10, 4, 14], 'Level1', 1, .5, (0, 0, 0), 1, 1,1, scr)
    if x == 2:
        return Level([8, .08, .15, .5, .25, 14, 4, 18], 'Level2', 1, .5, (0, 0, 0), 1.2, 1, 1.2, scr)
    if x == 3:
        return Level([10, .08, .3, .6, .25, 16, 4, 20], 'Level3', 1, .5, (0, 0, 0), 1.3, 1.15, 1.3, scr)
    if x == 4:
        return Level([10, .08, .3, .6, .25, 16, 4, 20], 'Level4', 1, .5, (0, 0, 0), 1.3, 1.2, 1.4, scr)
    if x == 5:
        lev = Level([], 'CUSTOM', 0, 0, (0, 0, 0), 0, 0, 0, scr)
        return lev
    return 0


def getMessages(p, a):
    if p == 'SpeedB' and a == .5:
        return ['The running man', 'speed up']
    if p == 'Heal' and a == 50:
        return ['medkit', 'instant health']
    if p == 'ExtraShot' and a == 1:
        return ['akimbo', 'gain another active shot']
    if p == 'HealthB' and a == 25:
        return ['spare heart', 'max health up']
    if p == 'Heal' and a == 25:
        return ['pill', 'usable healing']
    if p == 'RangeB' and a == 10:
        return ['scope', 'range up']
    if p == 'ArmorB' and a == 15:
        return ['Armored vest', 'negates some damage']
    return [p, p]


def home(screen):
    running = True
    selection = 0
    title = Text('title', 512 - len('title') * 40, 150, (255, 255, 255), 10, screen)
    clock = pygame.time.Clock()
    ret = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    running = False
                    ret = 1
                if event.key == pygame.K_BACKSPACE:
                    running = False
        screen.fill((0, 0, 0))
        title.update()
        pygame.display.update()
        clock.tick(60)
    return ret


def run(screen):
    running = True
    forceQuit = False
    interlude = True
    p1 = Player(500, 250, screen)
    currentLevel = 1
    screenState = 0
    clock = pygame.time.Clock()
    level = getLevel(1, screen)
    ret = 0
    doBoss = 0
    p1.giveWeapon(Projectile(Sprite('block.spr', 0, 0, (255, 0, 0), -1, 1, screen), 12, 10, 10, False, True, False, 5, 10))
    while running and not forceQuit:
        p1.updatePos(500, 250)
        p1.changeColor((255, 255, 255))
        isLevelComplete = False
        if currentLevel == 0:
            isLevelComplete = True
        fadeOut = 351
        while not isLevelComplete and not forceQuit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    forceQuit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        forceQuit = True
                    if event.key == pygame.K_r:
                        p1.map = level.getCoords()
                    if event.key == pygame.K_u:
                        p1.flipWasd()
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
                    if event.key == pygame.K_w:
                        isLevelComplete = True
                        p1.resetMap()
                    if event.key == pygame.K_m:
                        p1.inventory.money += 100
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
            # p1.drawIframes(300, 660, screen)
            level.drawCurrentCoords(300, 630, screen)
            level.showPath(200, 590)
            # p1.drawPos(360, 630, screen)
            if p1.exitRoom:
                p1.exitRoom = False
                fadeOut -= 1
            doBoss = p1.checkBoss()
            if doBoss > 0:
                fadeOut -= 1
            if fadeOut <= 350:
                fadeOut -= 2.5
                if fadeOut >= 95:
                    p1.changeColor((fadeOut - 95, fadeOut - 95, fadeOut - 95))
                if fadeOut <= 0:
                    isLevelComplete = True
            if p1.health <= 0:
                interlude = False
                running = False
                isLevelComplete = True
                ret = 1
            pygame.display.update()
            clock.tick(60)
        currentLevel += 1
        level = getLevel(currentLevel, screen)
        interlude = True
        if currentLevel == 5:
            running = False
            interlude = False
        items = []
        for i in range(3):
            unique = False
            while not unique:
                newI = randItem(0, screen)
                newI.sprite.scale *= 3
                unique = True
                for j in range(i):
                    if newI.isEqual(items[j]):
                        unique = False
                        break
            items.append(newI)
            items[i].sprite.y = 310
            items[i].sprite.x = 170 + i * 256
        msg = [Text("floor cleared!", 512 - len("floor cleared!") * 16, 100, (255, 255, 255), 4, screen),
               Text("pick an item", 512 - len("pick an item") * 8, 170, (255, 255, 255), 2, screen), 0, 0]
        index = 0
        finished = 121
        while interlude and not forceQuit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    forceQuit = True
                elif event.type == pygame.KEYDOWN and finished == 121:
                    if event.key == pygame.K_RIGHT:
                        index += 1
                        if index == 3:
                            index = 0
                    elif event.key == pygame.K_LEFT:
                        index -= 1
                        if index == -1:
                            index = 2
                    elif event.key == pygame.K_z:
                        finished = 120
                    elif event.key == pygame.K_BACKSPACE:
                        forceQuit = True
            screen.fill((0, 0, 0))
            pur = items[index].getPurpose()[0]
            amo = items[index].getPurpose()[1]
            messages = getMessages(pur, amo)
            msg[2] = Text(messages[0], 512 - len(messages[0]) * 16, 550, (255, 255, 255), 4, screen)
            msg[3] = Text(messages[1], 512 - len(messages[1]) * 8, 620, (255, 255, 255), 2, screen)
            for i in msg:
                i.update()
            if finished == 121:
                pygame.draw.rect(screen, (255, 255, 255), [160 + index * 256, 300, 212, 212])
                pygame.draw.rect(screen, (0, 0, 0), [170 + index * 256, 310, 192, 192])
            elif finished == 0:
                interlude = False
                items[index].sprite.scale /= 3
                if items[index].boost:
                    p1.updatePos(0, 0)
                    items[index].updatePos(0, 0)
                    p1.update([items[index]])
                else:
                    p1.inventory.addItem(items[index])
            else:
                finished -= 1
            for i in items:
                i.update()
            pygame.display.update()
            clock.tick(60)
    return ret

