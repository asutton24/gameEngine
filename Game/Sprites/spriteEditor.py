import ast
import math
import pygame

def drawHitbox(hit, scr, blocks):
    size = 512 / blocks
    for i in hit:
        pygame.draw.rect(scr, (255, 0, 0), (i[0] * size, i[1] * size, (i[2]-i[0]) * size, size))
        pygame.draw.rect(scr, (255, 0, 0), (i[0] * size, i[3] * size, (i[2] - i[0] + 1) * size, size))
        pygame.draw.rect(scr, (255, 0, 0), (i[0] * size, i[1] * size, size, (i[3] - i[1]) * size))
        pygame.draw.rect(scr, (255, 0, 0), (i[2] * size, i[1] * size, size, (i[3] - i[1]) * size))

def collapse(grid):
    blocks = len(grid)
    rowCount = 0
    stop = False
    for i in range(blocks):
        for j in range(blocks):
            if grid[j][i]:
                stop = True
                break
        if stop:
            break
        rowCount += 1
    if rowCount > 0:
        for i in range(rowCount, blocks):
            for j in range(blocks):
                grid[j][i-rowCount] = grid[j][i]
                grid[j][i] = False
    rowCount = 0
    stop = False
    for i in range(blocks):
        for j in range(blocks):
            if grid[i][j]:
                stop = True
                break
        if stop:
            break
        rowCount += 1
    if rowCount > 0:
        for i in range(rowCount, blocks):
            for j in range(blocks):
                grid[i - rowCount][j] = grid[i][j]
                grid[i][j] = False
    return grid

def newBoard(size):
    result = []
    for i in range(size):
        result.append([])
        for j in range(size):
            result[i].append(False)
    return result

def openSprite(spr, size):
    result = newBoard(size)
    draw = True
    xCounter = 0
    yCounter = 0
    for i in spr:
        if i == -1:
            yCounter += 1
            xCounter = 0
            draw = True
        elif draw:
            for j in range(i):
                result[yCounter][xCounter] = True
                xCounter += 1
            draw = False
        elif not draw:
            xCounter += i
            draw = True
    return result


def translate(grid):
    counter = 0
    result = []
    draw = True
    for i in grid:
        for j in i:
            if j and draw:
                counter += 1
            elif not j and draw:
                result.append(counter)
                counter = 1
                draw = False
            elif not j and not draw:
                counter += 1
            elif j and not draw:
                result.append(counter)
                counter = 1
                draw = True
        if draw and counter > 0:
            result.append(counter)
        result.append(-1)
        draw = True
        counter = 0
    return result


def drawBoard(scr, b, blocks):
    for i in range(blocks):
        for j in range(blocks):
            if b[i][j]:
                pygame.draw.rect(scr, (0, 0, 0), (int(j * (512/blocks)), int(i * (512/blocks)), int(512/blocks), int(512/blocks)))
def drawBG(scr, num):
    num = (2 ** (num - 1))
    l = 512 / num
    tick = 0
    col = (125, 125, 125)
    for i in range(num):
        for j in range(num):
            pygame.draw.rect(scr, col, (j * l, i * l, l, l))
            if tick == 0:
                col = (150, 150, 150)
                tick = 1
            else:
                col = (125, 125, 125)
                tick = 0
        if tick == 0:
            col = (150, 150, 150)
            tick = 1
        else:
            col = (125, 125, 125)
            tick = 0



