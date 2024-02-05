from room import *
from gameObject import *
import pygame

running = True
p = input('Enter room path')
screen = pygame.display.set_mode([1024, 720], pygame.FULLSCREEN)
p1 = Player(70, 250, screen)
clock = pygame.time.Clock()
room = Room(p, 0, (0, 0, 0), screen)
p1.giveWeapon(Projectile(Sprite('block.txt', 0, 0, (255, 0, 0), -1, 1, screen), 12, 10, 1, False, True, False, 5, 10))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                running = False
    p1.takeInput(pygame.key.get_pressed())
    room.update(p1)
    p1.update(room.returnAll())
    p1.drawHealthBar(64, 620, screen)
    p1.drawAutoMap(800, 620, screen)
    pygame.display.update()
    clock.tick(60)
