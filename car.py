import pygame
import sys
import random
import pygame.locals as K

class Car:
    def __init__(self, length, block_width, color, horizontal):
        self.color = color
        self.length = length
        self.width = block_width
        self.car_color = {'color': color,
                          'link': f"img/{color}_brick.png"}
        self.horizontal = horizontal
        if self.horizontal is None:
            self.horizontal = random.choice([True, False])
        if self.horizontal:
            self.size = (self.width * self.length, self.width)
        else:
            self.size = (self.width, self.width * self.length)
        self.car = pygame.image.load(self.car_color['link'])
        self.car = pygame.transform.scale(self.car, self.size)
        self.car_rect = self.car.get_rect()
