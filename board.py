import pygame
import sys
import random
import pygame.locals as K
from car import Car

car_colors = ['red', 'blue', 'cyan', 'pink', 'orange', 'green']

class Board:
    def __init__(self, size, level, rows_columns):
        self.size = size
        self.rows_columns_count = rows_columns
        self.block_size = size // rows_columns
        self.level = level
        self.cars = []
        self.full_grid = []
        self.free_places = []
        self.car_rects = []
        self.red_car_xys = []

    def create_spaces(self):
        self.free_places = []
        xy_values = [i for i in range(0, self.size + 1, self.block_size)]
        for x in range(0, len(xy_values)):
            for y in range(0, len(xy_values)):
                self.full_grid.append((xy_values[x], xy_values[y]))
                self.free_places.append((xy_values[x], xy_values[y]))
        self.red_car_xys = [place for place in self.full_grid[:-self.rows_columns_count]
                            if place[1] == self.full_grid[self.rows_columns_count // 2][1]
                            and place[0] < self.size - self.block_size*3]

    def create_cars(self):
        self.cars = []
        twos = self.level * 3
        threes = self.level
        self.cars.append(Car(2, self.block_size, car_colors[0], True))
        for i in range(1, twos+1):
            if i > len(car_colors[1:]):
                i = (i % len(car_colors[1:]))+1
            self.cars.append(Car(2, self.block_size, car_colors[i], None))
        for i in range(1, threes+1):
            if i > len(car_colors[1:]):
                i = (i % len(car_colors[1:]))+1
            self.cars.append(Car(3, self.block_size, car_colors[i], None))
        self.car_rects = [car.car_rect for car in self.cars]

    def place_car_pos(self, car):
        try:
            placement = random.choice(self.free_places)
        except IndexError:
            return False
        index = self.full_grid.index(placement)
        car.car_rect.topleft = placement
        new_free_places = self.free_places
        used_places = []
        if car.horizontal:
            for i in range(0, car.length):
                i = index + self.rows_columns_count * i
                if i <= len(self.full_grid)-1:
                    used_places.append(self.full_grid[i])
                else:
                    break
        elif not car.horizontal:
            for i in range(0, car.length):
                i = index + 1
                if i <= len(self.full_grid)-1:
                    used_places.append(self.full_grid[i])
                else:
                    break
        self.free_places = new_free_places
        return True

    def pos_check(self, car):
        if car.car_rect.bottom > self.size:
            return False
        elif car.car_rect.right > self.size:
            return False
        elif car.car_rect.collidelist(self.car_rects) != -1:
            return False
        else:
            return True

    def cars_random_placement(self, screen):
        def restart():
            screen.fill((0, 0, 0))
            self.create_spaces()
            self.create_cars()
            self.cars_random_placement(screen)

        self.cars[0].car_rect.topleft = random.choice(self.red_car_xys)
        screen.blit(self.cars[0].car, self.cars[0].car_rect)
        self.cars[1:].sort(key=lambda x: int(x.length), reverse=True)
        for car in self.cars[1:]:
            attempt_count = 0
            while True:
                positioned = self.place_car_pos(car)
                # next line makes a car_rects list without current car so that check dosent check car to itself
                self.car_rects = [car_u.car_rect for car_u in self.cars if car_u != car]
                if positioned and self.pos_check(car):
                    self.car_rects.append(car.car_rect)
                    screen.blit(car.car, car.car_rect)
                    print(attempt_count)
                    break
                attempt_count += 1
                if attempt_count > 100:
                    restart()
