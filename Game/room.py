import ast
import os
from gameObject import *
import pygame
import random
import math


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def makeNode(level, x, y, direct, length, curve, branch, special, dep):
    maximum = length
    final = random.randint(1, maximum) > length
    specialEnd = random.random() < special
    while not final:
        final = random.randint(1, maximum) > length
        if not (final and specialEnd) and random.random() < branch:
            change = random.randint(1, 2)
            if change == 2:
                change = -1
            d = (direct + change) % 4
            level = makeNode(level, x, y, d, maximum - 1, curve, branch * dep, special, dep)
        else:
            if random.random() < curve:
                change = random.randint(1, 2)
                if change == 2:
                    change = -1
                direct += change
                direct %= 4
            if direct == 0:
                y -= 1
            elif direct == 1:
                x += 1
            elif direct == 2:
                y += 1
            elif direct == 3:
                x -= 1
            if not (0 <= x <= 23 and 0 <= y <= 23) or level[y][x] != 'O':
                return level
            if level[y][x] != 'U' and level[y][x] != 'S':
                level[y][x] = 'N'
        length -= 1
    if specialEnd:
        level[y][x] = 'U'
    return level


def randLevel(nodeLen, branchProb, curveProb, specialProb, depreciation, minRooms, minSpecials):
    level = []
    for i in range(24):
        level.append([])
        for j in range(24):
            level[i].append('O')
    startX = 11 + random.randint(0, 1)
    startY = 11 + random.randint(0, 1)
    level[startY][startX] = 'S'
    for i in range(4):
        level = makeNode(level, startX, startY, i, nodeLen, curveProb, branchProb, specialProb, depreciation)
    roomCount = 0
    specialCount = 0
    x = 0
    y = 0
    for i in level:
        for j in i:
            if j == 'N' or j == 'S':
                roomCount += 1
            elif j == 'U':
                roomCount += 1
                if distance(startX, startY, x, y) < 1.5:
                    level[y][x] = 'N'
                else:
                    specialCount += 1
            x += 1
        y += 1
        x = 0
    if roomCount < minRooms or specialCount < minSpecials:
        return randLevel(nodeLen, branchProb, curveProb, specialProb, depreciation, minRooms, minSpecials)
    return level


