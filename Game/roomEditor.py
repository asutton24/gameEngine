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
    with open('Manifest\\TileManifest.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            tiles.append(ast.literal_eval(line))
    for i in range(9):
        board.append([])
        for j in range(16):
            board[i].append([])
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if index != len(tiles) - 1:
                        index += 1
                elif event.key == pygame.K_LEFT:
                    if index != 0:
                        index -= 1
                elif event.key == pygame.K_t:
                    mode = 't'
        screen.fill((0,0,0))
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
        elif mouse_buttons[0]:
            if mode == 't':
                board[realY][realX].append(['t', index, Sprite(tiles[index][0], realX * 64, realY * 64, tiles[index][1], tiles[index][2], tiles[index][3], screen)])
        for i in board:
            for j in i:
                for k in j:
                    k[2].update()
        if mode == 't':
            modeDisp = Text('Tiles', 960+64, 512-64, (255, 255, 255), 2, screen)
            sampleSprite = Sprite(tiles[index][0], 17 * 64, 8 * 64, tiles[index][1], tiles[index][2], tiles[index][3], screen)
        if mode == 'i':
            modeDisp = Text('Items', 960+64, 512-64, (255, 255, 255), 2, screen)
        if mode == 'e':
            modeDisp = Text('Enemies', 960 + 64, 512 - 64, (255, 255, 255), 2, screen)
        sampleSprite.update()
        modeDisp.update()
        pygame.display.update()

main()