import pygame
import sys
import pygame.locals as K
from board import Board
from gui import RushHourGui

pygame.init()

screen_size = 800
screen = pygame.display.set_mode((screen_size, screen_size))
rush_hour_gui = RushHourGui(screen_size)
board = Board(size=screen_size, level=4, rows_columns=6, gui=rush_hour_gui)
clock = pygame.time.Clock()

while True:
    # game loop - constantly updatinf status, re-rendering elements and listening to events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K.K_RETURN:
                board.create_random_card(screen)
                print(f"solved in {board.card.moves_2_exit} moves.")
                print(f"Level is minial? {board.card.level_is_minimal()}")
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_press = False
            for btn in rush_hour_gui.btns:
                if btn[3].collidepoint(pygame.mouse.get_pos()):
                    rush_hour_gui.btn_press(btn)
                    board.btn_funcs[btn[2]](screen)
                    button_press = True
            if board.listening and not button_press:
                board.car_move_click(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONUP:
            for btn in rush_hour_gui.btns:
                rush_hour_gui.btn_release(btn)

    screen.fill((0, 0, 0))
    board.blit_cars(screen)

    rush_hour_gui.blit_btns(screen, board)
    if board.red_is_out:
        board.listening = False
        rush_hour_gui.render_msg(screen, "Red car is out! Great!", "center")
    try:
        rush_hour_gui.blit_status(moves_count=len(board.previous_moves), min_moves=len(board.card.route), screen=screen)
    except AttributeError:
        pass
    pygame.display.flip()