class Room:
    def __init__(self, path, k, b, scr):
        self.screen = scr
        self.doors = []
        self.tiles = []
        self.key = k
        self.locks = []
        with open('Rooms\\' + path, 'r') as file:
            lines = file.readlines()
            counter = 0
            for line in lines:
                if counter == 0:
                    tilesI = eval(line)
                    tilesS = []
                    for i in range(len(tilesI)):
                        tilesS.append(tilesI[i].toString())
                elif counter == 1:
                    tileC = eval(line)
                    tileCount = 0
                    for i in tileC:
                        self.tiles.append(eval(tilesS[i[0]]))
                        self.tiles[tileCount].updatePos(i[1], i[2])
                        tileCount += 1
                elif counter == 2:
                    self.items = eval(line)
                elif counter == 3:
                    self.enemiesBackup = line
                    self.enemies = eval(line)
                counter += 1
        self.background = b

    def update(self, p1):
        self.screen.fill(self.background)
        for i in self.locks:
            i.update()
        for i in self.tiles:
            i.update()
        for i in self.items:
            i.update()
        for i in self.enemies:
            i.update(p1, self.tiles)

    def resetEnemies(self):
        self.enemies = eval(self.enemiesBackup)

    def setDoors(self, u, d, l, r):
        self.doors = []
        if u:
            self.doors.append(Tile(Sprite('block.txt', 448, 0, (0, 0, 0), -1, 8, self.screen), False, False, 100, 'Up'))
            self.doors.append(Tile(Sprite('block.txt', 512, 0, (0, 0, 0), -1, 8, self.screen), False, False, 100, 'Up'))
        if d:
            self.doors.append(
                Tile(Sprite('block.txt', 448, 512, (0, 0, 0), -1, 8, self.screen), False, False, 100, 'Down'))
            self.doors.append(
                Tile(Sprite('block.txt', 512, 512, (0, 0, 0), -1, 8, self.screen), False, False, 100, 'Down'))
        if l:
            self.doors.append(
                Tile(Sprite('block.txt', 0, 256, (0, 0, 0), -1, 8, self.screen), False, False, 100, 'Left'))
        if r:
            self.doors.append(
                Tile(Sprite('block.txt', 960, 256, (0, 0, 0), -1, 8, self.screen), False, False, 100, 'Right'))
        for i in self.tiles:
            if u and (i.getPos() == [448, 0] or i.getPos() == [512, 0]):
                i.kill()
            elif d and (i.getPos() == [448, 512] or i.getPos() == [512, 512]):
                i.kill()
            elif l and i.getPos() == [0, 256]:
                i.kill()
            elif r and i.getPos() == [960, 256]:
                i.kill()

    def setLocks(self, u, d, l, r):
        if u != 0:
            self.locks.append(Tile(Sprite('door.txt', 448, 0, (255, 255, 255), -1, 4, self.screen), True, False, 100,
                                   'Key' + str(u)))
            self.locks.append(Tile(Sprite('door.txt', 512, 0, (255, 255, 255), -1, 4, self.screen), True, False, 100,
                                   'Key' + str(u)))
        if d != 0:
            self.locks.append(Tile(Sprite('door.txt', 448, 512, (255, 255, 255), -1, 4, self.screen), True, False, 100,
                                   'Key' + str(d)))
            self.locks.append(Tile(Sprite('door.txt', 512, 512, (255, 255, 255), -1, 4, self.screen), True, False, 100,
                                   'Key' + str(d)))
        if l != 0:
            self.locks.append(Tile(Sprite('door.txt', 0, 256, (255, 255, 255), -1, 4, self.screen), True, False, 100,
                                   'Key' + str(l)))
        if r != 0:
            self.locks.append(Tile(Sprite('door.txt', 960, 256, (255, 255, 255), -1, 4, self.screen), True, False, 100,
                                   'Key' + str(r)))

    def returnAll(self):
        return self.locks + self.doors + self.tiles + self.items + self.enemies


class RoomArray:

    def __init__(self, r, b, s):
        self.rooms = []
        self.coords = []
        self.currentCoords = [0, 0]
        lockedRooms = []
        keys = []
        for i in r:
            self.rooms.append(Room(i[0], i[3], b, s))
            self.coords.append([i[1], i[2]])
            if i[3] > 0:
                lockedRooms.append([i[1], i[2]])
                keys.append(i[3])
        self.currentRoom = self.rooms[self.coords.index([0, 0])]
        for i in range(len(self.rooms)):
            x = self.coords[i][0]
            y = self.coords[i][1]
            u = False
            d = False
            l = False
            r = False
            u1 = 0
            d1 = 0
            l1 = 0
            r1 = 0
            if [x, y + 1] in self.coords:
                u = True
                if [x, y + 1] in lockedRooms:
                    u1 = keys[lockedRooms.index([x, y + 1])]
            if [x, y - 1] in self.coords:
                d = True
                if [x, y - 1] in lockedRooms:
                    d1 = keys[lockedRooms.index([x, y - 1])]
            if [x + 1, y] in self.coords:
                r = True
                if [x + 1, y] in lockedRooms:
                    r1 = keys[lockedRooms.index([x + 1, y])]
            if [x - 1, y] in self.coords:
                l = True
                if [x - 1, y] in lockedRooms:
                    l1 = keys[lockedRooms.index([x - 1, y])]
            self.rooms[i].setDoors(u, d, l, r)
            self.rooms[i].setLocks(u1, d1, l1, r1)

    def addRoom(self, r):
        self.rooms.append(r)

    def update(self, player):
        roomC = player.getRoomChange()
        if roomC > 0:
            if roomC == 1:
                player.move(0, 400)
            elif roomC == 2:
                player.move(-860, 0)
            elif roomC == 3:
                player.move(0, -400)
            elif roomC == 4:
                player.move(832, 0)
            self.changeRoom(roomC)
        self.currentRoom.update(player)

    def changeRoom(self, x):
        if x > 4:
            return
        if x == 1:
            index = self.coords.index([self.currentCoords[0], self.currentCoords[1] + 1])
            if index != -1:
                self.currentCoords[1] += 1
        elif x == 2:
            index = self.coords.index([self.currentCoords[0] + 1, self.currentCoords[1]])
            if index != -1:
                self.currentCoords[0] += 1
        elif x == 3:
            index = self.coords.index([self.currentCoords[0], self.currentCoords[1] - 1])
            if index != -1:
                self.currentCoords[1] -= 1
        else:
            index = self.coords.index([self.currentCoords[0] - 1, self.currentCoords[1]])
            if index != -1:
                self.currentCoords[0] -= 1
        self.currentRoom = self.rooms[index]
        self.currentRoom.resetEnemies()


