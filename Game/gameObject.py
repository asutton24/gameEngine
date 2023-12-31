import pygame
import random
from sprite import *

def sign(x):
    if x == 0:
        return 0
    if x > 0:
        return 1
    return -1


def rectCollide(x1, xlen1, y1, ylen1, x2, xlen2,  y2, ylen2, c):
    temp = (x1 <= x2 <= x1 + xlen1 or x1 <= x2 + xlen2 <= x1 + xlen1) and (y1 <= y2 <= y1 + ylen1 or y1 <= y2 + ylen2 <= y1 + ylen1)
    if c == 1:
        return temp
    elif not temp:
        return rectCollide(x2, xlen2, y2, ylen2, x1, xlen1, y1, ylen1, 1)
    else:
        return temp


class GameObject:

    def __init__(self, spr, sol, hel, gho, im):
        self.sprite = spr
        self.xVel = 0
        self.yVel = 0
        self.knockback = [0, 0, 0]
        self.solid = sol
        self.health = hel
        self.alive = True
        self.ghost = gho
        self.iFrames = 0
        self.iMax = im

    def setHealth(self, x):
        self.health = x
        if self.health <= 0:
            self.alive = False
        else:
            self.alive = True

    def damage(self, x):
        if self.alive and self.iFrames == 0:
            self.health -= x
            self.iFrames = self.iMax
            if self.health <= 0:
                self.alive = False

    def getPos(self):
        return self.sprite.getPos()

    def getCenter(self):
        temp = self.sprite.getPos()
        for i in range(2):
            temp[i] += self.sprite.getPing() * self.sprite.getScale()/2.0
        return temp

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
        self.health = 0

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

    def quickUpdate(self):
        if self.alive:
            self.move(self.xVel, self.yVel)
            self.sprite.update()

    def update(self, objs):
        if self.alive:
            if self.iFrames > 0:
                self.iFrames -= 1
            if self.knockback[2] != 0:
                xMove = self.knockback[0]
                yMove = self.knockback[1]
                self.knockback[2] -= 1
            else:
                xMove = self.xVel
                yMove = self.yVel
            self.move(xMove, 0)
            for i in objs:
                if i.solid and i.alive and self.collideWith(self, i):
                    self.move(-1 * xMove, 0)
            self.move(0, yMove)
            for i in objs:
                if i.solid and i.alive and not self.ghost and self.collideWith(self, i):
                    self.move(0, -1 * yMove)
            pos = self.getPos()
            if pos[0] < 0:
                self.updatePos(0, pos[1])
            elif pos[0] > 1024 - self.sprite.getScale() * self.sprite.getPing():
                self.updatePos(1024 - self.sprite.getScale() * self.sprite.getPing(), pos[1])
            if pos[1] < 0:
                self.updatePos(self.getPos()[0], 0)
            elif pos[1] > 576 - self.sprite.getScale() * self.sprite.getPing():
                self.updatePos(self.getPos()[0], 576 - self.sprite.getScale() * self.sprite.getPing())
            self.sprite.update()


class Player(GameObject):
    def __init__(self, x, y, scr):
        self.sprites = [Sprite('Player\\playerIdle.txt', x, y, (255,255,255), -1, 6, scr),
                        Sprite('Player\\playerMoveR.txt', x, y, (255,255,255), 3, 6, scr),
                        Sprite('Player\\playerMoveL.txt', x, y, (255,255,255), 3, 6, scr),
                        Sprite('Player\\playerMoveUD.txt', x, y, (255,255,255), 6, 6, scr)]
        self.facing = 1
        self.moving = False
        self.newSprite = False
        self.roomChange = 0
        self.attacking = False
        self.weapons = []
        GameObject.__init__(self, self.sprites[0], False, 100, False, 30)

    def takeInput(self, keys):
        currentFacing = self.facing
        currentMove = self.moving
        if keys[pygame.K_z]:
            self.attack()
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

    def getRoomChange(self):
        temp = self.roomChange
        self.roomChange = 0
        return temp

    def giveWeapon(self, x):
        self.weapons.append(x)

    def attack(self):
        x = self.getPos()[0]
        y = self.getPos()[1]
        for weapon in self.weapons:
            weapon.shoot(x, y, self.facing)


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
        for i in objs:
            if type(i) == Tile and self.collideWith(self, i):
                if i.getPurpose() == 'Up':
                    self.roomChange = 1
                elif i.getPurpose() == 'Right':
                    self.roomChange = 2
                elif i.getPurpose() == 'Down':
                    self.roomChange = 3
                elif i.getPurpose() == 'Left':
                    self.roomChange = 4
        for i in self.weapons:
            i.update(objs)
        GameObject.update(self, objs)

