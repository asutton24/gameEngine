import os
from gameObject import *
import pygame

pygame.init()
screen = pygame.display.set_mode([1024, 720])
rooms = os.listdir('RoomSaves')
tiles = []
enemies = []
items = []
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
for room in rooms:
    board = []
    for i in range(9):
        board.append([])
        for j in range(16):
            board[i].append([])
    with open('RoomSaves\\' + room, 'r') as file:
        info = eval(file.readline())
        file.close()
    for i in info:
        coords = i.pop(0)
        board[coords[0]][coords[1]] = i
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
                        proj.append(Projectile(
                            Sprite(projArr[1][0][0], 0, 0, projArr[1][0][1], projArr[1][0][2], projArr[1][0][3],
                                   screen), projArr[1][1], projArr[1][2], projArr[1][3],
                            projArr[1][4], projArr[1][5], projArr[1][6], projArr[1][7], projArr[1][8]))
                        proj.append(projArr[2])
                        proj.append(projArr[3])
                    if len(k) == 3:
                        point = []
                    else:
                        point = k[3]
                    temp = Enemy(tSprites, enemies[k[1]][4], enemies[k[1]][5], enemies[k[1]][6], enemies[k[1]][7],
                                 enemies[k[1]][8], enemies[k[1]][9], enemies[k[1]][10], enemies[k[1]][11], proj, point,
                                 enemies[k[1]][13])
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
                    if k[0] == 't' and t.isEqual(
                            Tile(k[2], tiles[k[1]][4], tiles[k[1]][5], tiles[k[1]][6], tiles[k[1]][7])):
                        saveTiles.append([counter, k[2].x, k[2].y])
                        break
                    counter += 1
    tempPath = room
    tempPath = tempPath[0: len(tempPath)-4]
    currentChar = 1
    numLen = 0
    path = 'Rooms\\Level'
    while tempPath[currentChar] in '0123456789':
        numLen += 1
        currentChar += 1
    path += tempPath[1:numLen+1] + '\\'
    if tempPath[currentChar] == 'r':
        path += tempPath + '.room'
    else:
        path += 'Specials\\' + tempPath + '.room'
    with open(path, 'w') as file:
        pass
        file.close()
    with open(path, 'w') as file:
        file.write('{}\n{}\n{}\n{}'.format(tileIndex, saveTiles, saveItems, saveEnemies))
        file.close()
print('Compiled!')
