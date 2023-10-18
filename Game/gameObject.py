from sprite import *

def rectCollide(x1, xlen1, y1, ylen1, x2, xlen2,  y2, ylen2):
    return (x1 <= x2 <= x1 + xlen1 or x1 <= x2 + xlen2 <= x1 + xlen1) and (y1 <= y2 <= y1 + ylen1 or y1 <= y2 + ylen2 <= y1 + ylen1)

class GameObject:

    def __init__(self,spr, sol, hel, gho):
        self.sprite = spr
        self.xVel = 0
        self.yVel = 0
        self.knockback = [0, 0, 0]
        self.solid = sol
        self.health = hel
        self.ghost = True
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

    def collideWith(self, go):
        if not (rectCollide(self.sprite.getPos()[0], self.sprite.getPing(), self.sprite.getPos()[1], self.sprite.getPing(), go.sprite.getPos()[0], go.sprite.getPing(), go.sprite.getPos()[1], go.sprite.getPing())):
            return False
        else:
            hb1 = self.sprite.getHitbox()
            hb2 = go.sprite.getHitbox()
            for i in hb1:
                for j in hb2:
                    if rectCollide(i[0], i[2] - i[0], i[1], i[3] - i[1], j[0], j[2] - j[0], j[1], j[3] - j[1]):
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
                if i.solid and (not self.ghost) and self.collideWith(i):
                    self.move(-1 * xMove, -1 * yMove)
            self.sprite.draw()


