
class Level:
    def __init__(self, grid, rows_columns, first_position_cars, screen_size):
        self.moving_cars = first_position_cars
        self.first_position = [car.car_rect.topleft for car in self.moving_cars]
        self.grid = grid
        self.board_edge = screen_size
        self.rows_columns = rows_columns
        self.solvable = False
        self.red_car_width = first_position_cars[0].width
        self.moves_2_exit = 0
        self.route = None

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

    def check_possible_moves(self, current_pos):
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

        return possible_moves

    def level_solver(self):
        def red_path_cleared():
            red_path = []
            for space in self.grid:
                if space[1] == self.moving_cars[0].car_rect.topleft[1] and space[0] >= self.moving_cars[0].car_rect.right:
                    red_path.append(space)
            for space in red_path:
                if space not in self.get_free_places(self.moving_cars):
                    return False
            return True

        queue = [self.first_position]
        moves_dictionary = {}
        visited = []
        end = None
        while len(queue) > 0:
            for current_pos in queue:
                remaining = len(queue)
                queue.remove(current_pos)
                if current_pos not in visited:
                    visited.append(current_pos)
                    for i in range(0, len(self.moving_cars)):
                        self.moving_cars[i].car_rect.topleft = current_pos[i]
                    if red_path_cleared():
                        self.moving_cars[0].car_rect.left += self.moving_cars[0].width
                        next_in_red_path = [car.car_rect.topleft for car in self.moving_cars]
                        moves_dictionary[visited.index(current_pos)] = [next_in_red_path]
                        queue.append(next_in_red_path)
                        # queue = [next_in_red_path]
                        if self.moving_cars[0].car_rect.right >= self.board_edge - 10:
                            end = next_in_red_path
                            self.solvable = True
                            queue = []
                            break
                    else:
                        possible_moves = self.check_possible_moves(self.moving_cars)
                        moves_dictionary[visited.index(current_pos)] = [move for move in possible_moves]
                        for move in possible_moves:
                            if move not in queue and move not in visited:
                                queue.append(move)
                        if len(queue) < remaining:
                            return None

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


# TODO:  If removing any piece has no effect on the solution, then the puzzle is not minimal and is discarded.
#  -- check in visited states if a car wasn't ever moved. if so, discard this game map as its not minimal!!





