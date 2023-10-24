from gameObject import *
import ast

def main():
    inp = 'a'
    while inp != 't' and inp != 'e' and inp != 'i':
        inp = input('t To add a tile, e to add an enemy, or i to add an item: ')
    path = input('Input sprite location within the Sprite folder: ')
    color = ast.literal_eval(input('Enter color tuple (x,y,z): '))
    animated = int(input('Enter frames between next frame for animated sprite (-1 for static): '))
    scale = int(input('Enter scale: '))
    if inp == 't':
        solid = bool(input('Is the tile solid (True/False): '))
        breakable = bool(input('Is the object breakable (T/F)? '))
        health = int(input('How much health does it have? '))
        purpose = input('Any special purpose for this tile (type Normal for none)? ')
        roomC = input('Follow room Color (T/F)? ')
        with open('Manifest\\TileManifest.txt', 'w') as file:
            file.write(str([path, color, animated, scale, solid, breakable, health, purpose, roomC]))
    if inp == 'i':
        purpose = input('Any special purpose for this item (type Normal for none)? ')
        amount = int(input('Enter an amount associated with this item: '))
        boost = bool(input('Does this item provide a boost of any kind (T/F)? '))
        iType = input('What type of item is it? ')
        stack = bool(input('Is this item stackable?'))
        with open('Manifest\\ItemManifest.txt', 'w') as file:
            file.write(str([path, color, animated, scale, purpose, amount, boost, iType, stack]))


main()