class Tile(GameObject):
    def __init__(self, spr, s, b, h, p):
        self.breakable = b
        self.purpose = p
        GameObject.__init__(self, spr, s, h, False, 0)

    def getPurpose(self):
        return self.purpose

    def breakTile(self):
        if self.breakable:
            self.alive = False
            return True
        return False

    def update(self):
        self.quickUpdate()

    def toString(self):
        return r"Tile(Sprite('{}', {}, {}, {}, {}, {}, {}), {}, {}, {}, '{}')".format(self.sprite.path, self.sprite.x, self.sprite.y, self.sprite.color, self.sprite.animated, self.sprite.scale, 'self.screen', self.solid, self.breakable, self.health, self.purpose)

class Item(GameObject):
    def __init__(self, spr, p, b, s):
        self.purpose = p
        self.boost = b
        self.stackable = s
        GameObject.__init__(self, spr, False, 1, False, 0)

    def getPurpose(self):
        return self.purpose

    def isBoost(self):
        return self.boost

    def update(self):
        self.quickUpdate()

    def toString(self):
        return r"Item(Sprite('{}', {}, {}, {}, {}, {}, {}), '{}', {}, {})".format(self.sprite.path, self.sprite.x,
                                                                                     self.sprite.y, self.sprite.color,
                                                                                     self.sprite.animated,
                                                                                     self.sprite.scale, 'self.screen',
                                                                                     self.purpose, self.boost,
                                                                                     self.stackable)

    def isStackable(self):
        return self.stackable

