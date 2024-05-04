import pygame
from room import *
from gameObject import *

global joystick


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
        lev.manualSetup(RoomArray([['Level5\\l5r1.room', 0, 0, 0], ['Level5\\l5r2.room', 1, 0, 0], ['Level5\\l5r3.room', 2, 0, 0]], (0, 0, 0), 1, 1, 1, scr))
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
    if p == 'DamageB' and a == 5:
        return ['Heavy Sword', 'damage up']
    if p == 'Map' and a == 1:
        return ['map', 'reveal the floor layout']
    if p == 'PermClear' and a == 1:
        return ['atomizer', 'set me on fire']
    if p == 'SuperShot' and a == 1:
        return ['sniper rifle', 'gain a powerful long range shot']
    if p == 'TempInvis' and a == 1:
        return ['idol', 'gain temporary invisibility']
    if p == 'SlowDecay' and a == 60:
        return ['stitches', 'life drains slower']
    if p == 'Skip' and a == 1:
        return ['nope button', 'skip a level']
    if p == 'HealthB' and a == 60:
        return ['super heart', 'max health way up']
    if p == 'Clear' and a == 1:
        return ['bomb', 'clear a room of enemies']
    if p == 'Money' and a == 150:
        return ['Money Bag', 'get $150']
    if p == 'Money' and a == 500:
        return ['bag of gold', 'get $500']
    if p == 'CannonShot' and a == 1:
        return ['Hand cannon', 'Gain a powerful short range shot']
    return [p, p]


def credits(screen):
    names = ['runner', 'guard', 'spike', 'turret', 'tank', 'gunner', 'sentinel']


def deathScreen(screen, score, state, controls):
    s = "score - {}".format(score)
    if state == 0:
        msg = "you died!"
    else:
        msg = "you win!"
    options = ["restart", "main menu"]
    text = [Text(msg, 512 - len(msg) * 24, 250, (255, 255, 255), 6, screen),
            Text(s, 512 - len(s) * 16, 330, (255, 255, 255), 4, screen),
            Text(options[0], 512 - len(options[0]) * 16, 370, (255, 255, 255), 4, screen),
            Text(options[1], 512 - len(options[1]) * 16, 410, (255, 255, 255), 4, screen)]
    running = True
    pointer = Sprite('block.spr', 320, 370, (255, 0, 0), -1, 4, screen)
    if controls == 0:
        up = pygame.K_UP
        down = pygame.K_DOWN
        select = pygame.K_z
    else:
        up = pygame.K_w
        down = pygame.K_s
        select = pygame.K_k
    selection = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == select:
                    running = False
                elif event.key == up or event.key == down:
                    if selection == 0:
                        selection = 1
                        pointer.y = 410
                    else:
                        selection = 0
                        pointer.y = 370
        pygame.draw.rect(screen, (255, 255, 255), [262, 184, 500, 400])
        pygame.draw.rect(screen, (0, 0, 0), [267, 189, 490, 390])
        for i in text:
            i.update()
        pointer.update()
        pygame.display.update()
    return selection


def endScreen(screen):
    clock = pygame.time.Clock()
    walls = []
    for i in range(16):
        walls.append(Sprite('block.spr', i * 64, 288, (255, 255, 255), -1, 8, screen))
        walls.append(Sprite('block.spr', i * 64, 416, (255, 255, 255), -1, 8, screen))
    running = True
    frameCount = 0
    teleporter = Sprite('exit.spr', 960, 352, (0, 0, 0), -1, 4, screen)
    player = Sprite('Player\\playerIdle.spr', 968, 360, (255, 255, 255), -1, 6, screen)
    color = 254
    while color != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return -1
        if 60 <= frameCount <= 315:
            teleporter.updateColor((frameCount - 60, frameCount - 60, frameCount - 60))
        if frameCount == 375:
            player = Sprite('Player\\playerMoveL.spr', 960, 360, (255, 255, 255), 3, 6, screen)
        if frameCount >= 376:
            player.x -= 3
        if frameCount >= 590:
            color -= 2
            for i in walls:
                i.updateColor((color, color, color))
            player.updateColor((color, color, color))
            teleporter.updateColor((color, color, color))
        screen.fill((0, 0, 0))
        if frameCount >= 345:
            player.update()
        for i in walls:
            i.update()
        teleporter.update()
        pygame.display.update()
        frameCount += 1
        clock.tick(60)


