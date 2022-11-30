import pygame
import random
import math
from car import Car
from level import Level

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
        self.density_factor = 0.3 + (0.1 * level)
        self.coverage = 0
        self.level = None

    def create_spaces(self):
        self.free_places = []
        self.full_grid = []
        xy_values = [i for i in range(0, self.size-self.block_size+1, self.block_size)]
        for x in range(0, len(xy_values)):
            for y in range(0, len(xy_values)):
                self.full_grid.append((xy_values[x], xy_values[y]))
                self.free_places.append((xy_values[x], xy_values[y]))
        self.red_car_xys = [place for place in self.full_grid
                            if place[1] == self.full_grid[self.rows_columns_count // 2][1]
                            and place[0] < self.size - self.block_size*3]
        self.coverage = math.floor(self.density_factor * len(self.full_grid))

    def create_cars(self):
        self.cars = []
        # randomly devides the grid coverage (minus red car) in to cars of length 2 and 3
        counter = self.coverage - 2
        car_count = []
        while counter > 0:
            two_three = random.choice([2, 3])
            counter -= two_three
            car_count.append(two_three)
        twos = car_count.count(2)
        threes = car_count.count(3)

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
        placement = random.choice(self.full_grid)
        car.car_rect.topleft = placement

    def pos_check(self, car):
        if car.car_rect.bottom > self.size:
            return False
        elif car.car_rect.right > self.size:
            return False
        elif car.car_rect.collidelist(self.car_rects) != -1:
            return False
        elif car.car_rect.topleft[1] == self.cars[0].car_rect.topleft[1] and car.horizontal:
            return False
        else:
            return True

    def update_free_places(self):
        used_places = []
        self.car_rects = [car.car_rect for car in self.cars]
        for car in self.cars:
            index = self.full_grid.index(car.car_rect.topleft)
            if car.horizontal:
                for i in range(0, car.length):
                    i = index + self.rows_columns_count * i
                    if i <= len(self.full_grid)-1:
                        used_places.append(self.full_grid[i])
                    else:
                        break
            elif not car.horizontal:
                for i in range(0, car.length):
                    i = index + i
                    if i <= len(self.full_grid)-1:
                        used_places.append(self.full_grid[i])
                    else:
                        break
            new_free_places = [place for place in self.full_grid if place not in used_places]
            self.free_places = new_free_places

    def create_random_level(self, screen):
        def restart():
            screen.fill((0, 0, 0))
            self.create_spaces()
            self.create_cars()
            self.create_random_level(screen)
        self.cars[0].car_rect.topleft = random.choice(self.red_car_xys)
        screen.blit(self.cars[0].car, self.cars[0].car_rect)
        self.cars[1:].sort(key=lambda x: int(x.length), reverse=True)
        for car in self.cars[1:]:
            attempt_count = 0
            while True:
                self.place_car_pos(car)
                # next line makes a car_rects list without current car so that check dosent check car to itself
                self.car_rects = [car_u.car_rect for car_u in self.cars if car_u != car]
                if self.pos_check(car):
                    self.car_rects.append(car.car_rect)
                    break
                attempt_count += 1
                if attempt_count > 300:
                    attempt_count = 0
                    print('oops')
                    restart()
        self.blit_cars(screen)
        self.update_free_places()
        self.level = Level(rows_columns=self.rows_columns_count, grid=self.full_grid, first_position_cars=self.cars, screen_size=self.size)

    def blit_cars(self, screen):
        for car in self.cars:
            screen.blit(car.car, car.car_rect)

    def check_mouse_click(self, pos, screen):
        for car in self.cars:
            if car.car_rect.collidepoint(pos):
                if not car.horizontal:
                    if pos[1] < car.car_rect.center[1]:
                        car.move('up', self.full_grid, self.free_places, self.rows_columns_count)
                    elif pos[1] > car.car_rect.center[1]:
                        car.move('down', self.full_grid, self.free_places, self.rows_columns_count)
                elif car.horizontal:
                    if pos[0] < car.car_rect.center[0]:
                        car.move('left', self.full_grid, self.free_places, self.rows_columns_count)
                    elif pos[0] > car.car_rect.center[0]:
                        car.move('right', self.full_grid, self.free_places, self.rows_columns_count)
                screen.fill((0, 0, 0))
                self.car_rects = [car.car_rect for car in self.cars]
                self.blit_cars(screen)
                self.update_free_places()

