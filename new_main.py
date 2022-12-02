import pygame
import sys
import pygame.locals as K
from board import Board
pygame.init()

screen_size = 800
screen = pygame.display.set_mode((screen_size, screen_size))
board = Board(size=screen_size, level=4, rows_columns=6)
clock = pygame.time.Clock()
clock.tick(70)

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
                        screen.fill((0, 0, 0))
                        board.blit_cars(screen)
                        print(f"solved in {len(solution_route)-1} moves.")
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


# TODO: implement yield function in recurssion functions. good for restarting function without variables reset!! (????)
# TODO: implement map building by level argument. calculate level by number of moves required.
# TODO: implement priority check on route building i n level solver.
# TODO: implement solution player as function and play through Thread so that can be in interrupted.
# TODO: try to create level creation log for future saving of generated maps.
# TODO: try implementing recurssion error handling instead of attrmpt counts for production of more complex maps.
# TODO: improve GUI: "please wait" messages, grid background, exit sign, board boarder, level request input, undo move button,
# move counter display, level reset button. solution player button, work on car images.

