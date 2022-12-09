import pygame
import sys
import random
import pygame.locals as K

class Car:
    def __init__(self, length, block_width, color, horizontal):
        self.length = length
        self.width = block_width
        self.car_color = f"img/{color}_car_{length}.png"
        self.car = pygame.image.load(self.car_color)
        self.horizontal = horizontal
        if self.horizontal is None:
            self.horizontal = random.choice([True, False])
        if self.horizontal:
            self.size = (self.width * self.length, self.width)
        else:
            self.size = (self.width, self.width * self.length)
            self.car = pygame.transform.rotate(self.car, random.choice([90, -90]))
        self.car = pygame.transform.scale(self.car, self.size)
        self.car_rect = self.car.get_rect()

    def move(self, direction, grid, free_places, rows_columns):
        last_index = grid.index(self.car_rect.topleft)
        if direction == 'right':
            if (self.car_rect.topleft[0] + self.width * self.length, self.car_rect.topleft[1]) in free_places:
                self.car_rect.topleft = grid[last_index + rows_columns]
                return True
        elif direction == 'left':
            if (self.car_rect.topleft[0] - self.width, self.car_rect.topleft[1]) in free_places:
                self.car_rect.topleft = grid[last_index - rows_columns]
                return True
        elif direction == 'up':
            if (self.car_rect.topleft[0], self.car_rect.topleft[1] - self.width) in free_places:
                self.car_rect.topleft = grid[last_index - 1]
                return True
        elif direction == 'down':
            if (self.car_rect.topleft[0], self.car_rect.topleft[1] + self.width * self.length) in free_places:
                self.car_rect.topleft = grid[last_index + 1]
                return True


