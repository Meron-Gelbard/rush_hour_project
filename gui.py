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
        self.move_count = 0
        self.min_moves = 0
        shift = 12
        button_height = 25

        self.btn_info = [{"pos": (shift, shift), "text": ' Load Card '},
                    {"pos": (screen_size - shift*12, shift), "text": ' Create Card '},
                    {"pos": (screen_size - shift*13, screen_size - shift - button_height), "text": ' Play Solution '},
                    {"pos": (shift, screen_size - shift - button_height), "text": ' Undo '},
                    {"pos": (screen_size / 2.3, screen_size - shift - button_height*3), "text": ' Restart '}
                    ]

        self.btns = [self.create_btn(btn['text'], button_height) for btn in self.btn_info]
        print(self.btns)

    def blit_btns(self, screen):
        for i in range(len(self.btn_info)):
            btn_rect = self.btns[i][0].get_rect()
            btn_rect.topleft = self.btn_info[i]['pos']
            lbl_rect = self.btns[i][1].get_rect()
            lbl_rect.topleft = (self.btn_info[i]['pos'][0] + 5, self.btn_info[i]['pos'][1] + 5)
            self.btns[i][3] = btn_rect
            screen.blit(self.btns[i][0], btn_rect)
            screen.blit(self.btns[i][1], lbl_rect)
