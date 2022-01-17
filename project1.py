import pygame
import os
import sys
import time

from pygame.constants import QUIT

pygame.init()

clock = pygame.time.Clock()

WIDTH, HEIGHT = 1200, 700
FPS = 60
INTRO_FPS = 20
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Santa fight!')

MENU_WIN_FILL = '#DCDDD8'

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

SANTA_WIDTH, SANTA_HEIGHT = 150, 125

SANTA1_HIT_SNOWBALL = pygame.USEREVENT + 1
SANTA2_HIT_SNOWBALL = pygame.USEREVENT + 2
SANTA1_HIT_PRESENT = pygame.USEREVENT + 3
SANTA2_HIT_PRESENT = pygame.USEREVENT + 4
SANTA1_HIT_PROJECTILE = pygame.USEREVENT + 5
SANTA2_HIT_PROJECTILE = pygame.USEREVENT + 6

MAX_SNOWBALLS = 5
MAX_PRESENTS = 2
MAX_PROJECTILE = 1

SNOWBALL_WIDTH, SNOWBALL_HEIGHT = 70, 70
PROJECTILE_WIDTH, PROJECTILE_HEIGHT = 100, 70

PRESENT_WIDTH, PRESENT_HEIGHT = 90, 90

WINNER_FONT = pygame.font.SysFont('Helvetica', 100)
# ROUND_FONT = pygame.font.SysFont('Arial', 50)

VELOCITY = 7
PROJECTILE_VELOCITY = 10
SNOWBALL_VELOCITY = 7
PRESENT_VELOCITY = 3

SANTA_IMAGE = pygame.image.load(os.path.join(
    r'C:\Users\bayar\OneDrive\Desktop\Techne club Python\New year project\Santa snowball fight\Assets\santa.png'))
SANTA1 = pygame.transform.scale(SANTA_IMAGE, (SANTA_WIDTH, SANTA_HEIGHT))

SANTA2_IMAGE = pygame.image.load(os.path.join(
    r'C:\Users\bayar\OneDrive\Desktop\Techne club Python\New year project\Santa snowball fight\Assets\gaigui_santa.png'))
SANTA2 = pygame.transform.scale(
    SANTA2_IMAGE, (SANTA_WIDTH, SANTA_HEIGHT))


SNOWBALL_IMAGE = pygame.image.load(os.path.join(
    r'C:\Users\bayar\OneDrive\Desktop\Techne club Python\New year project\Santa snowball fight\Assets\Snowball.png'))
SNOWBALL = pygame.transform.scale(
    SNOWBALL_IMAGE, (SNOWBALL_WIDTH, SNOWBALL_HEIGHT))

PROJECTILE1_IMAGE = pygame.image.load(
    os.path.join(r'C:\Users\bayar\OneDrive\Desktop\Techne club Python\New year project\Santa snowball fight\Assets\ice projectile.png'))
PROJECTILE1 = pygame.transform.scale(
    PROJECTILE1_IMAGE, (PROJECTILE_WIDTH, PROJECTILE_HEIGHT))

PROJECTILE2_IMAGE = pygame.image.load(
    os.path.join(r'C:\Users\bayar\OneDrive\Desktop\Techne club Python\New year project\Santa snowball fight\Assets\ice projectile.png'))
PROJECTILE2 = pygame.transform.flip(PROJECTILE1, True, False)

PRESENT_GREEN_IMAGE = pygame.image.load(
    os.path.join(r'C:\Users\bayar\OneDrive\Desktop\Techne club Python\New year project\Santa snowball fight\Assets\present_green.png'))
PRESENT_GREEN = pygame.transform.scale(
    PRESENT_GREEN_IMAGE, (PRESENT_WIDTH, PRESENT_HEIGHT))

PRESENT_RED_IMAGE = pygame.image.load(
    os.path.join(r'C:\Users\bayar\OneDrive\Desktop\Techne club Python\New year project\Santa snowball fight\Assets\present_red.png'))
PRESENT_RED = pygame.transform.scale(
    PRESENT_RED_IMAGE, (PRESENT_WIDTH, PRESENT_HEIGHT))

