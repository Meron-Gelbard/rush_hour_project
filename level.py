
class Level:
    def __init__(self, grid, rows_columns, first_position_cars, screen_size):
        # first positioning should be a set of cars from Board!!
        self.first_positioning = first_position_cars
        self.moves_history = []
        self.moves_count = 0
        self.grid = grid
        self.board_edge = screen_size
        self.rows_columns = rows_columns
        self.possible = False

    def check_possible_moves(self, position, free_places):
        # position is a set of cars!!
        # free_places are constant so cars move relevant to same starting position!!
        possible_moves = []
        print([car.car_rect.topleft for car in position])
        for i in range(0, len(position)):
            checked_pos = [car for car in position]
            if not checked_pos[i].horizontal:
                checked_pos[i].car_rect.topleft = checked_pos[i].move('up', self.grid, free_places, self.rows_columns)
                possible_moves.append(checked_pos)
                print([car.car_rect.topleft for car in checked_pos])

                checked_pos = [car for car in position]
                checked_pos[i].car_rect.topleft = checked_pos[i].move('down', self.grid, free_places, self.rows_columns)
                possible_moves.append(checked_pos)
                print([car.car_rect.topleft for car in checked_pos])

            elif checked_pos[i].horizontal:
                checked_pos[i].car_rect.topleft = checked_pos[i].move('left', self.grid, free_places, self.rows_columns)
                possible_moves.append(checked_pos)
                print([car.car_rect.topleft for car in checked_pos])

                checked_pos = [car for car in position]
                checked_pos[i].car_rect.topleft = checked_pos[i].move('right', self.grid, free_places, self.rows_columns)
                possible_moves.append(checked_pos)
                print([car.car_rect.topleft for car in checked_pos])

        return possible_moves


    def level_solver(self):

        def get_free_places(cars):
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

        queue = [self.first_positioning]
        moves_dictionary = {}
        visited = []
        end = None

        # queue for creating moves_dict - dictionary of moves relationships:
        while len(queue) > 0:
            for current_pos in queue:
                if current_pos[0].car_rect.right == self.board_edge:
                    end = current_pos
                    self.possible = True
                    print('found end')
                    break
                if current_pos not in visited:
                    visited.append(current_pos)
                    possible_moves = self.check_possible_moves(current_pos, get_free_places(current_pos))
                    moves_dictionary[visited.index(current_pos)] = [move for move in possible_moves]
                    print(moves_dictionary)
                    for move_option in possible_moves:
                        if move_option == current_pos:
                            print('shit')
                        # if move_option not in queue:
                        #     queue.append(move_option)
                    queue.remove(current_pos)
                    print(len(queue))

        print('visited:\n', visited)

        # finding shortest route in revers search through moves_dict:
        route = [end]
        next_move = end
        for parent_move_index, optional_moves in moves_dictionary.items():
            if next_move == self.first_positioning:
                route.append(visited[parent_move_index])
                route.append(self.first_positioning)
                break
            if next_move in optional_moves:
                route.append(visited[parent_move_index])
                next_move = visited[parent_move_index]
        route.reverse()
        return route