def main():
    print('Sprite Editor Controls:\nSetup Controls:\nLeft/right arrows: Change board size\nEnter: Start editing\nEditing controls:\nSpace: Change mode (Drawing/Hitbox)\nLeft/right arrows: Change frame\nUp/down arrows: Change pen size\nT: align to top left\nC: Copy frame\nP: Paste frame\nBackspace: Delete frame\nI: Print frame information to console\nF: Flip current frame\nS: Save Frame (Must enter file name into terminal if it is a new file)\nR: Reset save directory\nLeft Mouse: Draw (in draw mode)/Place hitbox coordinate (hitbox mode, must be top left and bottom right coordinate)\nRight mouse: Erase (in draw mode)')
    running = True
    startup = True
    reset = False
    num = 3
    frames = []
    currentFrame = 0
    finalFrame = 0
    board = []
    copied = []
    hitbox = []
    tempbox = []
    blocks = 0
    inp = 'a'
    path = 'noPath'
    while inp != 'y' and inp != 'n':
        inp = input('Open existing sprite? (y/n) ')
    if inp == 'y':
        path = input('Enter file name and sub-directory: ')
        with open(path, 'r') as file:
            lines = file.readlines()
            lineCount = 0
            for line in lines:
                if lineCount == 0:
                    blocks = ast.literal_eval(line)
                    lineCount += 1
                elif lineCount == 1:
                    hitbox = ast.literal_eval(line)
                    lineCount += 1
                else:
                    frames.append(ast.literal_eval(line))
            finalFrame = len(frames) - 1
            board = openSprite(frames[0], blocks)
            num = int(math.log2(blocks) + 1)
            startup = False
            file.close()
    pygame.init()
    screen = pygame.display.set_mode([512, 512])
    pygame.display.set_caption('Sprite Editor')
    hitCount = 0
    realX = 0
    realY = 0
    penSize = 1
    mode = 'draw'
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and mode == 'hitbox' and not startup:
                if event.button == 1:
                    if hitCount == 0 or hitCount == 1:
                        tempbox.append(realX)
                        tempbox.append(realY)
                        hitCount += 1
                    if hitCount == 2:
                        hitCount = 0
                        if tempbox[2] >= tempbox[0] and tempbox[3] >= tempbox[1]:
                            hitbox.append(tuple(tempbox))
                        tempbox = []
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and startup:
                    num += 1
                if event.key == pygame.K_RIGHT and not startup:
                    if currentFrame == finalFrame:
                        if len(frames) - 1 == currentFrame:
                            frames[currentFrame] = translate(board)
                        else:
                            frames.append(translate(board))
                        currentFrame += 1
                        finalFrame += 1
                        board = newBoard(blocks)
                    else:
                        frames[currentFrame] = translate(board)
                        currentFrame += 1
                        board = openSprite(frames[currentFrame], blocks)
                if event.key == pygame.K_LEFT and startup:
                    if num > 1:
                        num -= 1
                if event.key == pygame.K_LEFT and not startup and currentFrame > 0:
                    if currentFrame == finalFrame:
                        if len(frames) - 1 == currentFrame:
                            frames[currentFrame] = translate(board)
                        else:
                            frames.append(translate(board))
                    else:
                        frames[currentFrame] = translate(board)
                    currentFrame -= 1
                    board = openSprite(frames[currentFrame], blocks)
                if event.key == pygame.K_UP and not startup:
                    penSize += 1
                if event.key == pygame.K_DOWN and not startup:
                    if penSize > 0:
                        penSize -= 1
                if event.key == pygame.K_RETURN and startup:
                    startup = False
                    blocks = 2 ** (num - 1)
                    board = newBoard(blocks)
                if event.key == pygame.K_t and not startup:
                    board = collapse(board)
                if event.key == pygame.K_c and not startup:
                    copied = translate(board)
                if event.key == pygame.K_p and not startup:
                    board = openSprite(copied, blocks)
                if event.key == pygame.K_d and not startup:
                    hitbox = []
                if event.key == pygame.K_i and not startup:
                    print('Frame: {}/{}\nPen Size: {}'.format(currentFrame + 1, finalFrame + 1, penSize))
                if event.key == pygame.K_f and not startup:
                    for i in board:
                        i.reverse()
                if event.key == pygame.K_r and not startup:
                    if path != 'noPath':
                        path = 'noPath'
                        reset = True
                if (event.key == pygame.K_s and not startup) or reset:
                    if len(frames) == currentFrame and currentFrame == finalFrame:
                        frames.append(translate(board))
                    else:
                        frames[currentFrame] = translate(board)
                    if path == 'noPath':
                        path = input('Enter file name to save to: ')
                    with open(path, 'w') as file:
                        pass
                    with open(path, 'w') as file:
                        file.write('{}\n{}'.format(blocks, hitbox))
                        for i in frames:
                            file.write('\n{}'.format(i))
                        file.close()
                    print('Saved')
                    reset = False
                if event.key == pygame.K_SPACE and not startup:
                    if mode == 'draw':
                        mode = 'hitbox'
                    elif mode == 'hitbox':
                        tempbox = []
                        hitCount = 0
                        mode = 'draw'
                if event.key == pygame.K_BACKSPACE and not startup:
                    if currentFrame == finalFrame:
                        if currentFrame == 0:
                            board = newBoard(blocks)
                        else:
                            if currentFrame != len(frames):
                                del frames[currentFrame]
                            currentFrame -= 1
                            finalFrame -= 1
                            board = openSprite(frames[currentFrame], blocks)
                    else:
                        del frames[currentFrame]
                        finalFrame -= 1
                        board = openSprite(frames[currentFrame], blocks)
        screen.fill((0, 0, 0))
        drawBG(screen, num)
        if not startup:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_x > 511:
                mouse_x = 511
            elif mouse_x < 0:
                mouse_x = 0
            if mouse_y > 511:
                mouse_y = 511
            elif mouse_y < 0:
                mouse_y = 0
            realX = int(mouse_x / (512 / blocks))
            realY = int(mouse_y / (512 / blocks))
            if mouse_buttons[0] and mode == 'draw':
                for i in range(penSize):
                    for j in range(penSize):
                        if realX + j < blocks and realY + i < blocks:
                            board[realY + i][realX + j] = True
            elif mouse_buttons[2] and mode == 'draw':
                for i in range(penSize):
                    for j in range(penSize):
                        if realX + j < blocks and realY + i < blocks:
                            board[realY + i][realX + j] = False
        drawBoard(screen, board, blocks)
        if mode == 'hitbox':
            drawHitbox(hitbox, screen, blocks)
        pygame.display.update()
        clock.tick(60)

main()