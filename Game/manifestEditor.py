from gameObject import *
import ast

def main():
    inp = 'a'
    while inp != 't' and inp != 'e' and inp != 'i':
        inp = input('t To add a tile, e to add an enemy, or i to add an item: ')
    if inp == 'e':
        frames = int(input('How many sprites will there be?: '))
        if frames > 1:
            path = []
            for i in range(frames):
                path.append(input('Input sprite location within the Sprite folder: '))
        else:
            path = input('Input sprite location within the Sprite folder: ')
    else:
        path = input('Input sprite location within the Sprite folder: ')
    color = ast.literal_eval(input('Enter color tuple (x,y,z): '))
    animated = int(input('Enter frames between next frame for animated sprite (-1 for static): '))
    scale = int(input('Enter scale: '))
    if inp == 't':
        solid = eval(input('Is the tile solid (True/False): '))
        breakable = eval(input('Is the object breakable (T/F)? '))
        health = int(input('How much health does it have? '))
        purpose = input('Any special purpose for this tile (type Normal for none)? ')
        with open('Manifest\\TileManifest.txt', 'a') as file:
            file.write(str([path, color, animated, scale, solid, breakable, health, purpose]))
            file.write('\n')
    if inp == 'i':
        purpose = input('Any special purpose for this item (type Normal for none)? ')
        amount = int(input('Enter an amount associated with this item: '))
        boost = eval(input('Does this item provide a boost of any kind (T/F)? '))
        stack = eval(input('Is this item stackable?'))
        with open('Manifest\\ItemManifest.txt', 'a') as file:
            file.write(str([path, color, animated, scale, purpose, amount, boost, stack]))
            file.write('\n')
    if inp == 'e':
        faceType = int(input('What rotation sprites are there? 1 for single sprite, 2 for left/right, 3 for up/down 4 for all 4 directions: '))
        moveType = int(input('What movement type? 0 for stationary, 1 for chase, 2 for random, 3 for biased random, 4 for set path, 5 for point rotation, add 100 to make a solid enemy'))
        speed = int(input('Enemy speed?: '))
        if moveType == 2 or moveType == 3:
            moveLen = int(input('What is the average distanced covered before changing directions?'))
        elif moveType == 5:
            moveLen = int(input('How many frames between switching positions?'))
        else:
            moveLen = 0
        gho = eval(input('Is this a ghost? (True/False): '))
        health = int(input('Health?: '))
        drop = int(input('How much money is dropped?: '))
        damage = int(input('How much touch damage is done?: '))
        temp = input('Any projectiles? (y/n): ')
        proj = []
        if temp == 'y':
            proj.append(int(input('What attack type? 0-3 for single direction, 0 is upwards, rotates clockwise, 4 is direct aim, 5 is 4-way aim, 6 is 4-way random: ')))
            print('Create Projectile')
            projectile = []
            spr = []
            spr.append(input('Input sprite location within the Sprite folder: '))
            spr.append(ast.literal_eval(input('Enter color tuple (x,y,z): ')))
            spr.append(int(input('Enter frames between next frame for animated sprite (-1 for static): ')))
            spr.append(int(input('Enter scale: ')))
            projectile.append(spr)
            projectile.append(int(input('Enter projectile lifetime in frames: ')))
            projectile.append(int(input('Enter projectile speed: ')))
            projectile.append(int(input('Enter projectile damage: ')))
            projectile.append(eval(input('Is this projectile a ghost: ')))
            projectile.append(eval(input('Is this a player used projectile (T/F): ')))
            projectile.append(eval(input('Is this a piercing projectile (T/F): ')))
            projectile.append(int(input('How much knockback is done?: ')))
            projectile.append(int(input('How long is it applied?: ')))
            proj.append(projectile)
            proj.append(int(input('How many instances can be out at once?: ')))
            tempInp = float(input('Enter a decimal (0<=x<1) for a chance of a projectile launch per frame, enter a int (x>=1) for a set delay in frames:'))
            if tempInp >= 1:
                tempInp = int(tempInp)
            proj.append(tempInp)
        iFrames = int(input('How many invis frames does this enemy have?'))
        with open('Manifest\\EnemyManifest.txt', 'a') as file:
            file.write(str([path, color, animated, scale, faceType, moveType, speed, moveLen, gho, health, drop, damage, proj, iFrames]))
            file.write('\n')
    file.close()







main()