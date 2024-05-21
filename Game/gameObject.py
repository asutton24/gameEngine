import pygame
import random
from sprite import *


global itemPool
itemPool = [[['Items\\\\pmed.spr', (119, 252, 96), -1, 4, 'Heal', 25, False, True],
['Items\\\\medkit.spr', (119, 252, 96), -1, 8, 'Heal', 50, True, False],
['Items\\\\hpup.spr', (173, 2, 2), -1, 4, 'HealthB', 25, True, False],
['Items\\\\speedup.spr', (255, 180, 115), -1, 4, 'SpeedB', .5, True, False],
['Items\\\\rangeup.spr', (87, 9, 85), -1, 4, 'RangeB', 10, True, False],
['Items\\\\akimbo.spr', (100, 100, 100), -1, 4, 'ExtraShot', 1, True, False],
['Items\\\\armor.spr', (100, 100, 100), -1, 4, 'ArmorB', 15, True, False],
['Items\\\\sword.spr', (153, 0, 0), -1, 4, 'DamageB', 5, True, False],
['Items\\\\map.spr', (177, 2, 204), -1, 4, 'Map', 1, False, True],
['Items\\\\stitches.spr', (255, 255, 255), -1, 4, 'SlowDecay', 60, True, False],
['Items\\\\moneybag.spr', (153, 102, 0), -1, 4, 'Money', 150, False, False],
['Items\\\\bomb.spr', (100, 100, 100), -1, 4, 'Clear', 1, False, True]],
[['Items\\\\gun.spr', (0, 0, 128), -1, 4, 'SuperShot', 1, True, False],
['Items\\\\invis.spr', (255, 255, 255), -1, 4, 'TempInvis', 1, False, True],
['Items\\\\atomizer.spr', (102, 230, 255), 5, 4, 'PermClear', 1, False, True],
['Items\\\\nope.spr', (255, 0, 0), -1, 4, 'Skip', 1, False, False],
['Items\\\\hpup.spr', (255, 255, 51), -1, 4, 'HealthB', 60, True, False],
['Items\\\\moneybag.spr', (255, 238, 0), -1, 4, 'Money', 500, False, False],
['Items\\\\cannon.spr', (200, 200, 200), -1, 4, 'CannonShot', 1, True, False]]]


def randItem(pool, scr):
    item = itemPool[pool][random.randint(0, len(itemPool[pool]) - 1)]
    return Item(Sprite(item[0], 0, 0, item[1], item[2], item[3], scr), [item[4], item[5]], item[6], item[7])


def sign(x):
    if x == 0:
        return 0
    if x > 0:
        return 1
    return -1


