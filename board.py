import pygame
import sys
import random
import math
from car import Car
from card import Card
import json
import time
import itertools
import pygame.locals as K

car_colors = itertools.cycle(['blue', 'cyan', 'pink', 'orange', 'green'])


class Board:
    """ Main game class holding all main game functions,
    objects and attributes
    """

    def __init__(self, size, level, rows_columns, gui):
        self.GUI = gui
        self.ROWS_COLUMNS_COUNT = rows_columns
        self.BLOCK_SIZE = size // rows_columns
        self.BOARD_SIZE = size
        self.FULL_GRID = []

        self.level = level
        self.cars = []
        self.free_places = []
        self.red_car_xys = []
        self.density_factor = 0.3 + (0.1 * level)
        self.place_coverage = 0

        self.card = None
        self.listening = True
        self.red_is_out = False
        self.previous_moves = []

        self.btn_funcs = {
            " Load Card ": self.load_card,
            " Create Card ": self.create_card,
            " Play Solution ": self.solution_player,
            " Undo ": self.undo_move,
            " Restart ": self.restart_card}

    def create_spaces(self):
        """Creates a grid and a new free-places list
         Creates possible red car positions in center
         Generates a grid place coverage attribute used by card creator
         for generating cars.
         """

        self.free_places = []
        self.FULL_GRID = []
        xy_values = [i for i in range(0, self.BOARD_SIZE - self.BLOCK_SIZE + 1, self.BLOCK_SIZE)]
        self.FULL_GRID = list(itertools.product(xy_values, repeat=2))
        self.free_places = self.FULL_GRID
        self.red_car_xys = [place for place in self.FULL_GRID
                            if place[1] == self.FULL_GRID[self.ROWS_COLUMNS_COUNT // 2][1]
                            and place[0] < self.BOARD_SIZE - self.BLOCK_SIZE * 3]
        self.place_coverage = math.floor(self.density_factor * len(self.FULL_GRID))

    def create_cars(self):
        """ Randomly divides the grid place coverage (minus red car)
         into list of cars of lengths 2 or 3.
         Creates cars accordingly. red car always first
         """

        self.cars = []
        counter = self.place_coverage - 2  # take off red car coverage
        car_count = []

        # randomly divides coverage to 2's and 3's
        while counter > 0:
            two_three = random.choice([2, 3])
            counter -= two_three
            car_count.append(two_three)
        twos = car_count.count(2)
        threes = car_count.count(3)

        self.cars.append(Car(2, self.BLOCK_SIZE, 'red', True))  # add red car at random position
        # generates cars according to 2's and 3's counters
        for i in range(1, twos + 1):
            self.cars.append(Car(2, self.BLOCK_SIZE, next(car_colors), None))
        for i in range(1, threes + 1):
            self.cars.append(Car(3, self.BLOCK_SIZE, next(car_colors), None))

    def place_car_pos(self, car, placement):
        """Function tries to place a given car (top-left x,y)
         in a given position according to restrictions.
        Return success as a boolean
        """

        car.car_rect.topleft = placement
        # make a car rectangle list without current car so that check doesn't check car to itself
        car_rects = [car_u.car_rect for car_u in self.cars if car_u != car]

        # check car out of bottom
        if car.car_rect.bottom > self.BOARD_SIZE:
            return False
        # check car out of right side
        elif car.car_rect.right > self.BOARD_SIZE:
            return False
        # check car collision with other cars (pygame function)
        elif car.car_rect.collidelist(car_rects) != -1:
            return False
        # check if horizontal car blocking red car (makes card unsolvable)
        elif car.car_rect.topleft[1] == self.cars[0].car_rect.topleft[1] and car.horizontal:
            return False
        else:
            return True

    def update_free_places(self):
        """ Updates free grid places attribute according to current car positions """

        used_places = []
        for car in self.cars:
            index = self.FULL_GRID.index(car.car_rect.topleft)
            if car.horizontal:
                for i in range(0, car.length):
                    i = index + self.ROWS_COLUMNS_COUNT * i
                    if i <= len(self.FULL_GRID) - 1:
                        used_places.append(self.FULL_GRID[i])
                    else:
                        break
            elif not car.horizontal:
                for i in range(0, car.length):
                    i = index + i
                    if i <= len(self.FULL_GRID) - 1:
                        used_places.append(self.FULL_GRID[i])
                    else:
                        break
            self.free_places = [place for place in self.FULL_GRID if place not in used_places]

    def create_random_card(self, screen):

        screen.fill((0, 0, 0))
        pygame.display.flip()

        self.red_is_out = False
        self.listening = True
        self.create_spaces()
        self.create_cars()
        self.cars[0].car_rect.topleft = random.choice(self.red_car_xys)

        # attempt to place cars using placement checker
        for car in self.cars[1:]:
            attempt_count = 0
            self.update_free_places()
            while not self.place_car_pos(car, random.choice(self.free_places)):
                attempt_count += 1
                if attempt_count > 1000000:
                    print('failed to build')
                    self.create_random_card(screen)  # if failed to position restart function
                    return
        self.update_free_places()

        # when all cars are placed a card object is created
        self.card = Card(rows_columns=self.ROWS_COLUMNS_COUNT, grid=self.FULL_GRID, first_position_cars=self.cars,
                         screen_size=self.BOARD_SIZE)

        level_position = []
        for i in range(len(self.card.first_position)):
            level_position.append({'topleft_xy': self.card.first_position[i],
                                   'grid_index': self.FULL_GRID.index(self.card.first_position[i]),
                                   'car_length': self.cars[i].length,
                                   'horizontal': self.cars[i].horizontal})
        level_position[1:].sort(key=lambda x: (x['grid_index']))

        # check if new card appears in unsolvables and call the card solver if not

        with open("unsolvable.json", "r") as data:
            unsolvables = json.load(data)

        if level_position not in unsolvables:
            self.card.card_solver()
        elif level_position in unsolvables:
            print('unsolvable level. found in json!')
            self.create_random_card(screen)  # if found in unsolvables restart function
            return

        if not self.card.solvable:
            unsolvables.append(level_position)
            with open("unsolvable.json", "w") as file:
                json.dump(unsolvables, file)
            print('unsolvable level. added to json.')
            self.create_random_card(screen)
            return
        elif self.card.solvable:
            self.card.save_card()
            self.previous_moves = [self.card.route[0]]
            return

    def blit_cars(self, screen):
        """Render cars on screen in current positions """
        for car in self.cars:
            screen.blit(car.car, car.car_rect)

    def car_move_click(self, pos):
        """Function call the move function with appropriate parameters
         according to car orientation and the side of the car that was clicked
         (relative to center)
         if car was moves successfuly, functions updates the
         previouse moves list and the current free places"""

        previous_move = [car.car_rect.topleft for car in self.cars]
        moved = False
        for car in self.cars:
            if car.car_rect.collidepoint(pos):
                if not car.horizontal:
                    if pos[1] < car.car_rect.center[1]:
                        moved = car.move('up', self.FULL_GRID, self.free_places, self.ROWS_COLUMNS_COUNT)
                    elif pos[1] > car.car_rect.center[1]:
                        moved = car.move('down', self.FULL_GRID, self.free_places, self.ROWS_COLUMNS_COUNT)
                elif car.horizontal:
                    if pos[0] < car.car_rect.center[0]:
                        moved = car.move('left', self.FULL_GRID, self.free_places, self.ROWS_COLUMNS_COUNT)
                    elif pos[0] > car.car_rect.center[0]:
                        moved = car.move('right', self.FULL_GRID, self.free_places, self.ROWS_COLUMNS_COUNT)
                        if self.cars.index(car) == 0 and car.car_rect.right >= self.BOARD_SIZE - 10:
                            self.red_is_out = True
        if moved:
            self.previous_moves.append(previous_move)
            self.update_free_places()
            return True

    def solution_player(self, screen):
        """ Plays the solution path found by the card solver"""

        self.listening = False
        if self.red_is_out:
            self.previous_moves = [self.card.route[0]]
            self.red_is_out = False
        try:
            for move in self.card.route:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.GUI.btn_release(self.GUI.btns[2])
                    if event.type == pygame.QUIT:
                        sys.exit()
                for i in range(len(self.cars)):
                    self.cars[i].car_rect.topleft = move[i]
                screen.fill((0, 0, 0))
                self.blit_cars(screen)
                self.GUI.blit_btns(screen, self)
                self.GUI.blit_status(self.card.route.index(move) + 1, len(self.card.route), screen)
                pygame.display.flip()
                time.sleep(1)
            self.GUI.render_msg(screen, 'Red car is out!', 'center')
            pygame.display.flip()
            time.sleep(3)
            for i in range(len(self.cars)):
                self.cars[i].car_rect.topleft = self.previous_moves[-1][i]
                self.listening = True
        except AttributeError:
            pass

    @staticmethod
    def get_random_card(difficulty):
        """ gets a random card from the solved cards list"""

        difficulty *= 10
        with open("solved_cards.json", "r") as levels_db:
            levels = json.load(levels_db)
        try:
            random_level = random.choice([level for level in levels
                                          if difficulty <= int(level["moves_2_exit"]) < difficulty + 10])
        except Exception:
            return None
        return random_level

    def load_card(self, screen):
        """ Load level GUI """
        # need fixing. error when difficulty not found in level list

        self.listening = True
        self.red_is_out = False
        try:
            difficulty = int(self.GUI.user_input(screen))
        except TypeError:
            self.load_card(screen)
            return
        if 5 >= int(difficulty) >= 0:
            current_card = self.get_random_card(difficulty)
        else:
            self.GUI.user_input_txt = '#'
            self.load_card(screen)
            return
        if current_card is None:
            self.GUI.btn_release(self.GUI.btns[0])
            self.load_card(screen)
            return

        self.create_spaces()
        self.cars = []
        for i in range(1, len(current_card['cars'])):
            self.cars.append(Car(block_width=current_card['cars'][i]['block_width'],
                                 length=current_card['cars'][i]['length'], color=next(car_colors),
                                 horizontal=current_card['cars'][i]['horizontal']))
        self.cars.insert(0, Car(block_width=current_card['cars'][0]['block_width'],
                                length=current_card['cars'][0]['length'],
                                color='red', horizontal=current_card['cars'][0]['horizontal']))
        self.card = Card(rows_columns=self.ROWS_COLUMNS_COUNT, grid=self.FULL_GRID,
                         first_position_cars=self.cars, screen_size=self.BOARD_SIZE)

        for c in range(0, len(current_card['cars'])):
            self.cars[c].car_rect.topleft = current_card['cars'][c]['topleft_xy']

        self.card.solvable = True
        self.card.moves_2_exit = current_card['moves_2_exit']
        self.card.route = current_card['solution_route']
        self.previous_moves = [self.card.route[0]]
        self.GUI.user_input_txt = ''
        self.GUI.btn_release(self.GUI.btns[0])

    def restart_card(self):
        self.listening = True
        self.red_is_out = False
        try:
            self.previous_moves = [self.card.route[0]]
            for i in range(len(self.cars)):
                self.cars[i].car_rect.topleft = self.card.route[0][i]
            self.update_free_places()
        except AttributeError:
            pass

    def undo_move(self):
        """ goes back one move """

        if self.listening and len(self.previous_moves) > 1:
            last_position = self.previous_moves.pop(-1)
            for i in range(len(self.cars)):
                self.cars[i].car_rect.topleft = last_position[i]
        self.update_free_places()

    def create_card(self, screen):
        """ create a custom card that gets solved by the card solver """
        # still in development...
        screen.fill((0, 0, 0))
        pygame.display.flip()
        self.create_spaces()
        length = 2
        horizontal = False
        self.cars = []
        while True:
            if horizontal:
                gui_txt = f"Horizontal | Size: {length} ('f'/'2'/'3')"
            else:
                gui_txt = f"Vertical | Size: {length} ('f'/'2'/'3')"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K.K_f:
                        horizontal = not horizontal
                    if event.key == K.K_2:
                        length = 2
                    if event.key == K.K_3:
                        length = 3
                    if event.key == K.K_RETURN:
                        self.card = Card(rows_columns=self.ROWS_COLUMNS_COUNT, grid=self.FULL_GRID,
                                         first_position_cars=self.cars,
                                         screen_size=self.BOARD_SIZE)
                        self.card.card_solver()
                        self.previous_moves.append(self.card.first_position)
                        self.card.save_card()
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if not self.car_move_click(pos):
                        for block in self.FULL_GRID:
                            if pos[0] - block[0] < self.BLOCK_SIZE and \
                                    pos[1] - block[1] < self.BLOCK_SIZE:
                                pos = block
                                break
                        if not self.cars:
                            if pos[0] > self.FULL_GRID[-7][0]:
                                pos = (self.FULL_GRID[-7][0], pos[1])
                            pos = (pos[0], self.FULL_GRID[(self.ROWS_COLUMNS_COUNT // 2) - 1][1])
                            self.cars.append(Car(2, self.BLOCK_SIZE, 'red', True))
                            self.place_car_pos(self.cars[0], pos)
                        else:
                            new_car = Car(length, self.BLOCK_SIZE, next(car_colors), horizontal)
                            if self.place_car_pos(new_car, pos):
                                self.cars.append(new_car)
            screen.fill((0, 0, 0))
            self.GUI.render_msg(screen, gui_txt, "bottom")
            self.blit_cars(screen)
            pygame.display.flip()
