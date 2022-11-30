import pygame
import sys
import pygame.locals as K
from board import Board
pygame.init()

screen_size = 800
screen = pygame.display.set_mode((screen_size, screen_size))
board = Board(size=screen_size, level=4, rows_columns=6)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K.K_RETURN:
                solvable = False
                while not solvable:
                    board.create_spaces()
                    board.create_cars()
                    board.create_random_level(screen)
                    solution_route = board.level.level_solver()
                    if board.level.possible:
                        solvable = True
                        print('found solvable map!')
                        screen.fill((0, 0, 0))
                        board.blit_cars(screen)
                        print(len(solution_route))
                        for move in solution_route:
                            print(move)
                    else:
                        print('unsolvable...moving on')
            if event.key == K.K_p:
                for move in solution_route:
                    for i in range(len(board.cars)):
                        board.cars[i].car_rect.topleft = move[i]
                    screen.fill((0, 0, 0))
                    board.blit_cars(screen)
                    pygame.display.flip()
                    pygame.time.wait(1000)

        if event.type == pygame.MOUSEBUTTONDOWN:
            board.check_mouse_click(pygame.mouse.get_pos(), screen)


    pygame.display.flip()


# TODO: implement yield function in recurssion functions. good for restarting function without variables reset!!


''' 
que starts with first position
while the que is not empty:
    check from start position all possible one-move positions available and add them to the que if they are not there already and not in visited list
    add to dictionary: key of current position with list of possible next positions ass value
    add current possition to visited list
    remove current possition from que
    move up in the que and check again
    if que is empty or no next possitions available finish while loop

start and end positions given
add start to rout list as first item
make end position as first target value
iterate through key,value of above dictionary:
    if the target == start position:
        break loop
    if target is in value list:
        append the key to rout list
        make key as target
        
reverse rout for solution and count moves as totall positions in rout


'''