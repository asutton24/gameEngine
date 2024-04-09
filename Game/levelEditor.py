import pygame
from sprite import *
from room import randLevel


def indexToChar(x):
    if x == 0:
        return 'S'
    if x == 1:
        return 'N'
    if x == 2:
        return 'U'
    return 'O'


def drawLevel(scr, lvl):
    for i in range(24):
        for j in range(24):
            temp = (0, 0, 0)
            if lvl[i][j] == 'S':
                temp = (255, 0, 0)
            elif lvl[i][j] == 'N':
                temp = (0, 0, 255)
            elif lvl[i][j] == 'U':
                temp = (0, 255, 0)
            else:
                temp = -1
            if temp != -1:
                pygame.draw.rect(scr, temp, (j * 15, i * 15, 15, 15))

def drawBG(scr):
    counter = 0
    for i in range(24):
        if i % 2 == 0:
            counter = 0
        else:
            counter = 1
        for j in range(24):
            if counter % 2 == 0:
                pygame.draw.rect(scr, (50, 50, 50), (j * 15, i * 15, 15, 15))
            else:
                pygame.draw.rect(scr, (70, 70, 70), (j * 15, i * 15, 15, 15))
            counter += 1


def main():
    running = True
    level = []
    count = 0
    index = 0
    oldIndex = 0
    screen = pygame.display.set_mode([360, 500])
    clock = pygame.time.Clock()
    isError = False
    error = Text('There can be only/1 starting room!', 10, 420, (255, 255, 255), 2, screen)
    preview = Text('Starting Room', 10, 370, (255, 0, 0), 2, screen)
    for i in range(24):
        level.append([])
        for j in range(24):
            level[count].append('O')
        count += 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    index += 1
                    if index > 2:
                        index = 0
                if event.key == pygame.K_LEFT:
                    index -= 1
                    if index < 0:
                        index = 2
                if event.key == pygame.K_r:
                    level = randLevel(10, .06, .4, .6, .25, 16, 4, 20)
                if event.key == pygame.K_s:
                    sCount = 0
                    uCount = 0
                    for i in level:
                        for j in i:
                            if j == 'S':
                                sCount += 1
                            elif j == 'U':
                                uCount += 1
                    if sCount != 1:
                        isError = True
                        error = Text('There can be only/1 starting room!', 10, 420, (255, 255, 255), 2, screen)
                    elif uCount < 2:
                        isError = True
                        error = Text('Must have at least/2 special rooms!', 10, 420, (255, 255, 255), 2, screen)
                    else:
                        isError = False
                    path = input('Enter file to save to: ')
                    with open('Levels\\' + path, 'a') as file:
                        lev = ''
                        for i in level:
                            for j in i:
                                lev += j
                        file.write(lev + '\n')
                        file.close()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if 0 <= mouse_x < 360:
            realX = int(mouse_x / 15)
        else:
            realX = -1
        if 0 <= mouse_y < 360:
            realY = int(mouse_y / 15)
        else:
            realY = -1
        if realX != -1 and realY != -1 and mouse_buttons[0]:
            level[realY][realX] = indexToChar(index)
        elif realX != -1 and realY != -1 and mouse_buttons[2]:
            level[realY][realX] = 'O'
        if oldIndex != index:
            oldIndex = index
            if index == 0:
                preview = Text('Starting Room', 10, 370, (255, 0, 0), 2, screen)
            elif index == 1:
                preview = Text('Normal Room', 10, 370, (0, 0, 255), 2, screen)
            elif index == 2:
                preview = Text('Special Room', 10, 370, (0, 255, 0), 2, screen)
        screen.fill((0, 0, 0))
        drawBG(screen)
        drawLevel(screen, level)
        preview.update()
        if isError:
            error.update()
        pygame.display.update()
        clock.tick(60)


main()
