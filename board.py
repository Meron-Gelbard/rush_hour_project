import pygame
import sys
import random
import math
from car import Car
from level import Level
import json
import time
from threading import Thread

car_colors = ['red', 'blue', 'cyan', 'pink', 'orange', 'green']

class Board:
    def __init__(self, size, level, rows_columns, gui):
        self.gui = gui
        self.listening = True
        self.size = size
        self.rows_columns_count = rows_columns
        self.block_size = size // rows_columns
        self.level = level
        self.cars = []
        self.full_grid = []
        self.free_places = []
        self.red_car_xys = []
        self.density_factor = 0.3 + (0.1 * level)
        self.place_coverage = 0
        self.level = None
        self.previous_moves = []
        self.red_is_out = False
        self.btn_funcs = {
            " Load Card ": self.load_level,
            " Create Card ": self.create_level,
            " Play Solution ": self.solution_player,
            " Undo ": self.undo_move,
            " Restart ": self.restart_level
        }

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

    def place_car_pos(self, car, placement):
        car.car_rect.topleft = placement
        # next line makes a car_rects list without current car so that the check dosent check car to itself
        car_rects = [car_u.car_rect for car_u in self.cars if car_u != car]
        if car.car_rect.bottom > self.size:
            return False
        elif car.car_rect.right > self.size:
            return False
        elif car.car_rect.collidelist(car_rects) != -1:
            return False
        elif car.car_rect.topleft[1] == self.cars[0].car_rect.topleft[1] and car.horizontal:
            return False
        else:
            return True

    def update_free_places(self):
        used_places = []
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
            self.free_places = [place for place in self.full_grid if place not in used_places]

    def create_random_level(self, screen):
        self.red_is_out = False
        self.listening = True
        screen.fill((0, 0, 0))
        pygame.display.flip()
        self.create_spaces()
        self.create_cars()
        self.cars[0].car_rect.topleft = random.choice(self.red_car_xys)
        for car in self.cars[1:]:
            attempt_count = 0
            self.update_free_places()
            while not self.place_car_pos(car, random.choice(self.free_places)):
                attempt_count += 1
                if attempt_count > 1000000:
                    attempt_count = 0
                    print('failed to build')
                    self.create_random_level(screen)
                    return
        self.update_free_places()
        self.level = Level(rows_columns=self.rows_columns_count, grid=self.full_grid, first_position_cars=self.cars,
                           screen_size=self.size)

        level_position = []
        for i in range(len(self.level.first_position)):
            level_position.append({'topleft_xy': self.level.first_position[i],
                                   'grid_index': self.full_grid.index(self.level.first_position[i]),
                                   'car_length': self.cars[i].length,
                                   'horizontal': self.cars[i].horizontal})
        level_position[1:].sort(key=lambda x: (x['grid_index']))

        with open("unsolvable.json", "r") as data:
            unsolvables = json.load(data)

        if level_position not in unsolvables:
            self.level.level_solver()
        elif level_position in unsolvables:
            print('unsolvable level. found in json!!!!!')
            self.create_random_level(screen)
            return

        if not self.level.solvable:
            unsolvables.append(level_position)
            with open("unsolvable.json", "w") as file:
                json.dump(unsolvables, file)
            print('unsolvable level. added to json.')
            self.create_random_level(screen)
            return
        elif self.level.solvable:
            self.level.save_level()
            self.previous_moves = [self.level.route[0]]
            return
        # else:
        #     print('less than 10 moves...')
        #     self.create_random_level(screen)
        #     return

    def blit_cars(self, screen):
        for car in self.cars:
            screen.blit(car.car, car.car_rect)

    def car_move_click(self, pos):
        previous_move = [car.car_rect.topleft for car in self.cars]
        moved = False
        for car in self.cars:
            if car.car_rect.collidepoint(pos):
                if not car.horizontal:
                    if pos[1] < car.car_rect.center[1]:
                        moved = car.move('up', self.full_grid, self.free_places, self.rows_columns_count)
                    elif pos[1] > car.car_rect.center[1]:
                        moved = car.move('down', self.full_grid, self.free_places, self.rows_columns_count)
                elif car.horizontal:
                    if pos[0] < car.car_rect.center[0]:
                        moved = car.move('left', self.full_grid, self.free_places, self.rows_columns_count)
                    elif pos[0] > car.car_rect.center[0]:
                        moved = car.move('right', self.full_grid, self.free_places, self.rows_columns_count)
                        if self.cars.index(car) == 0 and car.car_rect.right >= self.size - 10:
                            self.red_is_out = True
        if moved:
            self.previous_moves.append(previous_move)
            self.update_free_places()

    def solution_player(self, screen):
        self.listening = False
        if self.red_is_out:
            self.previous_moves = [self.level.route[0]]
            self.red_is_out = False
        try:
            for move in self.level.route:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.gui.btn_release(self.gui.btns[2])
                    if event.type == pygame.QUIT:
                        sys.exit()
                for i in range(len(self.cars)):
                    self.cars[i].car_rect.topleft = move[i]
                screen.fill((0, 0, 0))
                self.blit_cars(screen)
                self.gui.blit_btns(screen, self)
                self.gui.blit_status(self.level.route.index(move) + 1, len(self.level.route), screen)
                pygame.display.flip()
                time.sleep(1)
            self.gui.message_text = "Red car is out!"
            self.gui.render_message(screen)
            pygame.display.flip()
            time.sleep(3)
            for i in range(len(self.cars)):
                self.cars[i].car_rect.topleft = self.previous_moves[-1][i]
                self.listening = True
        except AttributeError:
            pass

    def get_random_level(self, difficulty):
        difficulty *= 10
        with open("solved_levels.json", "r") as levels_db:
            levels = json.load(levels_db)
        try:
            random_level = random.choice([level for level in levels if difficulty <= int(level["moves_2_exit"]) < difficulty+10])
        except Exception:
            return None
        return random_level

    def load_level(self, screen):
        self.listening = True
        self.red_is_out = False
        try:
            difficulty = int(self.gui.user_input(screen, 'Please enter difficulty level (1 - 3):'))
        except TypeError:
            self.load_level(screen)
            return
        if 3 >= int(difficulty) >= 0:
            level = self.get_random_level(difficulty)
        else:
            self.gui.user_input_txt = '#'
            self.load_level(screen)
            return
        if level == None:
            self.gui.btn_release(self.gui.btns[0])
            self.load_level(screen)
            return

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
        self.previous_moves = [self.level.route[0]]
        self.gui.user_input_txt = ''
        self.gui.btn_release(self.gui.btns[0])

    def restart_level(self, screen):
        self.listening = True
        self.red_is_out = False
        try:
            self.previous_moves = [self.level.route[0]]
            for i in range(len(self.cars)):
                self.cars[i].car_rect.topleft = self.level.route[0][i]
            self.update_free_places()
        except AttributeError:
            pass

    def undo_move(self, screen):
        if self.listening and len(self.previous_moves) > 1:
            last_position = self.previous_moves.pop(-1)
            for i in range(len(self.cars)):
                self.cars[i].car_rect.topleft = last_position[i]
        self.update_free_places()

    def create_level(self, screen):
        self.create_spaces()
        length = 2
        horizontal = False
        cars = [Car(2, self.block_size, 'red', True)]
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not horizontal:
                    for i in range(len(self.full_grid)):
                        if self.full_grid[i][1] < pos[1] < self.full_grid[i+1][1]:
                            pos = self.full_grid[i]
                    new_car = Car(length, self.block_size, random.choice(car_colors[1:]), horizontal)
                    if self.place_car_pos(new_car, pos):
                        cars.append(new_car)
                elif horizontal:
                    for i in range(len(self.full_grid)):
                        if self.full_grid[i][0] < pos[0] < self.full_grid[i+self.rows_columns_count][0]:
                            pos = self.full_grid[i]
                    new_car = Car(length, self.block_size, random.choice(car_colors[1:]), horizontal)
                    if self.place_car_pos(new_car, pos):
                        cars.append(new_car)


