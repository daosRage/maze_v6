import pygame
from data import *

pygame.init()


class Sprite(pygame.Rect):
    def __init__(self, x, y, width, height, color=(120,120,120), image= None, speed= 5):
        super().__init__(x, y, width, height)
        self.COLOR = color
        self.IMAGE = image
        self.SPEED = speed

class Hero(Sprite):
    def __init__(self, x, y, width, height, color=(120,120,120), image= None, speed= 5):
        super().__init__(x, y, width, height, color, image, speed)
        self.MOVE = {"UP": False, "DOWN": False, "LEFT": False, "RIGHT": False}

    def move(self, window):
        if self.MOVE["UP"] and self.y > 0:
            self.y -= self.SPEED
        elif self.MOVE["DOWN"] and self.y < setting_win["HEIGHT"] - self.height:
            self.y += self.SPEED
        if self.MOVE["LEFT"] and self.x > 0:
            self.x -= self.SPEED
        elif self.MOVE["RIGHT"] and self.x < setting_win["WIDTH"] - self.width:
            self.x += self.SPEED

        pygame.draw.rect(window, self.COLOR, self)
