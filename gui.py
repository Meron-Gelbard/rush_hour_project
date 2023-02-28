import pygame
import pygame
import pygame.locals as K
import sys


class RushHourGui:

    def create_btn(self, text, height):
        font = pygame.font.SysFont('Ariel', height, bold=True)
        label = font.render(text, False, (255, 255, 255))
        label_rect = label.get_rect()
        btn = pygame.image.load('img/button.png')
        btn = pygame.transform.scale(btn, (label_rect.width + 10, label_rect.height + 10))
        return [btn, label, text, btn.get_rect()]

    def __init__(self, screen_size):
        shift = 12
        self.button_height = 25
        self.btn_info = [{"pos": (shift, shift), "text": ' Load Card '},
                         {"pos": (screen_size - shift * 12, shift), "text": ' Create Card '},
                         {"pos": (screen_size - shift * 13, screen_size - shift - self.button_height),
                          "text": ' Play Solution '},
                         {"pos": (shift, screen_size - shift - self.button_height), "text": ' Undo '},
                         {"pos": (screen_size / 2.3, screen_size - shift - self.button_height * 3), "text": ' Restart '}
                         ]

        self.btns = [self.create_btn(btn['text'], self.button_height) for btn in self.btn_info]
        self.flash_message = pygame.font.SysFont('Ariel', 40, bold=True)
        self.message_text = ''
        self.user_input_txt = ''

    def btn_press(self, btn):
        size = btn[0].get_size()
        btn[0] = pygame.image.load('img/button_pressed.png')
        btn[0] = pygame.transform.scale(btn[0], size)

    def btn_release(self, btn):
        size = btn[0].get_size()
        btn[0] = pygame.image.load('img/button.png')
        btn[0] = pygame.transform.scale(btn[0], size)

    def blit_btns(self, screen, board):
        x = 0
        if board.card == None:
            self.render_msg(screen, "Welcome to the RushHour Game!", "center")
            x = 3
        for i in range(len(self.btn_info) - x):
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

    def render_msg(self, screen, msg_txt, position):
        self.message_text = msg_txt
        msg_pos = {'center': (screen.get_size()[0] / 2, screen.get_size()[0] / 2),
                   'bottom': (screen.get_size()[0] / 2, screen.get_size()[0] - 30)}

        label = self.flash_message.render(self.message_text, False, (255, 255, 255))
        label_rect = label.get_rect()

        label_rect.center = msg_pos[position]
        bg_size = (label.get_width() + 20, label.get_height() + 20)
        bg = pygame.Surface(bg_size)
        bg.fill((0, 0, 0))
        bg_xy = (label_rect.topleft[0] - 10, label_rect.topleft[1] - 10)
        screen.blit(bg, bg_xy)
        screen.blit(label, label_rect)

    def render_user_input(self, screen):
        label = self.flash_message.render(self.user_input_txt, False, (255, 255, 255))
        label_rect = label.get_rect()
        size = screen.get_size()[0]
        label_rect.center = (size / 2, size / 2 + label_rect.height * 1.5)
        bg_size = (label.get_width() + 20, label.get_height() + 20)
        bg = pygame.Surface(bg_size)
        bg.fill((0, 0, 0))
        bg_xy = (label_rect.topleft[0] - 10, label_rect.topleft[1] - 10)
        screen.blit(bg, bg_xy)
        screen.blit(label, label_rect)

    def user_input(self, screen):
        finished = False
        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K.K_BACKSPACE and len(self.user_input_txt) > 0:
                        self.user_input_txt = self.user_input_txt[:-1]
                    elif event.key == K.K_RETURN:
                        finished = True
                        try:
                            self.user_input_txt = int(self.user_input_txt)
                            return self.user_input_txt
                        except Exception:
                            self.user_input_txt = '#'
                    else:
                        if len(self.user_input_txt) < 2:
                            self.user_input_txt = self.user_input_txt + event.unicode
                if event.type == pygame.QUIT:
                    sys.exit()
            screen.fill((0, 0, 0))
            self.render_msg(screen, 'Please enter difficulty level (1 - 5):', 'center')
            self.render_user_input(screen)
            pygame.display.flip()