BACKGROUND_IMAGE = pygame.image.load(
    os.path.join(r'C:\Users\bayar\OneDrive\Desktop\Techne club Python\New year project\Santa snowball fight\Assets\background_img.jpg'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

PLAYER_HEALTH = 500

DAMAGE = 10


WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED_OTHER = '#D74B4B'

button_font = pygame.font.SysFont('Helvetica', 30)


class Button:
    def __init__(self, button1_text, button2_text, button_width, button_height, button1_pos, button2_pos, button_elevation):
        self.pressed1 = False
        self.pressed2 = False
        self.elevation = button_elevation
        self.dynamic1_elevation = button_elevation
        self.dynamic2_elevation = button_elevation
        self.original1_y_pos = button1_pos[1]
        self.original2_y_pos = button2_pos[1]

        self.top1_rect = pygame.Rect(
            button1_pos, (button_width, button_height))
        self.top1_color = '#475F77'

        self.top2_rect = pygame.Rect(
            button2_pos, (button_width, button_height))
        self.top2_color = '#475F77'

        self.bottom1_rect = pygame.Rect(
            button1_pos, (button_width, button_elevation))
        self.bottom1_color = '#354B5E'

        self.bottom2_rect = pygame.Rect(
            button2_pos, (button_width, button_height))
        self.bottom2_color = '#354B5E'

        self.text1_surf = button_font.render(button1_text, True, '#FFFFFF')
        self.text1_rect = self.text1_surf.get_rect(
            center=self.top1_rect.center)

        self.text2_surf = button_font.render(button2_text, True, '#FFFFFF')
        self.text2_rect = self.text2_surf.get_rect(
            center=self.top2_rect.center)

    def draw(self):
        # elevation logic
        self.top1_rect.y = self.original1_y_pos - self.dynamic1_elevation
        self.text1_rect.center = self.top1_rect.center

        self.top2_rect.y = self.original2_y_pos - self.dynamic2_elevation
        self.text2_rect.center = self.top2_rect.center

        self.bottom1_rect.midtop = self.top1_rect.midtop
        self.bottom1_rect.height = self.top1_rect.height + self.dynamic1_elevation

        self.bottom2_rect.midtop = self.top2_rect.midtop
        self.bottom2_rect.height = self.top2_rect.height + self.dynamic2_elevation

        pygame.draw.rect(WIN, self.bottom1_color,
                         self.bottom1_rect, border_radius=12)

        pygame.draw.rect(WIN, self.top1_color,
                         self.top1_rect, border_radius=12)

        pygame.draw.rect(WIN, self.bottom2_color,
                         self.bottom2_rect, border_radius=12)

        pygame.draw.rect(WIN, self.top2_color,
                         self.top2_rect, border_radius=12)

        WIN.blit(self.text1_surf, self.text1_rect)
        self.check1_click()

        WIN.blit(self.text2_surf, self.text2_rect)
        self.check2_click()

    def check1_click(self):
        mouse1_pos = pygame.mouse.get_pos()
        if self.top1_rect.collidepoint(mouse1_pos):
            # self.top1_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic1_elevation = 0
                self.pressed1 = True
            else:
                self.dynamic1_elevation = self.elevation
                if self.pressed1 == True:
                    time.sleep(0.5)
                    main()
                    self.pressed1 = False
        else:
            self.dynamic1_elevation = self.elevation
            # self.top1_color = '#475F77'

    def check2_click(self):
        mouse2_pos = pygame.mouse.get_pos()
        if self.top2_rect.collidepoint(mouse2_pos):
            # self.top2_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic2_elevation = 0
                self.pressed2 = True
            else:
                self.dynamic2_elevation = self.elevation
                if self.pressed2 == True:
                    pygame.event.post(pygame.event.Event(QUIT))
                    self.pressed2 = False
        else:
            self.dynamic_elevation = self.elevation
            # self.top1_color = '#475F77'


def draw_window(santa1, santa2, snowball1, snowball2, SANTA1_HEALTH, SANTA2_HEALTH, present1, present2, projectile1, projectile2):
    WIN.blit(BACKGROUND, (0, 0))

    pygame.draw.rect(WIN, CYAN, BORDER)

    WIN.blit(SANTA1, (santa1.x, santa1.y))
    WIN.blit(SANTA2, (santa2.x, santa2.y))

    for sb in snowball1:
        WIN.blit(SNOWBALL, sb)

    for sb in snowball2:
        WIN.blit(SNOWBALL, sb)

    for pr in present1:
        WIN.blit(PRESENT_RED, pr)

    for pr in present2:
        WIN.blit(PRESENT_GREEN, pr)

    for po in projectile1:
        WIN.blit(PROJECTILE1, po)

    for po in projectile2:
        WIN.blit(PROJECTILE2, po)

    pygame.draw.rect(WIN, RED, (25, 25, PLAYER_HEALTH, 25))
    pygame.draw.rect(WIN, GREEN, (25, 25, SANTA1_HEALTH, 25))

    pygame.draw.rect(WIN, RED, (675, 25, PLAYER_HEALTH, 25))
    pygame.draw.rect(WIN, GREEN, (675 + PLAYER_HEALTH -
                     SANTA2_HEALTH, 25, SANTA2_HEALTH, 25))

    '''draw_santa1_round = ROUND_FONT.render(str(santa1_win), 1, BLACK)
    WIN.blit(draw_santa1_round, (550, 55))

    draw_santa2_round = ROUND_FONT.render(str(santa2_win), 1, BLACK)
    WIN.blit(draw_santa2_round, (625, 55))'''
    pygame.display.update()


def santa1_movement(keys_presed, santa1):
    if keys_presed[pygame.K_a] and santa1.x - VELOCITY > 0:
        santa1.x -= VELOCITY
    elif keys_presed[pygame.K_w] and santa1.y - VELOCITY > 55:
        santa1.y -= VELOCITY
    elif keys_presed[pygame.K_d] and santa1.x + VELOCITY + santa1.width < BORDER.x:
        santa1.x += VELOCITY
    elif keys_presed[pygame.K_s] and santa1.y + VELOCITY + santa1.height < HEIGHT:
        santa1.y += VELOCITY


def santa2_movement(keys_presed, santa2):
    if keys_presed[pygame.K_LEFT] and santa2.x - VELOCITY > BORDER.x + BORDER.width:
        santa2.x -= VELOCITY
    elif keys_presed[pygame.K_UP] and santa2.y - VELOCITY > 55:
        santa2.y -= VELOCITY
    elif keys_presed[pygame.K_RIGHT] and santa2.x + VELOCITY + santa2.width < WIDTH:
        santa2.x += VELOCITY
    elif keys_presed[pygame.K_DOWN] and santa2.y + VELOCITY + santa2.height < HEIGHT:
        santa2.y += VELOCITY


def handle_snowball(snowball1, snowball2, santa1, santa2):
    for sb in snowball1:
        sb.x += SNOWBALL_VELOCITY
        if santa2.colliderect(sb):
            pygame.event.post(pygame.event.Event(SANTA2_HIT_SNOWBALL))
            snowball1.remove(sb)
        elif sb.x > WIDTH:
            snowball1.remove(sb)

    for sb in snowball2:
        sb.x -= SNOWBALL_VELOCITY
        if santa1.colliderect(sb):
            pygame.event.post(pygame.event.Event(SANTA1_HIT_SNOWBALL))
            snowball2.remove(sb)
        elif sb.x < 0:
            snowball2.remove(sb)


def handle_present(present1, present2, santa1, santa2):
    for pr in present1:
        pr.x += PRESENT_VELOCITY
        if santa2.colliderect(pr):
            pygame.event.post(pygame.event.Event(SANTA2_HIT_PRESENT))
            present1.remove(pr)
        elif pr.x > WIDTH:
            present1.remove(pr)

    for pr in present2:
        pr.x -= PRESENT_VELOCITY
        if santa1.colliderect(pr):
            pygame.event.post(pygame.event.Event(SANTA1_HIT_PRESENT))
            present2.remove(pr)
        elif pr.x < 0:
            present2.remove(pr)


def handle_projectile(projectile1, projectile2, santa1, santa2):
    for po in projectile1:
        po.x += PROJECTILE_VELOCITY
        if santa2.colliderect(po):
            pygame.event.post(pygame.event.Event(SANTA2_HIT_PROJECTILE))
            projectile1.remove(po)
        elif po.x > WIDTH:
            projectile1.remove(po)

    for po in projectile2:
        po.x -= PROJECTILE_VELOCITY
        if santa1.colliderect(po):
            pygame.event.post(pygame.event.Event(SANTA1_HIT_PROJECTILE))
            projectile2.remove(po)
        elif po.x < 0:
            projectile2.remove(po)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, BLUE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() /
             2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def intro():
    button = Button('Play', 'Quit', 400, 100, (400, 250), (400, 400), 8)
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        WIN.fill(MENU_WIN_FILL)
        largeText = pygame.font.SysFont('Helvetica', 115)
        WIN.blit(largeText.render('Santa Fight', 1, RED_OTHER), (360, 50))
        button.draw()
        pygame.display.update()
        clock.tick(INTRO_FPS)


def main():
    pygame.init()

    santa1 = pygame.Rect(100, 400, SANTA_WIDTH, SANTA_HEIGHT)
    santa2 = pygame.Rect(1000, 400, SANTA_WIDTH, SANTA_HEIGHT)

    snowball1 = []
    snowball2 = []
    present1 = []
    present2 = []
    projectile1 = []
    projectile2 = []

    SANTA1_HEALTH = 500
    SANTA2_HEALTH = 500

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and len(snowball1) < MAX_SNOWBALLS:
                    sb = pygame.Rect(santa1.x + santa1.width // 2, santa1.y +
                                     santa1.height // 4, SNOWBALL_WIDTH, SNOWBALL_HEIGHT)
                    snowball1.append(sb)

                if event.key == pygame.K_KP1 and len(snowball2) < MAX_SNOWBALLS:
                    sb = pygame.Rect(
                        santa2.x, santa2.y + santa2.height // 4, SNOWBALL_WIDTH, SNOWBALL_HEIGHT)
                    snowball2.append(sb)

                if event.key == pygame.K_g and len(present1) < MAX_PRESENTS:
                    pr = pygame.Rect(santa1.x + santa1.width // 2, santa1.y +
                                     santa1.height // 4, PRESENT_WIDTH, PRESENT_HEIGHT)
                    present1.append(pr)

                if event.key == pygame.K_KP2 and len(present2) < MAX_PRESENTS:
                    pr = pygame.Rect(
                        santa2.x, santa2.y + santa2.height // 4, PRESENT_WIDTH, PRESENT_HEIGHT)
                    present2.append(pr)

                if event.key == pygame.K_h and len(projectile1) < MAX_PROJECTILE:
                    pt = pygame.Rect(santa1.x + santa1.width // 2, santa1.y +
                                     santa1.height // 4, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
                    projectile1.append(pt)

                if event.key == pygame.K_KP3 and len(projectile2) < MAX_PROJECTILE:
                    pt = pygame.Rect(
                        santa2.x, santa2.y + santa2.height // 4, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
                    projectile2.append(pt)

            if event.type == SANTA1_HIT_SNOWBALL:
                SANTA1_HEALTH -= 10

            if event.type == SANTA2_HIT_SNOWBALL:
                SANTA2_HEALTH -= 10

            if event.type == SANTA1_HIT_PRESENT:
                SANTA1_HEALTH -= 50

            if event.type == SANTA2_HIT_PRESENT:
                SANTA2_HEALTH -= 50

            if event.type == SANTA1_HIT_PROJECTILE:
                SANTA1_HEALTH -= 80

            if event.type == SANTA2_HIT_PROJECTILE:
                SANTA2_HEALTH -= 80

        winner_text = ""
        # santa1_win = 0
        # santa2_win = 0
        if SANTA2_HEALTH <= 0:
            # santa1_win += 1
            winner_text = "Player 1 wins!"
            SANTA1_HEALTH = 500
            SANTA2_HEALTH = 500

        if SANTA1_HEALTH <= 0:
            # santa2_win += 1
            winner_text = "Player 2 wins!"
            SANTA1_HEALTH = 500
            SANTA2_HEALTH = 500

        keys_pressed = pygame.key.get_pressed()
        santa1_movement(keys_pressed, santa1)
        santa2_movement(keys_pressed, santa2)
        handle_snowball(snowball1, snowball2, santa1, santa2)
        handle_present(present1, present2, santa1, santa2)
        handle_projectile(projectile1, projectile2, santa1, santa2)
        draw_window(santa1, santa2, snowball1, snowball2, SANTA1_HEALTH,
                    SANTA2_HEALTH, present1, present2, projectile1, projectile2)

        if winner_text != '':
            draw_winner(winner_text)

    main()


if __name__ == '__main__':
    intro()
    main()
