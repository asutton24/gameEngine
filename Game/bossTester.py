import pygame
from room import *
from gameObject import *

running = True
screen = pygame.display.set_mode([1024, 720], pygame.FULLSCREEN)
p1 = Player(70, 270, screen)
clock = pygame.time.Clock()
room = BossRoom('bossRoom.room', (0, 0, 0), 0, [[3, 4, 5, 6], [7, 8]], 600, [1, 2], [1, 2], 300, 0, 240, screen)
p1.giveWeapon(Projectile(Sprite('block.spr', 0, 0, (255, 0, 0), -1, 1, screen), 12, 10, 10, False, True, False, 5, 10))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                running = False
    screen.fill((0, 0, 0))
    p1.takeInput(pygame.key.get_pressed())
    room.update(p1)
    p1.update(room.returnAll())
    p1.drawHealthBar(64, 620, screen)
    p1.drawAutoMap(800, 620, screen)
    p1.drawMoneyCount(400, 620, screen)
    p1.drawCurrentItem(680, 620, screen)
    room.drawBossHp(64, 690, screen)
    pygame.display.update()
    clock.tick(60)
