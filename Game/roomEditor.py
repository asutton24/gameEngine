import math
import pygame
from gameObject import *
from sprite import Text, Counter


def newBoard():
    b = []
    for i in range(9):
        b.append([])
        for j in range(16):
            b[i].append([])
    return b


def drawBG(scr):
    counter = 0
    for i in range(9):
        if i % 2 == 0:
            counter = 0
        else:
            counter = 1
        for j in range(16):
            if counter % 2 == 0:
                pygame.draw.rect(scr, (50, 50, 50), (j * 64, i * 64, 64, 64))
            else:
                pygame.draw.rect(scr, (70, 70, 70), (j * 64, i * 64, 64, 64))
            counter += 1

def main():
    pygame.init()
    running = True
    screen = pygame.display.set_mode([1152, 576])
    clock = pygame.time.Clock()
    tiles = []
    enemies = []
    items = []
    board = newBoard()
    points = []
    pointSprites = []
    drawMode = True
    pointText = Text('enter/points/when/done/l for/loop/r for/reverse', 1024, 100, (255, 255, 255), 2, screen)
    mode = 't'
    index = 0
    realX = 0
    realY = 0
    new = True
    with open('Manifest\\TileManifest.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            tiles.append(ast.literal_eval(line))
        file.close()
    with open('Manifest\\ItemManifest.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            items.append(ast.literal_eval(line))
        file.close()
    with open('Manifest\\EnemyManifest.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            enemies.append(ast.literal_eval(line))
        file.close()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and drawMode:
                if event.button == 1:
                    if mode == 't':
                        board[realY][realX].append(['t', index, Sprite(tiles[index][0], realX * 64, realY * 64, tiles[index][1], tiles[index][2], tiles[index][3], screen)])
                    if mode == 'i':
                        board[realY][realX].append(['i', index, Sprite(items[index][0], realX * 64, realY * 64, items[index][1], items[index][2], items[index][3], screen)])
                    if mode == 'e':
                        if enemies[index][5] == 4:
                            drawMode = False
                            points = []
                            pointSprites = []
                            tempX = realX
                            tempY = realY
                        else:
                            if type(enemies[index][0]) == list:
                                board[realY][realX].append(['e', index, Sprite(enemies[index][0][0], realX * 64, realY * 64, enemies[index][1], enemies[index][2], enemies[index][3], screen)])
                            else:
                                board[realY][realX].append(['e', index, Sprite(enemies[index][0], realX * 64, realY * 64, enemies[index][1], enemies[index][2], enemies[index][3], screen)])
            elif event.type == pygame.MOUSEBUTTONDOWN and not drawMode:
                if event.button == 1:
                    points.append([realX * 64, realY * 64])
                    pointSprites.append(Sprite('smallBlock.txt', realX * 64, realY * 64, (255, 0, 0), -1, 8, screen))
                elif event.button == 2:
                    points = []
                    pointSprites = []
            if event.type == pygame.KEYDOWN and drawMode:
                if event.key == pygame.K_RIGHT:
                    if (mode == 't' and index != len(tiles) - 1) or (mode == 'i' and index != len(items) - 1) or (mode == 'e' and index != len(enemies) - 1):
                        index += 1
                elif event.key == pygame.K_LEFT:
                    if index != 0:
                        index -= 1
                elif event.key == pygame.K_t:
                    mode = 't'
                    index = 0
                elif event.key == pygame.K_i:
                    mode = 'i'
                    index = 0
                elif event.key == pygame.K_e:
                    mode = 'e'
                    index = 0
                elif event.key == pygame.K_l:
                    board = newBoard()
                    with open('RoomSaves\\' + input('Enter file location: '), 'r') as file:
                        info = eval(file.readline())
                        file.close()
                    for i in info:
                        coords = i.pop(0)
                        board[coords[0]][coords[1]] = i
                elif event.key == pygame.K_BACKSPACE:
                    board = newBoard()
                elif event.key == pygame.K_f:
                    if mode == 't':
                        for i in range(16):
                            board[0][i].append(['t', index, Sprite(tiles[index][0], i * 64, 0, tiles[index][1], tiles[index][2], tiles[index][3], screen)])
                            board[8][i].append(['t', index, Sprite(tiles[index][0], i * 64, 512, tiles[index][1], tiles[index][2], tiles[index][3], screen)])
                        for i in range(7):
                            board[i+1][0].append(['t', index, Sprite(tiles[index][0], 0, (i+1) * 64, tiles[index][1], tiles[index][2], tiles[index][3], screen)])
                            board[i + 1][15].append(['t', index, Sprite(tiles[index][0], 960, (i + 1) * 64, tiles[index][1], tiles[index][2], tiles[index][3], screen)])
                elif event.key == pygame.K_p:
                    for i in board:
                        for j in i:
                            for k in j:
                                if k[0] == 'e':
                                    print(k)
                elif event.key == pygame.K_s:
                    boardInfo = []
                    yi = 0
                    xi = 0
                    currentI = -1
                    for i in board:
                        for j in i:
                            if len(j) > 0:
                                boardInfo.append([[yi, xi]])
                                currentI += 1
                            for k in j:
                                boardInfo[currentI].append(k)
                            xi += 1
                        yi += 1
                        xi = 0
                    saveStr = '['
                    count = 0
                    mMax = len(boardInfo) - 1
                    for i in boardInfo:
                        sCount = 0
                        maximum = len(i) - 1
                        saveSub = '['
                        for j in i:
                            if sCount == 0:
                                saveSub += '[{}, {}]'.format(j[0], j[1])
                            else:
                                if len(j) == 3:
                                    saveSub += "['{}', {}, {}]".format(j[0], j[1], j[2].editorString())
                                else:
                                    saveSub += "['{}', {}, {}, {}]".format(j[0], j[1], j[2].editorString(), j[3])
                            if sCount < maximum:
                                sCount += 1
                                saveSub += ', '
                            else:
                                saveSub += ']'
                        saveStr += saveSub
                        if count < mMax:
                            count += 1
                            saveStr += ', '
                        else:
                            saveStr += ']'
                    with open('RoomSaves\\' + input('Enter save location: '), 'w') as file:
                        file.write(saveStr)
                        file.close()
                elif event.key == pygame.K_c:
                    tileTypes = []
                    saveItems = '['
                    saveEnemies = '['
                    for i in board:
                        for j in i:
                            for k in j:
                                if k[0] == 't':
                                    found = False
                                    temp = Tile(k[2], tiles[k[1]][4], tiles[k[1]][5], tiles[k[1]][6], tiles[k[1]][7])
                                    for t in tileTypes:
                                        if t.isEqual(temp):
                                            found = True
                                            break
                                    if not found:
                                        tileTypes.append(Tile(k[2], tiles[k[1]][4], tiles[k[1]][5], tiles[k[1]][6], tiles[k[1]][7]))
                                if k[0] == 'i':
                                    temp = Item(k[2], [items[k[1]][4], items[k[1]][5]], items[k[1]][6], items[k[1]][7])
                                    saveItems += temp.toString() + ', '
                                if k[0] == 'e':
                                    if type(enemies[k[1]][0]) == list:
                                        tSprites = [k[2]]
                                        for i in range(1, len(enemies[k[1]][0])):
                                            tSprites.append(enemies[k[1]][0][i])
                                    else:
                                        tSprites = [k[2]]
                                    proj = []
                                    if len(enemies[k[1]][12]) != 0:
                                        projArr = enemies[k[1]][12]
                                        proj.append(projArr[0])
                                        proj.append(Projectile(Sprite(projArr[1][0][0], 0, 0, projArr[1][0][1], projArr[1][0][2], projArr[1][0][3], screen), projArr[1][1], projArr[1][2], projArr[1][3],
                                                    projArr[1][4], projArr[1][5], projArr[1][6], projArr[1][7], projArr[1][8]))
                                        proj.append(projArr[2])
                                        proj.append(projArr[3])
                                    if len(k) == 3:
                                        point = []
                                    else:
                                        point = k[3]
                                    temp = Enemy(tSprites, enemies[k[1]][4], enemies[k[1]][5], enemies[k[1]][6], enemies[k[1]][7], enemies[k[1]][8], enemies[k[1]][9], enemies[k[1]][10], enemies[k[1]][11], proj, point, enemies[k[1]][13])
                                    saveEnemies += temp.toString() + ', '
                    if len(saveItems) > 2:
                        saveItems = saveItems[0: len(saveItems) - 2]
                    if len(saveEnemies) > 2:
                        saveEnemies = saveEnemies[0: len(saveEnemies) - 2]
                    saveItems += ']'
                    saveEnemies += ']'
                    tileIndex = '['
                    if len(tileTypes) == 0:
                        tileIndex = '[]'
                    else:
                        counter = 1
                        for i in tileTypes:
                            pos = i.getPos()
                            i.updatePos(0, 0)
                            tileIndex += i.toString()
                            i.updatePos(pos[0], pos[1])
                            if counter == len(tileTypes):
                                tileIndex += ']'
                            else:
                                tileIndex += ', '
                            counter += 1
                    saveTiles = []
                    for i in board:
                        for j in i:
                            for k in j:
                                counter = 0
                                for t in tileTypes:
                                    if k[0] == 't' and t.isEqual(Tile(k[2], tiles[k[1]][4], tiles[k[1]][5], tiles[k[1]][6], tiles[k[1]][7])):
                                        saveTiles.append([counter, k[2].x, k[2].y])
                                        break
                                    counter += 1
                    path = input('Enter file destination within Rooms folder: ')
                    with open('Rooms\\' + path, 'w') as file:
                        file.write('{}\n{}\n{}\n{}'.format(tileIndex, saveTiles, saveItems, saveEnemies))
                        file.close()
            elif event.type == pygame.KEYDOWN and not drawMode:
                if event.key == pygame.K_l:
                    points.append(0)
                if event.key == pygame.K_r:
                    points.append(1)
                if event.key == pygame.K_l or event.key == pygame.K_r:
                    drawMode = True
                    if type(enemies[index][0]) == list:
                        board[realY][realX].append(['e', index, Sprite(enemies[index][0][0], tempX * 64, tempY * 64, enemies[index][1], -1, enemies[index][3], screen)] + [points])
                    else:
                        board[realY][realX].append(['e', index, Sprite(enemies[index][0], tempX * 64, tempY * 64, enemies[index][1], -1, enemies[index][3], screen)] + [points])
        screen.fill((0, 0, 0))
        drawBG(screen)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_x > 1023:
            mouse_x = 1023
        elif mouse_x < 0:
            mouse_x = 0
        if mouse_y > 575:
            mouse_y = 575
        elif mouse_y < 0:
            mouse_y = 0
        realX = math.floor(mouse_x / 64)
        realY = math.floor(mouse_y / 64)
        if mouse_buttons[2] and drawMode:
            board[realY][realX] = []
        for i in board:
            for j in i:
                for k in j:
                    k[2].update()
        if mode == 't':
            modeDisp = Text('Tiles', 1024, 448, (255, 255, 255), 2, screen)
            sampleSprite = Sprite(tiles[index][0], 1088, 512, tiles[index][1], tiles[index][2], tiles[index][3], screen)
        if mode == 'i':
            modeDisp = Text('Items', 1024, 448, (255, 255, 255), 2, screen)
            sampleSprite = Sprite(items[index][0], 1088, 512, items[index][1], items[index][2], items[index][3], screen)
        if mode == 'e':
            modeDisp = Text('Enemies', 1024, 448, (255, 255, 255), 2, screen)
            if type(enemies[index][0]) != list:
                sampleSprite = Sprite(enemies[index][0], 1088, 512, enemies[index][1], -1, enemies[index][3], screen)
            else:
                sampleSprite = Sprite(enemies[index][0][0], 1088, 512, enemies[index][1], -1, enemies[index][3], screen)
        sampleSprite.update()
        modeDisp.update()
        if not drawMode:
            pointText.update()
            for i in pointSprites:
                i.update()
        clock.tick(60)
        pygame.display.update()

main()