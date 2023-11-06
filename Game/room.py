import ast

from gameObject import *
import pygame
import random
import math

def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

def randomLevel(x, y, r):
    if r < 3:
        r = 3
    level = []
    mainRooms = []
    for i in range(y):
        level.append([])
        for j in range(x):
            level[i].append(0)
    for i in range(r):
        placed = False
        while not placed:
            randX = random.randint(0, x-1)
            randY = random.randint(0, y-1)
            if level[randY][randX] == 0:
                level[randY][randX] = 2
                placed = True
                mainRooms.append((randX, randY))
    connections = []
    for i in range(len(mainRooms)):
        first = [[0, 0], 10000]
        second = [[0, 0], 10000]
        for j in range(len(mainRooms)):
            if not ([i, j] in connections or [j, i] in connections) and i != j and distance(mainRooms[i][0], mainRooms[i][1], mainRooms[j][0], mainRooms[j][i]) < second[1]:
                if distance(mainRooms[i][0], mainRooms[i][1], mainRooms[j][0], mainRooms[j][i]) < first[1]:
                    first[0] = [mainRooms[j][0], mainRooms[j][1]]
                    first[1] = distance(mainRooms[i][0], mainRooms[i][1], mainRooms[j][0], mainRooms[j][i])
                else:
                    second[0] = [mainRooms[j][0], mainRooms[j][1]]
                    second[1] = distance(mainRooms[i][0], mainRooms[i][1], mainRooms[j][0], mainRooms[j][i])
                connections.append([i, j])
        print(connections)
        print(second)
        print(first)
        if second[1] != 10000:
            xlen = second[0][0] - mainRooms[i][0]
            ylen = second[0][1] - mainRooms[i][1]
            currentX = mainRooms[i][0]
            currentY = mainRooms[i][1]
            while xlen != 0 and ylen != 0:
                randX = random.randint(0,abs(xlen)+1)
                randY = random.randint(0,abs(ylen)+1)
                if xlen < 0:
                    moveDir = -1
                else:
                    moveDir = 1
                for i in range(randX + 1):
                    if level[currentY][currentX + i * moveDir] != 2:
                        level[currentY][currentX + i * moveDir] = 1
                currentX += moveDir * randX
                xlen -= moveDir * randX
                if ylen < 0:
                    moveDir = 1
                else:
                    moveDir = -1
                for i in range(randY+1):
                    if level[currentY + i * moveDir][currentX] != 2:
                        level[currentY + i * moveDir][currentX] = 1
                currentY += moveDir * randY
                ylen -= moveDir * randY
        if first[1] != 10000:
            xlen = first[0][0] - mainRooms[i][0]
            ylen = first[0][1] - mainRooms[i][1]
            currentX = mainRooms[i][0]
            currentY = mainRooms[i][1]
            while xlen != 0 and ylen != 0:
                randX = random.randint(0,abs(xlen)+1)
                randY = random.randint(0,abs(ylen)+1)
                if xlen < 0:
                    moveDir = -1
                else:
                    moveDir = 1
                for i in range(randX + 1):
                    if level[currentY][currentX + i * moveDir] != 2:
                        level[currentY][currentX + i * moveDir] = 1
                currentX += moveDir * randX
                xlen -= moveDir * randX
                if ylen < 0:
                    moveDir = 1
                else:
                    moveDir = -1
                for i in range(randY):
                    if level[currentY + i * moveDir][currentX] != 2:
                        level[currentY + i * moveDir][currentX] = 1
                currentY += moveDir * randY
                ylen -= moveDir * randY



    for i in range(y):
        str = ''
        for j in range(x):
            str += "{} ".format(level[i][j])
        print(str)

class Room:
    def __init__(self, path, index, b, scr):
        self.screen = scr
        self.doors = []
        with open(path, 'r') as file:
            lines = file.readlines()
            counter = 0
            for line in lines:
                if counter == index:
                    self.tiles, self.items = eval(line)
                    break
                counter += 1
        self.background = b
    def update(self):
        self.screen.fill(self.background)
        for i in self.tiles:
            i.update()
        for i in self.items:
            i.update()


    def setDoors(self, u, d, l, r):
        self.doors = []
        if u:
            self.doors.append(Tile(Sprite('block.txt', 448, 0, (0, 0, 0), -1, 8, self.screen), False, False, 100, 'Up'))
            self.doors.append(Tile(Sprite('block.txt', 512, 0, (0, 0, 0), -1, 8, self.screen), False, False, 100, 'Up'))
        if d:
            self.doors.append(Tile(Sprite('block.txt', 448, 512, (0, 0, 0), -1, 8, self.screen), False, False, 100, 'Down'))
            self.doors.append(Tile(Sprite('block.txt', 512, 512, (0, 0, 0), -1, 8, self.screen), False, False, 100, 'Down'))
        if l:
            self.doors.append(Tile(Sprite('block.txt', 0, 256, (0, 0, 0), -1, 8, self.screen), False, False, 100, 'Left'))
        if r:
            self.doors.append(Tile(Sprite('block.txt', 960, 256, (0, 0, 0), -1, 8, self.screen), False, False, 100, 'Right'))
        for i in self.tiles:
            if u and (i.getPos() == [448, 0] or i.getPos() == [512, 0]):
                i.kill()
            elif d and (i.getPos() == [448, 512] or i.getPos() == [512, 512]):
                i.kill()
            elif l and i.getPos() == [0, 256]:
                i.kill()
            elif r and i.getPos() == [960, 256]:
                i.kill()


    def returnAll(self):
        return self.doors + self.tiles + self.items
