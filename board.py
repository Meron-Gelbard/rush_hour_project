import pygame
import random
import math
from car import Car
from level import Level
import json

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
        self.place_coverage = 0
        self.level = None
        self.previous_moves = []

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
        self.place_coverage = math.floor(self.density_factor * len(self.full_grid))

    def create_cars(self):
        # randomly devides the grid coverage (minus red car) into cars of length 2 and 3
        self.cars = []
        counter = self.place_coverage - 2
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
        placement = random.choice(self.free_places)
        car.car_rect.topleft = placement
        # next line makes a car_rects list without current car so that the check dosent check car to itself
        self.car_rects = [car_u.car_rect for car_u in self.cars if car_u != car]
        if car.car_rect.bottom > self.size:
            passed = False
        elif car.car_rect.right > self.size:
            passed = False
        elif car.car_rect.collidelist(self.car_rects) != -1:
            passed = False
        elif car.car_rect.topleft[1] == self.cars[0].car_rect.topleft[1] and car.horizontal:
            passed = False
        else:
            passed = True
        return passed

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
        screen.fill((0, 0, 0))
        pygame.display.flip()
        self.create_spaces()
        self.create_cars()
        self.cars[0].car_rect.topleft = random.choice(self.red_car_xys)
        for car in self.cars[1:]:
            attempt_count = 0
            self.update_free_places()
            while not self.place_car_pos(car):
                attempt_count += 1
                if attempt_count > 1000000:
                    attempt_count = 0
                    print('failed to build')
                    self.create_random_level(screen)
                    return
        self.update_free_places()
        self.level = Level(rows_columns=self.rows_columns_count, grid=self.full_grid, first_position_cars=self.cars,
                           screen_size=self.size)

        level_pos_dict = {'first_position': self.level.first_position,
                          'free_spaces': self.free_places}

        with open("unsolvable.json", "r") as data:
            unsolvables = json.load(data)

        if level_pos_dict not in unsolvables:
            self.level.level_solver()
        else:
            print('unsolvable level. found in json!')
            self.create_random_level(screen)
            return

        if not self.level.solvable:
            unsolvables.append(level_pos_dict)
            with open("unsolvable.json", "w") as file:
                json.dump(unsolvables, file)
            print('unsolvable level. added to json.')
            self.create_random_level(screen)
            return
        elif self.level.solvable and self.level.moves_2_exit > 10:
            self.level.save_level()
            print('solvable level saved to json!')
            return
        else:
            print('less than 10 moves...')
            self.create_random_level(screen)
            return

    def blit_cars(self, screen):
        for car in self.cars:
            screen.blit(car.car, car.car_rect)

    def car_move_click(self, pos, screen):
        self.previous_moves.append([car.car_rect.topleft for car in self.cars])
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
                        if self.cars.index(car) == 0 and car.car_rect.right >= self.size - 10:
                            print('red is out')
                screen.fill((0, 0, 0))
                self.car_rects = [car.car_rect for car in self.cars]
                self.blit_cars(screen)
                self.update_free_places()

    def solution_player(self, screen):
        for move in self.level.route:
            for i in range(len(self.cars)):
                self.cars[i].car_rect.topleft = move[i]
            screen.fill((0, 0, 0))
            self.blit_cars(screen)
            pygame.display.flip()
            pygame.time.wait(1000)

    def get_random_level(self):
        with open("solved_levels.json", "r") as levels_db:
            levels = json.load(levels_db)
        try:
            random_level = random.choice(levels)
        except Exception:
            random_level = {}
            print('No levels saved')
            return
        return random_level

    def load_level(self, screen, level):
        self.previous_moves = []
        screen.fill((0, 0, 0))
        pygame.display.flip()
        self.create_spaces()
        self.cars = []
        for i in range(1, len(level['cars'])):
            self.cars.append(Car(block_width=level['cars'][i]['block_width'],
                                 length=level['cars'][i]['length'],
                                 color=random.choice(car_colors[1:]),
                                 horizontal=level['cars'][i]['horizontal']))
        self.cars.insert(0, Car(block_width=level['cars'][0]['block_width'],
                                length=level['cars'][0]['length'],
                                color=car_colors[0],
                                horizontal=level['cars'][0]['horizontal']))
        self.level = Level(rows_columns=self.rows_columns_count, grid=self.full_grid, first_position_cars=self.cars,
                           screen_size=self.size)

        for c in range(0, len(level['cars'])):
            self.cars[c].car_rect.topleft = level['cars'][c]['topleft_xy']

        self.level.solvable = True
        self.level.moves_2_exit = level['moves_2_exit']
        self.level.route = level['solution_route']
        self.blit_cars(screen)

    def restart_level(self, screen):
        self.previous_moves = []
        first_position = self.level.route[0]
        for i in range(len(self.cars)):
            self.cars[i].car_rect.topleft = first_position[i]
        screen.fill((0, 0, 0))
        self.blit_cars(screen)

    def undo_move(self, screen):
        try:
            last_position = self.previous_moves.pop(-1)
            for i in range(len(self.cars)):
                self.cars[i].car_rect.topleft = last_position[i]
            screen.fill((0, 0, 0))
            self.blit_cars(screen)
        except IndexError:
            return




