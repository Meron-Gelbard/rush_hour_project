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
                board.create_random_level(screen)
                board.blit_cars(screen)
                print(f"solved in {board.level.moves_2_exit} moves.")
                print(f"Level is minial? {board.level.level_is_minimal()}")
            if event.key == K.K_p:
                board.solution_player(screen)
            if event.key == K.K_l:
                level = board.get_random_level()
                board.load_level(screen, level)
            if event.key == K.K_r:
                board.restart_level(screen)
            if event.key == K.K_u:
                board.undo_move(screen)

        if event.type == pygame.MOUSEBUTTONDOWN:
            board.car_move_click(pygame.mouse.get_pos(), screen)

    pygame.display.flip()


# TODO: implement yield function in recurssion functions. good for restarting function without variables reset!! (????)
# TODO: implement map building by level argument. calculate level by number of moves required.
# TODO: try to create level creation log for future saving of generated maps.
# TODO: try implementing recurssion error handling instead of attempt counts for production of more complex maps.??
# TODO: improve GUI: "please wait" messages, grid background, exit sign, board boarder, level request input, undo move button,
# move counter display, level reset button. solution player button, work on car images.