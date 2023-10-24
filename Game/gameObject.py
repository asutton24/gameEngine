import pygame

from sprite import *

def rectCollide(x1, xlen1, y1, ylen1, x2, xlen2,  y2, ylen2, c):
    temp = (x1 <= x2 <= x1 + xlen1 or x1 <= x2 + xlen2 <= x1 + xlen1) and (y1 <= y2 <= y1 + ylen1 or y1 <= y2 + ylen2 <= y1 + ylen1)
    if c == 1:
        return temp
    elif not temp:
        return rectCollide(x2, xlen2, y2, ylen2, x1, xlen1, y1, ylen1, 1)
    else:
        return temp
class GameObject:

    def __init__(self,spr, sol, hel):
        self.sprite = spr
        self.xVel = 0
        self.yVel = 0
        self.knockback = [0, 0, 0]
        self.solid = sol
        self.health = hel
        self.alive = True

    def setHealth(self, x):
        self.health = x
        if self.health <= 0:
            self.alive = False

    def changeHealth(self, x):
        self.health += x
        if self.health <= 0:
            self.alive = False

    def updatePos(self, x, y):
        self.sprite.updatePos(x, y)

    def move(self, x, y):
        self.sprite.move(x, y)

    def setVel(self, x, y):
        self.xVel = x
        self.yVel = y

    def changeVel(self, x, y):
        self.xVel += x
        self.yVel += y

    def kill(self):
        self.alive = False

    def changeSprite(self, x):
        self.sprite = x

    def setKnockback(self, x, y, z):
        self.knockback = [x, y, z]

    def collideWith(self, go1, go2):
        if not (rectCollide(go1.sprite.getPos()[0], go1.sprite.getPing() * go1.sprite.getScale(), go1.sprite.getPos()[1], go1.sprite.getPing() * go1.sprite.getScale(), go2.sprite.getPos()[0], go2.sprite.getPing() * go2.sprite.getScale(), go2.sprite.getPos()[1], go2.sprite.getPing() * go2.sprite.getScale(), 0)):
            return False
        else:
            for i in go1.sprite.getHitbox():
                for j in go2.sprite.getHitbox():
                    if rectCollide((i[0] * go1.sprite.getScale()) + go1.sprite.getPos()[0], (i[2] - i[0] + 1) * go1.sprite.getScale(), (i[1] * go1.sprite.getScale()) + go1.sprite.getPos()[1], (i[3] - i[1] + 1) * go1.sprite.getScale(), (j[0] * go2.sprite.getScale()) + go2.sprite.getPos()[0], (j[2] - j[0] + 1) * go2.sprite.getScale(), (j[1] * go2.sprite.getScale()) + go2.sprite.getPos()[1], (j[3] - j[1] + 1) * go2.sprite.getScale(), 0):
                        return True
        return False

    def update(self, objs):
        if self.alive:
            if self.knockback[2] != 0:
                xMove = self.knockback[0]
                yMove = self.knockback[1]
                self.knockback[2] -= 1
            else:
                xMove = self.xVel
                yMove = self.yVel
            self.move(xMove, yMove)
            for i in objs:
                if i.solid and self.collideWith(self, i):
                    self.move(-1 * xMove, -1 * yMove)
            self.sprite.update()


class Player(GameObject):
    def __init__(self, x, y, scr):
        self.sprites = [Sprite('Player\\playerIdle.txt', x, y, (255,255,255), -1, 4, scr),
                        Sprite('Player\\playerMoveR.txt', x, y, (255,255,255), 3, 4, scr),
                        Sprite('Player\\playerMoveL.txt', x, y, (255,255,255), 3, 4, scr),
                        Sprite('Player\\playerMoveUD.txt', x, y, (255,255,255), 6, 4, scr)]
        self.facing = 1
        self.moving = False
        self.newSprite = False
        GameObject.__init__(self, self.sprites[0], False, 100)

    def takeInput(self, keys):
        currentFacing = self.facing
        currentMove = self.moving
        if (keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]) or (keys[pygame.K_UP] and keys[pygame.K_DOWN]):
            return
        horiMove = False
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.xVel = 3
            if not currentMove or self.yVel == 0:
                self.facing = 1
            horiMove = True
            self.moving = True
        elif not keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
            self.xVel = -3
            if not currentMove or self.yVel == 0:
                self.facing = 3
            horiMove = True
            self.moving = True
        else:
            self.xVel = 0
            horiMove = False
            self.moving = False
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            if not horiMove:
                self.facing = 0
                self.moving = True
            self.yVel = -3
        elif not keys[pygame.K_UP] and keys[pygame.K_DOWN]:
            if not horiMove:
                self.facing = 2
                self.moving = True
            self.yVel = 3
        else:
            self.yVel = 0
        if currentFacing != self.facing or currentMove != self.moving:
            self.newSprite = True

    def update(self, objs):
        if self.newSprite:
            pos = self.sprite.getPos()
            if self.moving:
                if self.facing == 0 or self.facing == 2:
                    self.changeSprite(self.sprites[3])
                elif self.facing == 1:
                    self.changeSprite(self.sprites[1])
                else:
                    self.changeSprite(self.sprites[2])
            else:
                if self.facing == 0 or self.facing == 2:
                    self.changeSprite(self.sprites[0])
                    self.sprite.updateFrame(2)
                elif self.facing == 1:
                    self.changeSprite(self.sprites[0])
                    self.sprite.updateFrame(0)
                else:
                    self.changeSprite(self.sprites[0])
                    self.sprite.updateFrame(1)
            self.sprite.updatePos(pos[0], pos[1])
            self.newSprite = False
        GameObject.update(self, objs)

class Tile(GameObject):
    def __init__(self, spr, s, b, h, p, c):
        self.breakable = b
        self.purpose = p
        self.roomColor = c
        GameObject.__init__(self, spr, s, h)

    def getPurpose(self):
        return self.purpose

    def breakTile(self):
        if self.breakable:
            self.alive = False

    def update(self):
        GameObject.update(self, [])

    def toString(self):
        return "Tile(Sprite({}, {}, {}, {}, {}, {}, {}), {}, {}, {}, {}, {})".format(self.sprite.path, self.sprite.x, self.sprite.y, self.sprite.color, self.sprite.animated, self.sprite.scale, 'self.screen', self.solid, self.breakable, self.health, self.purpose, self.roomColor)

class Item(GameObject):
    def __init__(self, spr, p, b, t, s):
        self.purpose = p
        self.boost = b
        self.type = t
        self.stackable = s
        GameObject.__init__(spr, False, 1)

    def getPurpose(self):
        return self.purpose

    def isBoost(self):
        return self.boost

    def getType(self):
        return self.type

    def isStackable(self):
        return self.stackable

class Inventory:
    def __init__(self, items, m, s):
        self.inventory = items
        self.boosts = []
        self.money = m
        self.secondary = s

    def addItem(self, item):
        if item.getPurpose()[0] == 'Money':
            self.money += item.getPurpose[1]
        elif item.isBoost():
            self.boosts.append(item)
        else:
            for i in self.inventory:
                if i[0] == item:
                    if item.isStackable():
                        i[1] += 1
                    return
            self.inventory.append([item, 1])