class Enemy(GameObject):
    def __init__(self, spr, faceType, moveType, speed, moveLen, gho, health, drop, damage, proj, points, im):
        if moveType == 4:
            self.points = points
            self.moving = False
            self.indexCount = 1
        self.mType = moveType
        self.speed = speed
        self.drop = drop
        self.hitDamage = damage
        self.fType = faceType
        self.currentDir = -1
        self.avgLen = moveLen
        self.isAttacking = False
        self.projectiles = []
        self.projStatus = []
        self.projectiles = []
        self.tickClock = 0
        if len(proj) == 4:
            self.attackType = proj[0]
            for i in range(proj[2]):
                self.projectiles.append(proj[1])
                self.projStatus.append(False)
            self.chance = proj[3]
        else:
            self.attackType = None
            self.chance = 0
        if self.mType == 4:
            im = 0
        if faceType == 1:
            self.sprites = 0
            self.facing = 0
            GameObject.__init__(self, spr, False, health, gho, im)
        else:
            self.sprites = spr
            GameObject.__init__(self, spr[0], False, health, gho, im)
            if faceType == 2:
                self.facing = 1
            if faceType == 3 or faceType == 4:
                self.facing = 2

    def attack(self, player):
        if not self.isAttacking and self.attackType is not None:
            projIndex = 0
            for i in self.projStatus:
                if not i:
                    self.projStatus[projIndex] = True
                    break
                projIndex += 1
            if projIndex >= len(self.projStatus):
                return
            selfPos = self.getCenter()
            playerPos = player.getCenter()
            xLen = playerPos[0] - selfPos[0]
            yLen = playerPos[1] - selfPos[1]
            if self.attackType == 4:
                xSign = sign(xLen)
                ySign = sign(yLen)
                xLen = abs(xLen)
                yLen = abs(yLen)
                normal = self.projectiles[projIndex].speed / ((xLen ** 2 + yLen ** 2) ** .5)
                xLen *= (normal * xSign)
                yLen *= (normal * ySign)
                self.projectiles[projIndex].manualShoot(selfPos[0], selfPos[1], xLen, yLen)
            elif self.attackType == 5:
                if abs(xLen) > abs(yLen):
                    if playerPos[0] > selfPos[0]:
                        self.projectiles[projIndex].shoot(selfPos[0], selfPos[1], 1)
                    else:
                        self.projectiles[projIndex].shoot(selfPos[0], selfPos[1], 3)
                else:
                    if playerPos[1] > selfPos[1]:
                        self.projectiles[projIndex].shoot(selfPos[0], selfPos[1], 2)
                    else:
                        self.projectiles[projIndex].shoot(selfPos[0], selfPos[1], 0)
            else:
                self.projectiles[projIndex].shoot(selfPos[0], selfPos[1], self.attackType)

    def changeFacing(self, x, y):
        # 0 is downward, increments clockwise
        pos = self.getPos()
        if x == -1 or self.fType == 1:
            return
        if x == self.facing:
            return
        if self.fType == 2:
            if x == 0 or x == 2:
                return self.changeFacing(y, -1)
            elif x == 1:
                self.changeSprite(self.sprites[0])
                self.updatePos(pos[0], pos[1])
            else:
                self.changeSprite(self.sprites[1])
                self.updatePos(pos[0], pos[1])
            self.facing = x
        if self.fType == 3:
            if x == 1 or x == 3:
                return self.changeFacing(y, -1)
            elif x == 2:
                self.changeSprite(self.sprites[0])
                self.updatePos(pos[0], pos[1])
            else:
                self.changeSprite(self.sprites[1])
                self.updatePos(pos[0], pos[1])
            self.facing = x
        elif self.fType == 4:
            self.changeSprite(self.sprites[(x+2) % 4])
            self.updatePos(pos[0], pos[1])
            self.facing = x

    def update(self, player, objs):
        # 0: Stationary 1: Chase 2: Random move
        faceDir = []
        if not self.alive:
            return
        if self.mType == 0:
            self.setKnockback(0, 0, 0)
            GameObject.update(self, [])
        elif self.mType == 1:
            self.setVel(0, 0)
            playerPos = player.getPos()
            selfPos = self.getPos()
            newVel = []
            if playerPos[0] > selfPos[0]:
                newVel.append(self.speed)
                faceDir.append(1)
            else:
                newVel.append(-1*self.speed)
                faceDir.append(3)
            if playerPos[1] > selfPos[1]:
                newVel.append(self.speed)
                faceDir.append(2)
            else:
                newVel.append(-1 * self.speed)
                faceDir.append(0)
            if abs(playerPos[0]-selfPos[0]) > abs(playerPos[1]-selfPos[1]):
                self.changeFacing(faceDir[0], faceDir[1])
            else:
                self.changeFacing(faceDir[1], faceDir[0])
            self.setVel(newVel[0], newVel[1])
            GameObject.update(self, objs)
        elif self.mType == 2 or self.mType == 3:
            if self.currentDir == -1:
                self.currentDir = random.randint(0,3)
            doChange = random.randint(0,int(self.avgLen/self.speed)-1)
            if doChange == 0:
                if self.mType == 3:
                    if self.getPos()[0] < player.getPos()[0]:
                        lrBias = 1
                    else:
                        lrBias = -1
                    if self.getPos()[1] < player.getPos()[1]:
                        udBias = -1
                    else:
                        udBias = 1
                    temp = random.randint(0, 7)
                    if temp < 4:
                        self.currentDir = temp
                    elif temp < 6:
                        if lrBias == 1:
                            self.currentDir = 1
                        else:
                            self.currentDir = 3
                    else:
                        if udBias == 1:
                            self.currentDir = 0
                        else:
                            self.currentDir = 2
                self.currentDir = random.randint(0, 3)
            if self.currentDir == 0:
                self.setVel(0, -1 * self.speed)
            elif self.currentDir == 1:
                self.setVel(self.speed, 0)
            elif self.currentDir == 2:
                self.setVel(0, self.speed)
            else:
                self.setVel(-1 * self.speed, 0)
            self.changeFacing(self.currentDir, -1)
            currentPos = self.getPos()
            GameObject.update(self, objs)
            if currentPos == self.getPos():
                self.currentDir = random.randint(0,3)
        elif self.mType == 4:
            changeDir = False
            if not self.moving:
                if self.getPos()[0] == self.points[self.indexCount][0]:
                    if self.getPos()[1] < self.points[self.indexCount][1]:
                        self.currentDir = 2
                    else:
                        self.currentDir = 0
                else:
                    if self.getPos()[0] < self.points[self.indexCount][0]:
                        self.currentDir = 1
                    else:
                        self.currentDir = 3
                self.changeFacing(self.currentDir, -1)
                self.moving = True
            if self.currentDir == 0:
                if self.getPos()[1] <= self.points[self.indexCount][1]:
                    changeDir = True
                else:
                    self.setVel(0, -1 * self.speed)
            elif self.currentDir == 1:
                if self.getPos()[0] >= self.points[self.indexCount][0]:
                    changeDir = True
                else:
                    self.setVel(self.speed, 0)
            elif self.currentDir == 2:
                if self.getPos()[1] >= self.points[self.indexCount][1]:
                    changeDir = True
                else:
                    self.setVel(0, self.speed)
            elif self.currentDir == 3:
                if self.getPos()[0] <= self.points[self.indexCount][0]:
                    changeDir = True
                else:
                    self.setVel(-1 * self.speed, 0)
            if changeDir:
                self.moving = False
                self.updatePos(self.points[self.indexCount][0], self.points[self.indexCount][1])
                self.setVel(0, 0)
                self.indexCount += 1
                if self.points[self.indexCount] == 0:
                    self.indexCount = 0
                elif self.points[self.indexCount] == 1:
                    self.points.reverse()
                    del self.points[0]
                    self.points.append(1)
                    self.indexCount = 1
            GameObject.update(self, objs)
        if self.chance < 1:
            if random.random() <= self.chance:
                self.attack(player)
        else:
            if self.tickClock >= self.chance:
                self.attack(player)
                self.tickClock = 0
            self.tickClock += 1
        counter = 0
        foundFalse = False
        for i in self.projStatus:
            if i:
                self.projectiles[counter].update(objs + [player])
                self.projStatus[counter] = self.projectiles[counter].isShooting
            if not i:
                foundFalse = True
            counter += 1
        if foundFalse:
            self.isAttacking = False
        else:
            self.isAttacking = True


