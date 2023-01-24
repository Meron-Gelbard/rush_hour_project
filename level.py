from _collections import deque
import json

class Level:
    def __init__(self, grid, rows_columns, first_position_cars, screen_size):
        self.moving_cars = first_position_cars
        self.first_position = [car.car_rect.topleft for car in self.moving_cars]
        self.grid = grid
        self.board_edge = screen_size
        self.rows_columns = rows_columns
        self.solvable = False
        self.moves_2_exit = 0
        self.route = None

    def save_level(self):
        cars = []
        for car in self.moving_cars:
            cars.append(
                {
                    "length": car.length,
                    "block_width": car.width,
                    "horizontal": car.horizontal,
                    "topleft_xy": car.car_rect.topleft,
                    "grid_index": self.grid.index(car.car_rect.topleft)
                }
            )
        cars[1:].sort(key=lambda x: (x['grid_index']))
        level_save_params = {
            "moves_2_exit": self.moves_2_exit,
            "solution_route": self.route,
            "grid": self.grid,
            "rows_columns": self.rows_columns,
            "cars": cars,
            "screen_size": self.board_edge,
            "minimal": self.level_is_minimal()
        }

        with open("solved_levels.json", "r") as levels_data:
            save = True
            saved_levels = json.load(levels_data)
            for level in saved_levels:
                if level['cars'] == level_save_params['cars']:
                    save = False
                    print('Level already exists in database.')
                    break
        if save:
            saved_levels.append(level_save_params)
            with open("solved_levels.json", "w") as file:
                json.dump(saved_levels, file)
            print('solvable level saved to json!')

    def get_free_places(self, cars):
        used_places = []
        for car in cars:
            index = self.grid.index(car.car_rect.topleft)
            if car.horizontal:
                for i in range(0, car.length):
                    i = index + self.rows_columns * i
                    if i <= len(self.grid) - 1:
                        used_places.append(self.grid[i])
                    else:
                        break
            elif not car.horizontal:
                for i in range(0, car.length):
                    i = index + i
                    if i <= len(self.grid) - 1:
                        used_places.append(self.grid[i])
                    else:
                        break
        free_places = [place for place in self.grid if place not in used_places]
        return free_places

    def get_possible_moves(self, current_pos):
        def car_blocking_red(car, red_car):
            if car.car_rect.bottom > red_car.car_rect.top >= car.car_rect.top:
                if car.car_rect.left >= red_car.car_rect.right:
                    return True
                else:
                    return False

        possible_moves = []
        for i in range(0, len(current_pos)):
            if not current_pos[i].horizontal:
                if current_pos[i].move('up', self.grid, self.get_free_places(current_pos), self.rows_columns):
                    possible_moves.append([car.car_rect.topleft for car in current_pos])
                    current_pos[i].move('down', self.grid, self.get_free_places(current_pos), self.rows_columns)
                    if car_blocking_red(current_pos[i], current_pos[0]):
                        possible_moves.insert(0, possible_moves.pop(-1))
                if current_pos[i].move('down', self.grid, self.get_free_places(current_pos), self.rows_columns):
                    possible_moves.append([car.car_rect.topleft for car in current_pos])
                    current_pos[i].move('up', self.grid, self.get_free_places(current_pos), self.rows_columns)
                    if car_blocking_red(current_pos[i], current_pos[0]):
                        possible_moves.insert(0, possible_moves.pop(-1))

            elif current_pos[i].horizontal:
                if current_pos[i].move('left', self.grid, self.get_free_places(current_pos), self.rows_columns):
                    possible_moves.append([car.car_rect.topleft for car in current_pos])
                    current_pos[i].move('right', self.grid, self.get_free_places(current_pos), self.rows_columns)
                if current_pos[i].move('right', self.grid, self.get_free_places(current_pos), self.rows_columns):
                    possible_moves.append([car.car_rect.topleft for car in current_pos])
                    current_pos[i].move('left', self.grid, self.get_free_places(current_pos), self.rows_columns)

        return iter(possible_moves)

    def level_solver(self):
        print("started solver")
        def red_path_cleared():
            red_path = []
            for space in self.grid:
                if space[1] == self.moving_cars[0].car_rect.topleft[1] and space[0] >= self.moving_cars[0].car_rect.right:
                    red_path.append(space)
            for space in red_path:
                if space not in self.get_free_places(self.moving_cars):
                    return False
            return True

        moves_queue = deque([self.first_position])
        moves_dictionary = {}
        visited = []
        end = None
        while len(moves_queue) > 0:
            current_pos = moves_queue.popleft()
            if current_pos not in visited:
                visited.append(current_pos)
                for i in range(0, len(self.moving_cars)):
                    self.moving_cars[i].car_rect.topleft = current_pos[i]
                if red_path_cleared():
                    self.moving_cars[0].car_rect.left += self.moving_cars[0].width
                    next_in_red_path = [car.car_rect.topleft for car in self.moving_cars]
                    moves_dictionary[visited.index(current_pos)] = [next_in_red_path]
                    moves_queue.clear()
                    moves_queue.append(next_in_red_path)
                    if self.moving_cars[0].car_rect.right >= self.board_edge - 10:
                        end = next_in_red_path
                        self.solvable = True
                        break
                else:
                    possible_moves = self.get_possible_moves(self.moving_cars)
                    moves_dictionary[visited.index(current_pos)] = [move for move in possible_moves]
                    for move in possible_moves:
                        if move not in moves_queue and move not in visited:
                            moves_queue.append(move)

        if self.solvable:
            reversed_dict = {}
            dict_keys = [key for key in moves_dictionary.keys()]
            dict_keys.reverse()
            for key in dict_keys:
                reversed_dict[key] = moves_dictionary[key]
            start = self.first_position
            self.route = [end]
            next_move = end
            for parent_move_index, optional_moves in reversed_dict.items():
                if next_move == start:
                    self.route.append(visited[parent_move_index])
                    break
                if next_move in optional_moves:
                    self.route.append(visited[parent_move_index])
                    next_move = visited[parent_move_index]
            for i in range(0, len(self.moving_cars)):
                self.moving_cars[i].car_rect.topleft = self.first_position[i]
            self.route.reverse()
            self.moves_2_exit = len(self.route) - 1
        print("finished solver")

    def level_is_minimal(self):
        for car in range(1, len(self.first_position)):
            car_moved = False
            for pos in self.route:
                if self.first_position[car] != pos[car]:
                    car_moved = True
            if not car_moved:
                return False
        return True

