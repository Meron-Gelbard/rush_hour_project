
class Level:
    def __init__(self, grid, rows_columns, first_position_cars, screen_size):
        self.moving_cars = first_position_cars
        self.first_position = [car.car_rect.topleft for car in self.moving_cars]
        self.moves_history = []
        self.grid = grid
        self.board_edge = screen_size
        self.rows_columns = rows_columns
        self.possible = False
        self.red_car_width = first_position_cars[0].width
        self.moves_2_exit = 0

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

    def check_possible_moves(self, position):
        # add repositiong cars by priority per check .. if top priority move to start of moves list
        # priority: always move first cars blocking the red path
        # priority: move first cars blocking the exit
        possible_moves = []
        for i in range(0, len(position)):
            if not position[i].horizontal:
                if position[i].move('up', self.grid, self.get_free_places(position), self.rows_columns):
                    possible_moves.append([car.car_rect.topleft for car in position])
                    position[i].move('down', self.grid, self.get_free_places(position), self.rows_columns)
                if position[i].move('down', self.grid, self.get_free_places(position), self.rows_columns):
                    possible_moves.append([car.car_rect.topleft for car in position])
                    position[i].move('up', self.grid, self.get_free_places(position), self.rows_columns)

            elif position[i].horizontal:
                if position[i].move('left', self.grid, self.get_free_places(position), self.rows_columns):
                    possible_moves.append([car.car_rect.topleft for car in position])
                    position[i].move('right', self.grid, self.get_free_places(position), self.rows_columns)
                if position[i].move('right', self.grid, self.get_free_places(position), self.rows_columns):
                    possible_moves.append([car.car_rect.topleft for car in position])
                    position[i].move('left', self.grid, self.get_free_places(position), self.rows_columns)
        return possible_moves

    def level_solver(self):
        queue = [self.first_position]
        moves_dictionary = {}
        visited = []
        end = None
        # queue for creating moves_dict - dictionary of moves relationships:
        while len(queue) > 0:
            for current_pos in queue:
                queue.remove(current_pos)
                if current_pos not in visited:
                    visited.append(current_pos)
                    for i in range(0, len(self.moving_cars)):
                        self.moving_cars[i].car_rect.topleft = current_pos[i]
                    possible_moves = self.check_possible_moves(self.moving_cars)
                    moves_dictionary[visited.index(current_pos)] = [move for move in possible_moves]
                    if self.moving_cars[0].car_rect.right >= self.board_edge - 10:
                        end = current_pos
                        self.possible = True
                        queue = []
                        break
                    for move in possible_moves:
                        if move not in queue and move not in visited:
                            queue.append(move)

        if self.possible:
            reversed_dict = {}
            dict_keys = [key for key in moves_dictionary.keys()]
            dict_keys.reverse()
            for key in dict_keys:
                reversed_dict[key] = moves_dictionary[key]

            start = self.first_position
            # finding shortest route in revers search through moves_dict:
            route = [end]
            next_move = end
            for parent_move_index, optional_moves in reversed_dict.items():
                if next_move == start:
                    route.append(visited[parent_move_index])
                    break
                if next_move in optional_moves:
                    route.append(visited[parent_move_index])
                    next_move = visited[parent_move_index]
            for i in range(0, len(self.moving_cars)):
                self.moving_cars[i].car_rect.topleft = self.first_position[i]
            route.reverse()
            self.moves_2_exit = len(route) - 1
            return route


# TODO: make level solver shorter by dicovering last move that clears the red car path to exit.
#  if path is clear stop adding possible moves!!
# TODO:  If removing any piece has no effect on the solution, then the puzzle is not minimal and is discarded.
#  -- check in visited states if a car wasn't ever moved. if so, discard this game map as its not minimal!!





