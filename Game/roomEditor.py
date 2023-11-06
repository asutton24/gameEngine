import math
import pygame
from gameObject import *
from sprite import Text

def drawBG(scr):
    counter = 0
    for i in range(9):
        if i % 2 == 0:
            counter = 0
        else:
            counter = 1
        for j in range(16):
            if counter % 2 == 0:
                pygame.draw.rect(scr, (50, 50, 50), (j * 64, i * 64, 64, 64))
            else:
                pygame.draw.rect(scr, (70, 70, 70), (j * 64, i * 64, 64, 64))
            counter += 1

def main():
    pygame.init()
    running = True
    screen = pygame.display.set_mode([1152, 576])
    tiles = []
    enemies = []
    items = []
    board = []
    mode = 't'
    index = 0
    realX = 0
    realY = 0
    new = True
    with open('Manifest\\TileManifest.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            tiles.append(ast.literal_eval(line))
    with open('Manifest\\ItemManifest.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            items.append(ast.literal_eval(line))
    for i in range(9):
        board.append([])
        for j in range(16):
            board[i].append([])
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mode == 't':
                        board[realY][realX].append(['t', index, Sprite(tiles[index][0], realX * 64, realY * 64, tiles[index][1], tiles[index][2], tiles[index][3], screen)])
                    if mode == 'i':
                        board[realY][realX].append(['i', index, Sprite(items[index][0], realX * 64, realY * 64, items[index][1], items[index][2], items[index][3], screen)])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if index != len(tiles) - 1:
                        index += 1
                elif event.key == pygame.K_LEFT:
                    if index != 0:
                        index -= 1
                elif event.key == pygame.K_t:
                    mode = 't'
                    index = 0
                elif event.key == pygame.K_i:
                    mode = 'i'
                    index = 0
                elif event.key == pygame.K_e:
                    if mode == 't':
                        for i in range(16):
                            board[0][i].append(['t', index, Sprite(tiles[index][0], i * 64, 0, tiles[index][1], tiles[index][2], tiles[index][3], screen)])
                            board[8][i].append(['t', index, Sprite(tiles[index][0], i * 64, 512, tiles[index][1], tiles[index][2], tiles[index][3], screen)])
                        for i in range(7):
                            board[i+1][0].append(['t', index, Sprite(tiles[index][0], 0, (i+1) * 64, tiles[index][1], tiles[index][2], tiles[index][3], screen)])
                            board[i + 1][0].append(['t', index, Sprite(tiles[index][0], 960, (i + 1) * 64, tiles[index][1], tiles[index][2], tiles[index][3], screen)])
                elif event.key == pygame.K_s:
                    saveTiles = '['
                    saveItems = '['
                    saveEnemies = '['
                    for i in board:
                        for j in i:
                            for k in j:
                                if k[0] == 't':
                                    temp = Tile(k[2], tiles[k[1]][4],tiles[k[1]][5], tiles[k[1]][6], tiles[k[1]][7])
                                    saveTiles += temp.toString() + ', '
                                if k[0] == 'i':
                                    temp = Item(k[2], [items[k[1]][4], items[k[1]][5]], items[k[1]][6], items[k[1]][7])
                                    saveItems += temp.toString() + ', '
                    if len(saveTiles)>2:
                        saveTiles = saveTiles[0: len(saveTiles) - 2]
                    saveTiles += ']'
                    if len(saveItems)>2:
                        saveItems = saveItems[0: len(saveItems) - 2]
                    saveItems += ']'
                    if new:
                        with open('Manifest\\RoomManifest.txt', 'w') as file:
                            temp = (saveTiles+', '+saveItems)
                            file.write(temp)

        screen.fill((0, 0, 0))
        drawBG(screen)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_x > 1023:
            mouse_x = 1023
        elif mouse_x < 0:
            mouse_x = 0
        if mouse_y > 575:
            mouse_y = 575
        elif mouse_y < 0:
            mouse_y = 0
        realX = math.floor(mouse_x / 64)
        realY = math.floor(mouse_y / 64)
        if mouse_buttons[2]:
            board[realY][realX] = []
        for i in board:
            for j in i:
                for k in j:
                    k[2].update()
        if mode == 't':
            modeDisp = Text('Tiles', 1024, 448, (255, 255, 255), 2, screen)
            sampleSprite = Sprite(tiles[index][0], 1088, 512, tiles[index][1], tiles[index][2], tiles[index][3], screen)
        if mode == 'i':
            modeDisp = Text('Items', 1024, 448, (255, 255, 255), 2, screen)
            sampleSprite = Sprite(items[index][0], 1088, 512, items[index][1], items[index][2], items[index][3], screen)
        if mode == 'e':
            modeDisp = Text('Enemies', 1024, 448, (255, 255, 255), 2, screen)
        sampleSprite.update()
        modeDisp.update()
        pygame.display.update()

main()