def rectCollide(x1, xlen1, y1, ylen1, x2, xlen2, y2, ylen2, c):
    temp = (x1 <= x2 <= x1 + xlen1 or x1 <= x2 + xlen2 <= x1 + xlen1) and (
            y1 <= y2 <= y1 + ylen1 or y1 <= y2 + ylen2 <= y1 + ylen1)
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
        if self.alive and self.iFrames <= 0 and x > 0:
            self.health -= x
            self.iFrames = self.iMax
            if self.health <= 0:
                self.alive = False

    def getPos(self):
        return self.sprite.getPos()

    def getCenter(self):
        temp = self.sprite.getPos()
        for i in range(2):
            temp[i] += self.sprite.getPing() * self.sprite.getScale() / 2.0
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

    def revive(self):
        self.alive = True
        self.health = 1

    def changeSprite(self, x):
        self.sprite = x

    def setKnockback(self, x, y, z):
        if self.iFrames == self.iMax:
            self.knockback = [x, y, z]

    def collideWith(self, go2):
        if not self.alive or not go2.alive:
            return False
        if not (
                rectCollide(self.sprite.getPos()[0], self.sprite.getPing() * self.sprite.getScale(),
                            self.sprite.getPos()[1],
                            self.sprite.getPing() * self.sprite.getScale(), go2.sprite.getPos()[0],
                            go2.sprite.getPing() * go2.sprite.getScale(), go2.sprite.getPos()[1],
                            go2.sprite.getPing() * go2.sprite.getScale(), 0)):
            return False
        else:
            for i in self.sprite.getHitbox():
                for j in go2.sprite.getHitbox():
                    if rectCollide((i[0] * self.sprite.getScale()) + self.sprite.getPos()[0],
                                   (i[2] - i[0] + 1) * self.sprite.getScale(),
                                   (i[1] * self.sprite.getScale()) + self.sprite.getPos()[1],
                                   (i[3] - i[1] + 1) * self.sprite.getScale(),
                                   (j[0] * go2.sprite.getScale()) + go2.sprite.getPos()[0],
                                   (j[2] - j[0] + 1) * go2.sprite.getScale(),
                                   (j[1] * go2.sprite.getScale()) + go2.sprite.getPos()[1],
                                   (j[3] - j[1] + 1) * go2.sprite.getScale(), 0):
                        return True
        return False

    def quickUpdate(self):
        if self.alive:
            self.move(self.xVel, self.yVel)
            self.sprite.update()

    def isEqual(self, obj):
        return self.sprite.isEqual(
            obj.sprite) and self.solid == obj.solid and self.iMax == obj.iMax and self.ghost == obj.ghost

    def update(self, objs):
        if self.alive:
            if self.iFrames > 0 and self.iMax < 50:
                self.iFrames -= 1
                if int(self.iFrames / 5) % 2 == 0:
                    self.sprite.invis = True
                else:
                    self.sprite.invis = False
            else:
                self.sprite.invis = False
            if self.knockback[2] != 0:
                xMove = self.knockback[0]
                yMove = self.knockback[1]
                self.knockback[2] -= 1
            else:
                xMove = self.xVel
                yMove = self.yVel
            self.move(xMove, 0)
            for i in objs:
                if i.solid and i.alive and self.collideWith(i):
                    self.move(-1 * xMove, 0)
            self.move(0, yMove)
            for i in objs:
                if i.solid and i.alive and not self.ghost and self.collideWith(i):
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
        self.sprites = [Sprite('Player\\playerIdle.spr', x, y, (255, 255, 255), -1, 6, scr),
                        Sprite('Player\\playerMoveR.spr', x, y, (255, 255, 255), 3, 6, scr),
                        Sprite('Player\\playerMoveL.spr', x, y, (255, 255, 255), 3, 6, scr),
                        Sprite('Player\\playerMoveUD.spr', x, y, (255, 255, 255), 6, 6, scr)]
        self.facing = 1
        self.shootDir = 0
        self.moving = False
        self.newSprite = False
        self.roomChange = 0
        self.attacking = False
        self.weapons = []
        self.maxHealth = 100
        self.exitRoom = False
        self.gotoBoss = 0
        self.inventory = Inventory([], 0)
        self.currentRoom = [0, 0]
        self.map = [[0, 0]]
        self.rangeB = 0
        self.totalRB = 0
        self.damageB = 0
        self.totalDB = 0
        self.healB = 0
        self.speed = 3
        self.hold = [False, False, 0]
        self.wasd = False
        self.controller = False
        self.armor = 1
        self.itemTimer = 0
        self.currentItem = ''
        self.flags = [False, False, False]
        self.queue = []
        self.message = ''
        self.messageTimer = 0
        self.score = 0
        self.decay = 300
        self.decayMax = 300
        GameObject.__init__(self, self.sprites[0], False, 100, False, 30)

    def takeInput(self, keys):
        currentFacing = self.facing
        currentMove = self.moving
        if not self.wasd or self.controller:
            right = pygame.K_RIGHT
            left = pygame.K_LEFT
            up = pygame.K_UP
            down = pygame.K_DOWN
            fire = pygame.K_z
            use = pygame.K_x
            change = pygame.K_c
        else:
            right = pygame.K_d
            left = pygame.K_a
            up = pygame.K_w
            down = pygame.K_s
            fire = pygame.K_k
            use = pygame.K_l
            change = pygame.K_SEMICOLON
        if not keys[use]:
            self.hold[0] = False
        if not keys[change]:
            self.hold[1] = False
        if not keys[fire]:
            self.hold[2] = 0
        if not self.hold[0] and keys[use]:
            self.useItem(self.inventory.useItem())
            self.hold[0] = True
        if not self.hold[1] and keys[change]:
            self.inventory.inc()
            self.hold[1] = True
        if keys[fire] and self.hold[2] == 0:
            self.attack()
            self.hold[2] = 10
        if self.hold[2] > 0:
            self.hold[2] -= 1
        if (keys[right] and keys[left]) or (keys[up] and keys[down]):
            return
        horiMove = False
        if keys[right] and not keys[left]:
            self.xVel = self.speed
            if not currentMove or self.yVel == 0:
                self.facing = 1
            horiMove = True
            self.moving = True
        elif not keys[right] and keys[left]:
            self.xVel = -self.speed
            if not currentMove or self.yVel == 0:
                self.facing = 3
            horiMove = True
            self.moving = True
        else:
            self.xVel = 0
            horiMove = False
            self.moving = False
        if keys[up] and not keys[down]:
            if not horiMove:
                self.facing = 0
                self.moving = True
            self.yVel = -self.speed
        elif not keys[up] and keys[down]:
            if not horiMove:
                self.facing = 2
                self.moving = True
            self.yVel = self.speed
        else:
            self.yVel = 0
        if self.xVel != 0 and self.yVel != 0:
            self.xVel = sign(self.xVel) * ((self.xVel * self.xVel) / 2) ** 0.5
            self.yVel = sign(self.yVel) * ((self.yVel * self.yVel) / 2) ** 0.5
        if keys[up] and keys[right]:
            self.shootDir = 4
        elif keys[down] and keys[right]:
            self.shootDir = 5
        elif keys[down] and keys[left]:
            self.shootDir = 6
        elif keys[up] and keys[left]:
            self.shootDir = 7
        else:
            self.shootDir = self.facing
        if currentFacing != self.facing or currentMove != self.moving:
            self.newSprite = True

    def getRoomChange(self):
        temp = self.roomChange
        if temp > 0:
            self.setKnockback(0, 0, 0)
        self.roomChange = 0
        return temp

    def checkBoss(self):
        temp = self.gotoBoss
        self.gotoBoss = 0
        return temp

    def giveWeapon(self, x):
        x.hitDamage += self.totalDB
        x.lifetime += self.totalRB
        self.weapons.append(x)

    def useItem(self, item):
        if item == -1:
            return
        purpose = item.getPurpose()[0]
        amount = item.getPurpose()[1]
        if purpose == 'Heal':
            if self.health == self.maxHealth:
                self.inventory.addItem(item)
            else:
                self.health += amount
                if self.health > self.maxHealth:
                    self.health = self.maxHealth
        elif purpose == 'TempInvis':
            if self.itemTimer != 0:
                self.inventory.addItem(item)
            else:
                self.itemTimer = 750
                self.currentItem = purpose
        elif purpose == 'Map':
            self.flags[0] = True
        elif purpose == 'Skip':
            self.exitRoom = True
        elif purpose == 'Clear':
            self.flags[1] = True
        elif purpose == 'PermClear':
            self.flags[2] = True

    def damage(self, x):
        if self.currentItem != 'TempInvis':
            GameObject.damage(self, x * self.armor)

    def attack(self):
        if not self.alive:
            return
        x = self.getCenter()[0]
        y = self.getCenter()[1]
        if self.rangeB > 0 or self.damageB > 0:
            for weapon in self.weapons:
                weapon.lifetime += self.rangeB
                weapon.hitDamage += self.damageB
            self.rangeB = 0
            self.damageB = 0
        count = 0
        for weapon in self.weapons:
            if not weapon.isShooting:
                weapon.shoot(x, y, self.shootDir)
                self.weapons.append(self.weapons.pop(count))
                return
            count += 1

    def resetMap(self):
        self.map = [[0, 0]]
        self.currentRoom = [0, 0]

    def getFlags(self):
        temp = []
        count = 0
        for i in self.flags:
            temp.append(i)
            self.flags[count] = False
            count += 1
        return temp

    def drawMoneyCount(self, x, y, scr):
        msg = '${}'.format(self.inventory.money)
        t = Text(msg, x - ((len(msg)-2) * 16), y, (255, 255, 255), 2, scr)
        t.update()

    def drawCurrentItem(self, x, y, scr):
        pygame.draw.rect(scr, (255, 255, 255), (x, y, 94, 94))
        pygame.draw.rect(scr, (0, 0, 0), (x + 5, y + 5, 84, 84))
        item = self.inventory.peekItem()
        if item == -1:
            return
        item[0].updatePos(x+7, y+7)
        item[0].revive()
        item[0].update()
        t = Text('{}'.format(item[1]), x+72, y+72, (255, 255, 255), 2, scr)
        t.update()

    def drawIframes(self, x, y, scr):
        t = Text('{}'.format(self.iFrames), x, y, (255, 255, 255), 2, scr)
        t.update()

    def drawHealthBar(self, x, y, scr):
        pygame.draw.rect(scr, (255, 255, 255), [x, y, 200, 50])
        pygame.draw.rect(scr, (0, 0, 0), [x + 5, y + 5, 190, 40])
        pygame.draw.rect(scr, (255, 0, 0), [x + 5, y + 5, int(190 * self.health / self.maxHealth), 40])
        helString = "{}|{}".format(int(self.health + 0.5), self.maxHealth)
        if len(helString) % 2 == 1:
            start = 100 - 8 - 16 * int(len(helString) / 2)
        else:
            start = 100 - 16 * int(len(helString) / 2)
        t = Text(helString, x + start, y + 9, (255, 255, 255), 2, scr)
        t.update()

    def drawAutoMap(self, x, y, scr):
        pygame.draw.rect(scr, (255, 255, 255), [x, y, 110, 110])
        pygame.draw.rect(scr, (0, 0, 0), [x + 5, y + 5, 100, 100])
        for i in self.map:
            pygame.draw.rect(scr, (255, 255, 255), [(x + 5) + 4 * (i[0] + 12), (y + 5) + 4 * (12 - i[1]), 4, 4])
        pygame.draw.rect(scr, (255, 0, 0),
                         [(x + 5) + 4 * (self.currentRoom[0] + 12), (y + 5) + 4 * (12 - self.currentRoom[1]), 4, 4])

    def drawPos(self, x, y, scr):
        t = Text('{} {}'.format(int(self.getPos()[0]), int(self.getPos()[1])), x, y, (255, 255, 255), 2, scr)
        t.update()

    def drawMessage(self, x, y, scr):
        pygame.draw.rect(scr, (255, 255, 255), [x, y, 332, 28])
        pygame.draw.rect(scr, (0, 0, 0), [x + 5, y + 5, 322, 18])
        if self.message != '':
            t = Text(self.message, x+6, y+6, (255, 255, 255), 2, scr)
            t.update()

    def addMessage(self, m):
        self.queue.append(m)

    def flipWasd(self):
        self.wasd = not self.wasd

    def changeColor(self, c):
        for i in self.sprites:
            i.updateColor(c)

    def update(self, objs):
        if not self.alive:
            return
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
        self.move(self.xVel, self.yVel)
        locked = False
        changeDone = False
        for i in objs:
            if type(i) == Tile and self.collideWith(i):
                if i.getPurpose() == 'Up' and not locked and not changeDone and 436 <= self.getPos()[0] <= 540:
                    self.roomChange = 1
                    self.currentRoom[1] += 1
                    changeDone = True
                elif i.getPurpose() == 'Right' and not locked and 256 <= self.getPos()[1] <= 272:
                    self.roomChange = 2
                    self.currentRoom[0] += 1
                elif i.getPurpose() == 'Down' and not locked and not changeDone and 436 <= self.getPos()[0] <= 540:
                    self.roomChange = 3
                    self.currentRoom[1] -= 1
                    changeDone = True
                elif i.getPurpose() == 'Left' and not locked and 256 <= self.getPos()[1] <= 272:
                    self.roomChange = 4
                    self.currentRoom[0] -= 1
                elif i.getPurpose()[0:3] == 'Key':
                    if self.inventory.find(i.getPurpose()):
                        i.kill()
                        locked = False
                    else:
                        locked = True
                elif i.getPurpose() == 'Exit':
                    self.exitRoom = True
                    self.resetMap()
                elif i.getPurpose()[0:4] == 'Boss':
                    self.gotoBoss = int(i.getPurpose()[4:])
                if not (self.currentRoom in self.map):
                    self.map.append([self.currentRoom[0], self.currentRoom[1]])
            if Item == type(i) and self.collideWith(i):
                if len(i.getPurpose()[0]) > 6 and i.getPurpose()[0][0:6] == 'Random':
                    cost = int(i.getPurpose()[0][6:])
                    if self.inventory.money >= cost:
                        i.spawnNew()
                        self.inventory.money -= cost
                elif i.isBoost():
                    purpose = i.getPurpose()[0]
                    amount = i.getPurpose()[1]
                    if purpose == 'HealthB':
                        self.maxHealth += amount
                        self.health += amount
                        if self.health > self.maxHealth:
                            self.health = self.maxHealth
                        self.addMessage('health up')
                    elif purpose == 'SpeedB':
                        self.speed += amount
                        self.addMessage('speed up')
                    elif purpose == 'DamageB':
                        self.damageB = amount
                        self.totalDB += amount
                        self.addMessage('damage up')
                    elif purpose == 'RangeB':
                        self.rangeB = amount
                        self.totalRB += amount
                        self.addMessage('range up')
                    elif purpose == 'Heal':
                        self.health += amount
                        if self.health > self.maxHealth:
                            self.health = self.maxHealth
                        self.addMessage('health recovered')
                    elif purpose == 'ExtraShot':
                        self.giveWeapon(Projectile(Sprite('block.spr', 0, 0, (255, 0, 0), -1, 1, self.sprite.screen), 12, 10, 10, False, True, False, 5, 10))
                        self.addMessage('got an extra shot')
                    elif purpose == 'ArmorB':
                        if self.armor > .2:
                            self.armor -= amount * .01
                            if self.armor < .2:
                                self.armor = .2
                        self.addMessage('got armor')
                    elif purpose == 'SuperShot':
                        self.giveWeapon(Projectile(Sprite('block.spr', 0, 0, (0, 0, 255), -1, 1, self.sprite.screen), 60, 15, 20, False, True, False, 5, 10))
                        self.addMessage('got an extra shot')
                    elif purpose == 'SlowDecay':
                        self.decayMax += amount
                        self.addMessage('life retention up')
                    elif purpose == 'CannonShot':
                        self.giveWeapon(Projectile(Sprite('block.spr', 0, 0, (200, 200, 200), -1, 4, self.sprite.screen), 16, 8, 40, False, True, False, 10, 10))
                        self.addMessage('life retention up')
                    i.kill()
                else:
                    self.inventory.addItem(i)
                    i.kill()
        self.move(-self.xVel, -self.yVel)
        for i in self.weapons:
            i.update(objs)
            money = i.takeMoney()
            self.inventory.money += money
            self.score += money * 10
        if self.itemTimer > 0:
            self.itemTimer -= 1
            if self.currentItem == 'TempInvis' and not self.exitRoom:
                self.changeColor((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            if self.itemTimer == 0:
                self.changeColor((255, 255, 255))
                self.currentItem = ''
        if self.messageTimer > 0:
            self.messageTimer -= 1
        else:
            if self.message != '':
                self.message = ''
            if len(self.queue) != 0:
                self.message = self.queue.pop(0)
                self.messageTimer = 120
        if self.decay == 0:
            if self.health > 1:
                self.health -= 1
            self.decay = self.decayMax
        else:
            self.decay -= 1
        self.score += self.inventory.getScore() * 10
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

    def isEqual(self, tile):
        return self.purpose == tile.purpose and self.breakable == tile.breakable and GameObject.isEqual(self, tile)

    def update(self):
        self.quickUpdate()

    def toString(self):
        return r"Tile({}, {}, {}, {}, '{}')".format(self.sprite.toString(), self.solid, self.breakable, self.health,
                                                    self.purpose)


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
        return r"Item({}, {}, {}, {})".format(self.sprite.toString(),
                                              "['{}', {}]".format(self.purpose[0], self.purpose[1]), self.boost,
                                              self.stackable)

    def spawnNew(self):
        if self.purpose[0][0:6] == 'Random':
            num = int(self.purpose[1])
            self.move(64, 0)
            newItem = itemPool[num][random.randint(0, len(itemPool[num])-1)]
            self.sprite = Sprite(newItem[0], self.sprite.x, self.sprite.y, newItem[1], newItem[2], newItem[3], self.sprite.screen)
            self.purpose = [newItem[4], newItem[5]]
            self.boost = newItem[6]
            self.stackable = newItem[7]

    def isStackable(self):
        return self.stackable

    def sameItem(self, item):
        return self.purpose == item.purpose


class Enemy(GameObject):
    def __init__(self, spr, faceType, moveType, speed, moveLen, gho, health, drop, damage, proj, points, im):
        if moveType == 4 or moveType == 5:
            self.points = points
            self.moving = False
            self.indexCount = 1
            if moveType == 5:
                self.maxDelay = moveLen
            else:
                self.maxDelay = 0
        else:
            self.points = []
        self.mType = moveType
        makeSolid = False
        if self.mType >= 100:
            makeSolid = True
            self.mType -= 100
        self.speed = speed
        self.drop = drop
        self.hitDamage = damage
        self.fType = faceType
        self.currentDir = -1
        self.avgLen = moveLen
        self.isAttacking = False
        self.projStatus = []
        self.projectiles = []
        self.tickClock = 0
        self.maxHP = health
        if faceType == 1:
            self.sprites = spr
            self.facing = 0
            GameObject.__init__(self, spr, makeSolid, health, gho, im)
        else:
            if type(spr[1]) == str:
                self.sprites = []
                first = True
                for i in spr:
                    if first:
                        self.sprites.append(i)
                        first = False
                    else:
                        self.sprites.append(Sprite(i, 0, 0, spr[0].color, spr[0].animated, spr[0].scale, spr[0].screen))
            else:
                self.sprites = spr
            GameObject.__init__(self, spr[0], makeSolid, health, gho, im)
            if faceType == 2:
                self.facing = 1
            if faceType == 3 or faceType == 4:
                self.facing = 2
        if len(proj) == 4:
            if type(self.sprite) == list:
                self.screen = self.sprite[0].screen
            else:
                self.screen = self.sprite.screen
            self.attackType = proj[0]
            for i in range(proj[2]):
                self.projectiles.append(eval(proj[1].toString()))
                self.projStatus.append(False)
            self.chance = proj[3]
        else:
            self.attackType = None
            self.chance = 0
        self.solid = makeSolid

    def toString(self):
        if self.fType == 1:
            spr = self.sprites[0].toString()
        else:
            allSame = True
            for i in self.sprites:
                if self.sprites[0].color != i.color or self.sprites[0].animated != i.animated or self.sprites[0].scale != i.scale:
                    allSame = False
                    break
            if allSame:
                spr = '[{}, '.format(self.sprites[0].toString())
                for i in range(len(self.sprites) - 1):
                    spr += ("'{}'".format(self.sprites[i + 1].path))
                    if i != len(self.sprites) - 2:
                        spr += ', '
                    else:
                        spr += ']'
            else:
                spr = '['
                for i in range(len(self.sprites)):
                    spr += self.sprites[i].toString()
                    if i != len(self.sprites) - 1:
                        spr += ', '
                    else:
                        spr += ']'
        if len(self.projectiles) == 0:
            projStr = '[]'
        else:
            projStr = '[{}, {}, {}, {}]'.format(self.attackType, self.projectiles[0].toString(), len(self.projectiles),
                                                self.chance)

        return "Enemy({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(spr, self.fType, self.mType + self.solid * 100, self.speed,
                                                                              self.avgLen,
                                                                              self.ghost, self.health, self.drop,
                                                                              self.hitDamage, projStr, self.points,
                                                                              self.iMax)

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
            elif self.attackType == 6:
                self.projectiles[projIndex].shoot(selfPos[0], selfPos[1], random.randint(0, 3))
            elif self.attackType == 7:
                self.projectiles[projIndex].shoot(selfPos[0], selfPos[1], self.facing)
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
            self.changeSprite(self.sprites[(x + 2) % 4])
            self.updatePos(pos[0], pos[1])
            self.facing = x

    def revive(self):
        self.alive = True
        self.health = self.maxHP

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
                newVel.append(-1 * self.speed)
                faceDir.append(3)
            if playerPos[1] > selfPos[1]:
                newVel.append(self.speed)
                faceDir.append(2)
            else:
                newVel.append(-1 * self.speed)
                faceDir.append(0)
            if abs(playerPos[0] - selfPos[0]) > abs(playerPos[1] - selfPos[1]):
                self.changeFacing(faceDir[0], faceDir[1])
            else:
                self.changeFacing(faceDir[1], faceDir[0])
            self.setVel(newVel[0], newVel[1])
            GameObject.update(self, objs)
        elif self.mType == 2 or self.mType == 3:
            if self.currentDir == -1:
                self.currentDir = random.randint(0, 3)
            doChange = random.randint(0, int(self.avgLen / self.speed) - 1)
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
                    temp = random.randint(0, 11)
                    if temp < 4:
                        self.currentDir = temp
                    elif temp < 8:
                        if lrBias == 1:
                            self.currentDir = 1
                        else:
                            self.currentDir = 3
                    else:
                        if udBias == 1:
                            self.currentDir = 0
                        else:
                            self.currentDir = 2
                else:
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
                self.currentDir = random.randint(0, 3)
        elif self.mType == 4:
            changeDir = False
            self.setKnockback(0, 0, 0)
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
        elif self.mType == 5:
            self.setKnockback(0, 0, 0)
            if self.avgLen <= 0:
                pos = self.points[self.indexCount]
                self.updatePos(pos[0], pos[1])
                self.avgLen = self.maxDelay
                self.indexCount += 1
                if self.indexCount == len(self.points):
                    self.indexCount = 0
            else:
                self.avgLen -= 1
            GameObject.update(self, objs)
        if self.collideWith(player):
            player.damage(self.hitDamage)
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
        self.money = 0
        GameObject.__init__(self, spr, False, 1, g, 0)
        self.kill()

    def toString(self):
        return r'Projectile({}, {}, {}, {}, {}, {}, {}, {}, {})'.format(self.sprite.toString(), self.lifetime,
                                                                        self.speed, self.hitDamage, self.ghost,
                                                                        self.isPlayer, self.pierce, self.knockVal,
                                                                        self.knockFrames)

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
            dSpeed = 0
            dKnock = 0
            if dir > 3:
                dSpeed = (self.speed * self.speed / 2) ** .5
                dKnock = (self.knockVal * self.knockVal / 2) ** .5
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
            elif dir == 4:
                GameObject.setVel(self, dSpeed, -dSpeed)
                self.knock = [dKnock, -dKnock]
            elif dir == 5:
                GameObject.setVel(self, dSpeed, dSpeed)
                self.knock = [dKnock, dKnock]
            elif dir == 6:
                GameObject.setVel(self, -dSpeed, dSpeed)
                self.knock = [-dKnock, dKnock]
            elif dir == 7:
                GameObject.setVel(self, -dSpeed, -dSpeed)
                self.knock = [-dKnock, -dKnock]

    def status(self):
        print('Am Shooting: {} Current tick: {} Alive: {}'.format(self.isShooting, self.ticks, self.alive))

    def takeMoney(self):
        temp = self.money
        self.money = 0
        return temp

    def update(self, objs):
        if self.isShooting:
            self.ticks += 1
            if self.ticks == self.lifetime:
                self.isShooting = False
                GameObject.setVel(self, 0, 0)
            if self.isShooting:
                for i in objs:
                    if self.isPlayer and type(i) == Enemy and self.collideWith(i):
                        i.damage(self.hitDamage)
                        i.setKnockback(self.knock[0], self.knock[1], self.knockFrames)
                        if not self.pierce:
                            self.kill()
                            self.isShooting = False
                        if not i.alive:
                            self.money += i.drop
                    if not self.ghost and type(i) == Tile and self.collideWith(i):
                        if self.isPlayer and i.breakTile():
                            if not self.pierce:
                                self.kill()
                                self.isShooting = False
                        else:
                            self.kill()
                            self.isShooting = False
                    if not self.isPlayer and type(i) == Player and self.collideWith(i):
                        i.damage(self.hitDamage)
                        i.setKnockback(self.knock[0], self.knock[1], self.knockFrames)
                        self.isShooting = False
                    pos = self.getPos()
                    if pos[0] < 0 or pos[1] < 0 or pos[0] > 1024 or pos[1] > 576:
                        self.isShooting = False
            self.quickUpdate()


class Inventory:
    def __init__(self, items, m):
        self.inventory = items
        self.keys = []
        self.boosts = []
        self.money = m
        self.scoreToCollect = 0
        self.index = -1

    def addItem(self, item):
        if item.getPurpose()[0] == 'Money':
            self.money += item.getPurpose()[1]
            self.scoreToCollect += item.getPurpose()[1]
        elif item.getPurpose()[0][0:3] == 'Key':
            self.keys.append(item)
        elif item.isBoost():
            self.boosts.append(item)
        else:
            found = False
            for i in self.inventory:
                if i[0].sameItem(item):
                    found = True
                    if item.isStackable():
                        i[1] += 1
                        if i[1] > 9:
                            i[1] = 9
                    return
            if not found:
                self.inventory.append([item, 1])
            if self.index == -1:
                self.index = 0

    def findAndRemove(self, s):
        for i in self.inventory:
            if i[0].getPurpose() == s:
                i[1] -= 1
                if i[1] == 0:
                    del i
                return True
        return False

    def find(self, s):
        for i in self.inventory:
            if i[0].getPurpose()[0] == s:
                return True
        for i in self.keys:
            if i.getPurpose()[0] == s:
                return True
        return False

    def showItems(self):
        for i in self.inventory:
            print(i[0].toString())

    def inc(self):
        if len(self.inventory) == 0:
            self.index = -1
        else:
            self.index += 1
            if self.index == len(self.inventory):
                self.index = 0

    def useItem(self):
        if self.index == -1:
            return -1
        item = self.inventory[self.index][0]
        if self.inventory[self.index][1] == 1:
            self.inventory.pop(self.index)
            if self.index == len(self.inventory):
                self.index -= 1
        else:
            self.inventory[self.index][1] -= 1
        return item

    def getScore(self):
        temp = self.scoreToCollect
        self.scoreToCollect = 0
        return temp

    def peekItem(self):
        if self.index == -1:
            return -1
        return self.inventory[self.index]


class Spawner(GameObject):

    def __init__(self, spr, delay, enemy):
        GameObject.__init__(self, spr, False, 100000, False, 100000)
        self.setDelay = True
        if delay < 1:
            self.setDelay = False
        self.delay = delay
        self.timer = delay
        self.enemy = enemy
        self.spawnFlag = False

    def checkFlag(self):
        oldFlag = self.spawnFlag
        self.spawnFlag = False
        return oldFlag

    def getEnemy(self):
        return self.enemy

    def update(self, objs):
        GameObject.update(self, objs)
        if self.setDelay:
            if self.timer == 0:
                self.spawnFlag = True
                self.timer = self.delay
            else:
                self.timer -= 1
        else:
            if random.random() < self.delay:
                self.spawnFlag = True