def settings(screen, current, fs):
    instructText = 'How to play'
    controlsText = ['Arrow Keys to move/z to attack/x to use an item/c to cycle through items/p to pause',
                    'wasd to move/k to attack/l to use an item/semicolon to cycle through items/p to pause']
    controlType = Text(controlsText[current], 100, 100, (255, 255, 255), 3, screen)
    select = Text('toggle controls/toggle fullscreen', 300, 500, (255, 255, 255), 4, screen)
    pointer = Sprite('block.spr', 260, 500, (255, 0, 0), -1, 4, screen)
    running = True
    clock = pygame.time.Clock()
    selection = 0
    if current == 0:
        up = pygame.K_UP
        down = pygame.K_DOWN
        s = pygame.K_z
    else:
        up = pygame.K_w
        down = pygame.K_s
        s = pygame.K_k
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == s:
                    if selection == 0:
                        current += 1
                        if current == 2:
                            current = 0
                        controlType = Text(controlsText[current], 100, 100, (255, 255, 255), 3, screen)
                    elif selection == 1:
                        if fs == 0:
                            fs = 1
                            screen = pygame.display.set_mode([1024, 768], pygame.FULLSCREEN)
                        else:
                            fs = 0
                            screen = pygame.display.set_mode([1024, 768])
                if event.key == up or event.key == down:
                    if selection == 0:
                        selection = 1
                        pointer.y = 540
                    else:
                        selection = 0
                        pointer.y = 500
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill((0, 0, 0))
        controlType.update()
        select.update()
        pointer.update()
        pygame.display.update()
        clock.tick(60)
    return 10 * fs + current


def home(screen, controls, high):
    running = True
    selection = 0
    name = 'one way out'
    score = Text('High score- {}'.format(high), 512 - len('High score- {}'.format(high)) * 16, 50, (255, 255, 255), 4, screen)
    title = Text(name, 512 - len(name) * 40, 150, (255, 255, 255), 10, screen)
    labels = ['play', 'help', 'quit']
    options = []
    y = 300
    for i in labels:
        options.append(Text(i, 512 - len(i) * 20, y, (255, 255, 255), 5, screen))
        y += 90
    icon = Sprite('Player\\playerIdle.spr', 300, 300, (255, 255, 255), -1, 5, screen)
    clock = pygame.time.Clock()
    selection = 0
    if controls == 1:
        select = pygame.K_k
        up = pygame.K_w
        down = pygame.K_s
    else:
        select = pygame.K_z
        up = pygame.K_UP
        down = pygame.K_DOWN
    stop = pygame.K_ESCAPE
    wait = 11
    while wait != 0:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == select:
                    wait -= 1
                if event.key == stop:
                    return 2
                if event.key == down:
                    if selection == 2:
                        icon.y = 300
                        selection = 0
                    else:
                        icon.y += 90
                        selection += 1
                if event.key == up:
                    if selection == 0:
                        icon.y = 480
                        selection = 2
                    else:
                        icon.y -= 90
                        selection -= 1
        if wait <= 10:
            wait -= 1
        screen.fill((0, 0, 0))
        title.update()
        for i in options:
            i.update()
        icon.update()
        score.update()
        pygame.display.update()
        clock.tick(60)
    return selection


def doBossFight(p1, screen):
    p1.changeColor((255, 255, 255))
    boss = BossRoom('bossRoom.room', (0, 0, 0), 0, [[3, 4], [5, 6]], 600, [1, 2], [1, 2], 300, 0, 180, screen)
    clock = pygame.time.Clock()
    running = True
    end = 0
    exit = 351
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return -1
                if event.key == pygame.K_p:
                    pause = True
                    while pause:
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                return -1
                            elif e.type == pygame.KEYDOWN:
                                if e.key == pygame.K_p:
                                    pause = False
                        clock.tick(60)
        if not boss.head.alive:
            end += 1
        if end == 1:
            offScreen = False
            color = (255, 255, 255)
            cNum = 255
            lineguy = [Sprite('lgl.spr', boss.head.getPos()[0], boss.head.getPos()[1], (0, 0, 0), -1, 4, screen),
                       Sprite('lgr.spr', boss.head.getPos()[0], boss.head.getPos()[1], (0, 0, 0), -1, 4, screen)]
            while color != (0, 0, 0):
                if not offScreen:
                    lineguy[0].move(-10, 0)
                    lineguy[1].move(10, 0)
                    offScreen = (lineguy[0].x <= -64) and (lineguy[1].x >= 1024)
                else:
                    cNum -= 5
                    color = (cNum, cNum, cNum)
                screen.fill(color)
                for i in lineguy:
                    i.update()
                pygame.display.update()
                clock.tick(60)
            end += 1
            boss.tiles.append(
                Tile(Sprite('exit.spr', 448, 256, (255, 255, 255), 6, 4, screen), False, False, 100, 'Boss100'))
            boss.tiles.append(
                Tile(Sprite('exit2.spr', 512, 256, (255, 255, 255), 6, 4, screen), True, False, 100, 'Normal'))
        if not p1.alive:
            return 0
        if p1.checkBoss() == 100:
            exit -= 1
        if exit <= 350:
            exit -= 2.5
            if exit >= 95:
                p1.changeColor((exit - 95, exit - 95, exit - 95))
            if exit <= 0:
                running = False
        screen.fill((0, 0, 0))
        p1.takeInput(pygame.key.get_pressed())
        boss.update(p1)
        p1.update(boss.returnAll())
        p1.drawHealthBar(64, 620, screen)
        p1.drawAutoMap(800, 620, screen)
        p1.drawMoneyCount(400, 620, screen)
        p1.drawCurrentItem(680, 620, screen)
        boss.drawBossHp(64, 690, screen)
        pygame.display.update()
        clock.tick(60)
    return 1


