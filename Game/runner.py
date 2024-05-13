import pygame
import game


def main():
    running = True
    quickStart = False
    restart = False
    status = 0
    read = False
    while not read:
        try:
            with open('data.bin', 'rb') as file:
                data1 = file.read(1)
                data2 = file.read(4)
                data3 = file.read(1)
                read = True
                file.close()
        except FileNotFoundError:
            with open('data.bin', 'wb') as file:
                file.close()
    controls = int.from_bytes(data1, 'little')
    score = int.from_bytes(data2, 'little')
    full = int.from_bytes(data3, 'little')
    if full == 66 or full == 67:
        full -= 66
        cheats = 0
    else:
        cheats = 1
    if full == 1:
        screen = pygame.display.set_mode([1024, 768], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([1024, 768])
    pygame.display.set_caption(' ')
    pygame.init()
    pygame.joystick.init()
    if quickStart:
        running = False
        game.run(screen, controls)
    while running:
        if not restart:
            status = game.home(screen, controls, score)
            if status == -1:
                running = False
        else:
            restart = False
        if status == 0:
            status = game.run(screen, controls, cheats)
            if int(status / 10) > score:
                score = int(status / 10)
            status %= 10
            if status == 0:
                restart = True
        elif status == 1:
            status = game.settings(screen, controls, full)
            if status == -1:
                running = False
            elif status > 9 and full == 0:
                full = 1
                screen = pygame.display.set_mode([1024, 768], pygame.FULLSCREEN)
            elif status < 10 and full == 1:
                full = 0
                screen = pygame.display.set_mode([1024, 768])
            controls = status % 10
        elif status == 2:
            running = False
    with open('data.bin', 'wb') as file:
        pass
        file.close()
    with open('data.bin', 'wb') as file:
        file.write(controls.to_bytes(1, 'little'))
        file.write(score.to_bytes(4, 'little'))
        file.write(full.to_bytes(1, 'little'))
        file.close()


main()
