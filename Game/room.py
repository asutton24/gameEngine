import gameObject
import pygame

class Room:
    def __init__(self, t, e, it, b, r, ty, scr):
        self.tiles = t
        self.enemies = e
        self.items = it
        self.background = b
        self.reward = r
        self.type = ty
        self.screen = scr

    def update(self):
        self.screen.fill(self.background)
        for i in self.tiles:
            i.update()