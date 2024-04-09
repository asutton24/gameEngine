import os
import pygame
from gameObject import *


class Copier:

    def __init__(self):
        self.screen = pygame.display.set_mode([1024, 720])

    def copy(self):
        num = 1
        exclude = []
        print('Enter room numbers to exclude')
        while num != -1:
            num = int(input())
            if num != -1:
                exclude.append(num)
        start = int(input("Enter level to take from: "))
        target = int(input("Enter target level: "))
        rooms = os.listdir("Rooms\\Level{}".format(start))
        rooms.remove('Specials')
        color = eval(input('Enter floor color: '))
        takenNums = []
        takenRooms = os.listdir("Rooms\\Level{}".format(target))
        takenRooms.remove('Specials')
        for r in rooms:
            roomNum = int(r[r.index('r') + 1:r.index('.')])
            if roomNum in exclude:
                continue
            with open('Rooms\\Level{}\\{}'.format(start, r), 'r') as file:
                lines = file.readlines()
                tiles = eval(lines[0])
                newLine = '['
                count = 0
                for t in tiles:
                    if t.sprite.path == 'block.spr':
                        t.sprite.color = color
                    newLine += t.toString()
                    if count == len(tiles) - 1:
                        newLine += ']\n'
                    else:
                        newLine += ', '
                    count += 1
                lines[0] = newLine
                file.close()
            with open('Rooms\\Level{}\\l{}r{}.room'.format(target, start, roomNum), 'w') as file:
                for l in lines:
                    file.write(l)
                file.close()


c = Copier()
c.copy()
