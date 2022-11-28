import pygame
import sys
import random
import pygame.locals as K

car_colors = ['red', 'blue', 'cyan', 'pink', 'orange', 'green']

pygame.init()
class Car:
    def __init__(self, length, img_color):
        self.horizontal = random.choice([True, False])
        self.length = length
        if self.horizontal:
            self.size = (130 * length, 130)
        else:
            self.size = (130, 130 * length)
        img_color = f"img/{img_color}_brick.png"
        self.car = pygame.image.load(img_color)
        self.car = pygame.transform.scale(self.car, self.size)
        self.car_rect = self.car.get_rect()


def place_car_pos(car, places):
    try:
        placement = random.choice(places)
    except IndexError:
        return None
    except TypeError:
        return None
    car.car_rect.topleft = placement
    if car.horizontal:
        index = places.index(placement)
        try:
            used_places = [places[index + 6 * i] for i in range(1, car.length + 1)]
            places = [place for place in places if place not in used_places]
            places.remove(placement)
            return places
        except IndexError:
            places.remove(placement)
            return places
    elif not car.horizontal:
        index = places.index(placement)
        try:
            used_places = [places[index+i] for i in range(1, car.length + 1)]
            places = [place for place in places if place not in used_places]
            places.remove(placement)
            return places
        except IndexError:
            places.remove(placement)
            return places

def randomize_cars(screen_size):
    def check(this_car, car_rects):
        if this_car.car_rect.bottom > screen_size:
            return False
        elif this_car.car_rect.right > screen_size:
            return False
        elif this_car.car_rect.collidelist(car_rects) != -1:
            return False
        else:
            return True

    cars = [Car(2, random.choice(car_colors)) for _ in range(4)]
    for _ in range(2):
        cars.append(Car(3, random.choice(car_colors)))
    cars.sort(key=lambda x: int(x.length), reverse=True)

    car_rects = [car.car_rect for car in cars]

    values = [i for i in range(-130, screen_size+1, 130)]
    places = []

    for x in range(1, 7):
        for y in range(1, 7):
            places.append((values[x], values[y]))

    for car in cars:
        while True:
            places = place_car_pos(car, places)
            if places == None or len(places) < 2:
                screen.fill((0, 0, 0))
                randomize_cars(screen_size)
            car_rects = [car_u.car_rect for car_u in cars if car_u != car]
            passed = check(car, car_rects)
            if passed:
                screen.blit(car.car, car.car_rect)
                break

screen_size = 780
screen = pygame.display.set_mode((screen_size, screen_size))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K.K_RETURN:
                screen.fill((0, 0, 0))
                try:
                    randomize_cars(screen_size)
                except RecursionError:
                    break

    pygame.display.flip()








# position_map = [car.position for car in cars]
# create surfaces from positions map
# map_history = [position_map, position_map, position_map, position_map]

# def car_movment(postion_map):
#     for car in cars:
#         if car.free:
#             # if position map not in history:
#                 # move car to free spot
#                 # if red car is out - finish game!
#                 # if not:
#                     # new position_map
#                     # save position map to history
#                     # call self with new position map
#             # but if position map is in history:
#             #     continue