def run(screen, controls):
    running = True
    forceQuit = False
    interlude = True
    p1 = Player(500, 250, screen)
    currentLevel = 1
    clock = pygame.time.Clock()
    level = getLevel(currentLevel, screen)
    ret = 1
    doBoss = 0
    isGameComplete = False
    if controls == 2:
        p1.controller = True
        joystick = pygame.joystick.Joystick(0)
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
                    if event.key == pygame.K_ESCAPE:
                        forceQuit = True
                    if event.key == pygame.K_p:
                        pause = True
                        while pause:
                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    pause = False
                                    isLevelComplete = True
                                    running = False
                                    forceQuit = True
                                elif e.type == pygame.KEYDOWN:
                                    if e.key == pygame.K_p:
                                        pause = False
                            clock.tick(60)
            flags = p1.getFlags()
            if flags[0]:
                p1.map = level.getCoords()
            if flags[1] or flags[2]:
                level.roomArr.currentRoom.enemies = []
            if flags[2]:
                level.roomArr.currentRoom.enemiesBackup = '[]'
            if p1.controller:
                inp = []
                for i in range(joystick.get_numbuttons()):
                    inp.append(joystick.get_button(i))
                p1.takeInput(inp)
            else:
                p1.takeInput(pygame.key.get_pressed())
            level.update(p1)
            p1.update(level.returnAll())
            p1.drawHealthBar(64, 620, screen)
            p1.drawAutoMap(800, 620, screen)
            p1.drawMoneyCount(360, 660, screen)
            p1.drawCurrentItem(680, 620, screen)
            p1.drawMessage(64, 680, screen)
            # p1.drawIframes(300, 660, screen)
            # level.drawCurrentCoords(300, 630, screen)
            # level.showPath(200, 590)
            # p1.drawPos(360, 630, screen)
            if p1.exitRoom:
                p1.exitRoom = False
                fadeOut -= 1
            if doBoss > 0:
                fadeOut -= 1
            else:
                doBoss = p1.checkBoss()
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
        if doBoss > 0:
            bossStat = doBossFight(p1, screen)
            if bossStat == 1:
                isGameComplete = True
                p1.score += 3200
            elif bossStat == -1:
                forceQuit = True
            doBoss = 0
            p1.changeColor((255, 255, 255))
        currentLevel += 1
        interlude = True
        if p1.alive and not forceQuit:
            p1.score += 1000 + (currentLevel - 1) * 200 + int(p1.health) * 4
        if not p1.alive:
            ret = deathScreen(screen, p1.score, 0, controls)
            running = False
            interlude = False
        if isGameComplete:
            interlude = False
            endScreen(screen)
            ret = deathScreen(screen, p1.score, 1, controls)
        if currentLevel == 6 or not p1.alive:
            running = False
            interlude = False
        level = getLevel(currentLevel, screen)
        items = []
        for i in range(3):
            unique = False
            while not unique:
                itemType = random.randint(1, 10)
                if itemType > 1:
                    itemType = 0
                newI = randItem(itemType, screen)
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
        if controls == 0:
            left = pygame.K_LEFT
            right = pygame.K_RIGHT
            s = pygame.K_z
        else:
            left = pygame.K_a
            right = pygame.K_d
            s = pygame.K_k
        while interlude and not forceQuit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    forceQuit = True
                elif event.type == pygame.KEYDOWN and finished == 121:
                    if event.key == right:
                        index += 1
                        if index == 3:
                            index = 0
                    elif event.key == left:
                        index -= 1
                        if index == -1:
                            index = 2
                    elif event.key == s:
                        finished = 120
                    elif event.key == pygame.K_ESCAPE:
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
    return p1.score * 10 * (not forceQuit) + ret