class Projectile(GameObject):
    def __init__(self, spr, t, s, d, g, p, pi, k, kf):
        self.lifetime = t
        self.ticks = 0
        self.speed = s
        self.hitDamage = d
        self.isShooting = False
        self.isPlayer = p
        self.pierce = pi
        self.knockVal = k
        self.knockFrames = kf
        self.knock = [0, 0, 0]
        GameObject.__init__(self, spr, False, 1, g, 0)
        self.kill()


    def manualShoot(self, x, y, xs, ys):
        if not self.isShooting:
            self.isShooting = True
            self.setHealth(1)
            GameObject.updatePos(self, x, y)
            self.ticks = 0
            GameObject.setVel(self, xs, ys)
            self.knock = [self.knockVal * sign(xs), self.knockVal * sign(ys)]

    def shoot(self, x, y, dir):
        if not self.isShooting:
            self.isShooting = True
            self.setHealth(1)
            GameObject.updatePos(self, x, y)
            self.ticks = 0
            if dir == 0:
                GameObject.setVel(self, 0, -self.speed)
                self.knock = [0, -self.knockVal]
            elif dir == 1:
                GameObject.setVel(self, self.speed, 0)
                self.knock = [self.knockVal, 0]
            elif dir == 2:
                GameObject.setVel(self, 0, self.speed)
                self.knock = [0, self.knockVal]
            elif dir == 3:
                GameObject.setVel(self, -self.speed, 0)
                self.knock = [-self.knockVal, 0]

    def status(self):
        print('Am Shooting: {} Current tick: {} Alive: {}'.format(self.isShooting, self.ticks, self.alive))

    def update(self, objs):
        if self.isShooting:
            self.ticks += 1
            if self.ticks == self.lifetime:
                self.isShooting = False
                GameObject.setVel(self, 0, 0)
            if self.isShooting:
                for i in objs:
                    if self.isPlayer and type(i) == Enemy and self.collideWith(self, i):
                        i.damage(self.hitDamage)
                        i.setKnockback(self.knock[0], self.knock[1], self.knockFrames)
                        if not self.pierce:
                            self.kill()
                            self.isShooting = False
                    if not self.ghost and type(i) == Tile and self.collideWith(self, i):
                        if self.isPlayer and i.breakTile():
                            if not self.pierce:
                                self.kill()
                                self.isShooting = False
                        else:
                            self.kill()
                            self.isShooting = False
                    if not self.isPlayer and type(i) == Player and self.collideWith(self, i):
                        i.damage(self.hitDamage)
                        i.setKnockback(self.knock[0], self.knock[1], self.knockFrames)
                        self.isShooting = False
            self.quickUpdate()













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











