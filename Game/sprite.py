import ast
import pygame

class Sprite:

    def __init__(self, path, x, y, c, a, s, scr):
        self.x = x
        self.y = y
        self.animated = a
        self.frameTick = a
        self.currentFrame = 0
        self.scale = s
        self.color = c
        self.screen = scr
        if path == 'null':
            self.frames = []
            self.pingRange = 0
            self.hitbox = []
        else:
            with open('Sprites\\' + path, 'r') as file:
                lines = file.readlines()
                lineCount = 0
                self.frames = []
                for line in lines:
                    if lineCount == 0:
                        self.pingRange = ast.literal_eval(line)
                        lineCount += 1
                    elif lineCount == 1:
                        self.hitbox = ast.literal_eval(line)
                        lineCount += 1
                    else:
                        self.frames.append(ast.literal_eval(line))

    def manualSprite(self, p, h, f):
        self.pingRange = p
        self.hitbox = h
        self.frames = f

    def updateSprite(self, path):
        with open(path, 'r') as file:
            lines = file.readlines()
            lineCount = 0
            self.frames = []
            for line in lines:
                if lineCount == 0:
                    self.pingRange = ast.literal_eval(line)
                    lineCount += 1
                elif lineCount == 1:
                    self.hitbox = ast.literal_eval(line)
                    lineCount += 1
                else:
                    self.frames.append(ast.literal_eval(line))

    def updateFrame(self, x):
        if 0 <= x < len(self.frames):
            self.currentFrame = x

    def updateColor(self, c):
        self.color = c

    def updatePos(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x += x
        self.y += y

    def draw(self):
        xRow = 0
        yRow = 0
        draw = True
        for i in self.frames[self.currentFrame]:
            if i == -1:
                yRow += 1
                xRow = 0
                draw = True
            elif draw == True:
                pygame.draw.rect(self.screen, self.color, (self.x + (xRow * self.scale), self.y + (yRow * self.scale), self.scale * i, self.scale))
                xRow += i
                draw = False
            else:
                xRow += i
                draw = True

    def update(self):
        if self.animated >= 0:
            if self.frameTick == 0:
                if self.currentFrame == len(self.frames) - 1:
                    self.currentFrame = 0
                else:
                    self.currentFrame += 1
                self.frameTick = self.animated
            else:
                self.frameTick -= 1
        self.draw()


# noinspection PyRedeclaration
class Text:
    global chars
    global blocks
    global dict
    global hitbox
    chars = []
    lineCount = 0
    dict = 'abcdefghijklmnopqrstuvwxyz 123456789.?!'
    with open('Sprites\\charList.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if lineCount == 0:
                blocks = ast.literal_eval(line)
                lineCount += 1
            elif lineCount == 1:
                hitbox = ast.literal_eval(line)
                lineCount += 1
            else:
                chars.append(ast.literal_eval(line))

    def __init__(self, t, x, y, c, s, scr):
        self.text = t.lower()
        self.x = x
        self.y = y
        self.sprites = []
        sprCount = 0
        xRow = 0
        yRow = 0
        for i in self.text:
            if i == '/':
                yRow += 1
                xRow = 0
            elif dict.find(i) > -1:
                self.sprites.append(Sprite('null', self.x + (blocks * xRow * s), self.y + 2 * yRow * s + (blocks * yRow * s), c, -1, s, scr))
                self.sprites[sprCount].manualSprite(blocks, hitbox, [chars[dict.find(i)]])
                xRow += 1
                sprCount += 1

    def update(self):
        for i in self.sprites:
            i.draw()
