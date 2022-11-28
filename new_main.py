import pygame
import sys
import pygame.locals as K
from board import Board

pygame.init()

screen_size = 800
screen = pygame.display.set_mode((screen_size, screen_size))

board = Board(size=screen_size, level=2, rows_columns=6)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K.K_RETURN:
                screen.fill((0, 0, 0))
                print('---------- New ---------')
                board.create_spaces()
                board.create_cars()
                board.cars_random_placement(screen)

    pygame.display.flip()


# TODO: horizontal cars musent be in way of red car
# TODO: car movement check if there is a center point around that isnt collided with  car_rects