class Level:

    def __init__(self, l, p, c, d, b, s):
        self.path = 'Rooms\\' + p
        self.rooms = os.listdir(self.path)
        self.rooms.remove('Specials')
        self.specialRooms = os.listdir(self.path + '\\Specials')
        self.specialRooms.remove('Start.txt')
        self.specialRooms.remove('Exit.txt')
        self.specialRooms.remove('ExitKeyRoom.txt')
        if str == type(l):
            with open('Levels\\' + l, 'r') as file:
                lines = file.readlines()
                layout = lines[random.randint(0, len(lines) - 1)]
                file.close()
        else:
            layout = ''
            for i in randLevel(l[0], l[1], l[2], l[3], l[4], l[5], l[6]):
                for j in i:
                    layout += j
        xOff, yOff = layout.index('S') % 24, int(layout.index('S') / 24)
        roomList = []
        specials = []
        roomList.append([p + '\\Specials\\Start.txt', 0, 0, 0])
        x = 0
        y = 0
        for i in layout:
            if i == 'N':
                roomList.append([self.randRoom(), x - xOff, y - yOff, 0])
            if i == 'U':
                specials.append([x - xOff, y - yOff])
            x += 1
            if x == 24:
                y += 1
                x = 0
        temp = specials.pop(random.randint(0, len(specials) - 1))
        roomList.append([p + '\\Specials\\ExitKeyRoom.txt', temp[0], temp[1], 0])
        temp = specials.pop(random.randint(0, len(specials) - 1))
        roomList.append([p + '\\Specials\\Exit.txt', temp[0], temp[1], 1])
        while len(specials) > 0 and random.random() < c:
            temp = specials.pop(random.randint(0, len(specials) - 1))
            roomList.append([p + '\\Specials\\' + self.randSpecialRoom(), temp[0], temp[1], 0])
            c *= d
        while len(specials) > 0:
            temp = specials.pop(0)
            roomList.append([self.randRoom(), temp[0], temp[1], 0])
        self.roomArr = RoomArray(roomList, b, s)

    def randRoom(self):
        return self.rooms[random.randint(0, len(self.rooms) - 1)]

    def randSpecialRoom(self):
        return self.specialRooms[random.randint(0, len(self.specialRooms) - 1)]

    def seeRooms(self):
        print(self.rooms)

    def getCoords(self):
        return self.roomArr.coords

    def update(self, player):
        self.roomArr.update(player)

    def getMap(self):
        ret = []
        for i in self.roomArr.coords:
            ret.append([i[0], -1 * i[1]])
        return ret

    def returnAll(self):
        return self.roomArr.currentRoom.returnAll()
