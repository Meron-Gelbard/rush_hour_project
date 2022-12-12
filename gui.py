import pygame
import pygame

class RushHourGui:

    def create_btn(self, text, height):
        font = pygame.font.SysFont('Ariel', height, bold=True)
        label = font.render(text, False, (255, 255, 255))
        label_rect = label.get_rect()
        btn = pygame.image.load('img/button.png')
        btn = pygame.transform.scale(btn, (label_rect.width + 10, label_rect.height + 10))
        return [btn, label, text, None]

    def __init__(self, screen_size):
        shift = 12
        self.button_height = 25

        self.btn_info = [{"pos": (shift, shift), "text": ' Load Card '},
                    {"pos": (screen_size - shift*12, shift), "text": ' Create Card '},
                    {"pos": (screen_size - shift*13, screen_size - shift - self.button_height), "text": ' Play Solution '},
                    {"pos": (shift, screen_size - shift - self.button_height), "text": ' Undo '},
                    {"pos": (screen_size / 2.3, screen_size - shift - self.button_height*3), "text": ' Restart '}
                    ]

        self.btns = [self.create_btn(btn['text'], self.button_height) for btn in self.btn_info]

    def btn_press(self, btn):
        size = btn[0].get_size()
        btn[0] = pygame.image.load('img/button_pressed.png')
        btn[0] = pygame.transform.scale(btn[0], size)

    def btn_release(self, btn):
        size = btn[0].get_size()
        btn[0] = pygame.image.load('img/button.png')
        btn[0] = pygame.transform.scale(btn[0], size)

    def blit_btns(self, screen):
        for i in range(len(self.btn_info)):
            btn_rect = self.btns[i][0].get_rect()
            btn_rect.topleft = self.btn_info[i]['pos']
            lbl_rect = self.btns[i][1].get_rect()
            lbl_rect.topleft = (self.btn_info[i]['pos'][0] + 5, self.btn_info[i]['pos'][1] + 5)
            self.btns[i][3] = btn_rect
            screen.blit(self.btns[i][0], btn_rect)
            screen.blit(self.btns[i][1], lbl_rect)

    def blit_status(self, moves_count, min_moves, screen):
        font = pygame.font.SysFont('Ariel', self.button_height, bold=True)
        label = font.render(f'moves: {moves_count - 1} / {min_moves - 1} (shortest)', False, (255, 255, 255))
        bg_size = (label.get_width() + 15, label.get_height() + 15)
        bg = pygame.Surface(bg_size)
        bg.fill((0, 0, 0))
        label_rect = label.get_rect()
        label_rect.center = (screen.get_width() / 2, screen.get_width() - self.button_height * 1.5)
        bg_xy = (label_rect.topleft[0] - 7.5, label_rect.topleft[1] - 7.5)
        screen.blit(bg, bg_xy)
        screen.blit(label, label_rect)

