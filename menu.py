import pygame
import sys

import common

window = pygame.display.set_mode((1200, 800))
screen = pygame.Surface(pygame.display.get_window_size())
info = pygame.Surface(pygame.display.get_window_size())


class Sprite:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap = pygame.image.load(filename)
        self.bitmap.set_colorkey((0, 0, 0))

    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))


class Menu:
    def __init__(self, punkts, sfx):
        self.punkts = punkts
        self.sfx = sfx

    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self, flag=False):
        global done, world
        self.flag = flag
        font_menu = pygame.font.Font(common.assets.font, 50)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        punkt = 0
        prev_punkt = 0
        while done:
            info.fill('#FFAE9A')
            screen.fill('#FFAE9A')
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if i[0] < mp[0] < i[0] + 155 and i[1] < mp[1] < i[1] + 50:
                    punkt = i[5]
            self.render(screen, font_menu, punkt)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if flag:
                        if e.key == pygame.K_RETURN:
                            done = False
                    else:
                        if e.key == pygame.K_ESCAPE:
                            sys.exit()
                        if e.key == pygame.K_UP:
                            if punkt > 0:
                                punkt -= 1
                        if e.key == pygame.K_DOWN:
                            if punkt < len(self.punkts) - 1:
                                punkt += 1
                        if e.key == pygame.K_RETURN:
                            if punkt == 0:
                                done = False
                                world = 0
                            if punkt == 1:
                                done = False
                                world = 1
                            elif punkt == 2:
                                exit()
                            elif punkt == 6:
                                done = False
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if flag:
                        done = False
                    else:
                        if punkt == 0:
                            done = False
                            world = 0
                        if punkt == 1:
                            done = False
                            world = 1
                        elif punkt == 2:
                            exit()
                if prev_punkt != punkt:
                    self.sfx[3].play()
                    prev_punkt = punkt
                    # elif punkt == 2:
                    #     s = pg.image.load('regu.png')
                    #     window.blit(s, info)
            window.blit(info, (0, 0))
            window.blit(screen, (0, 30))
            pygame.display.flip()


pygame.font.init()

size = pygame.display.get_window_size()

done = True
world = 0


def show_menu(sfx):
    punkts = [(10, size[1] - 400, 'Карта 1', '#F50E69', '#29073E', 0),
              (10, size[1] - 300, 'Карта 2', '#F50E69', '#29073E', 1),
              (10, size[1] - 200, 'Выход', '#F50E69', '#29073E', 2),
              (2, 10, 'The Battle of Pixeltopia', '#510F58', '#510F58', 3)
              ]

    global done, world
    done = True
    game = Menu(punkts, sfx)
    game.menu()
    while done:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quit()

        window.fill('#FFAE9A')
        screen.fill('#FFAE9A')
        info.fill('#FFAE9A')

        window.blit(info, (0, 0))
        pygame.display.flip()
    pygame.display.flip()
    return world


def show_end_screen(player, score, sfx):
    punkts = [(350, 95, str(score) + ' очков', '#29073E', '#29073E', 6),
              (50, 45, u'Выиграл игрок ' + player, '#29073E', '#29073E', 6),
              (300, 300, u'Выйти из игры', '#F50E69', '#29073E', 6)
              ]

    global done
    done = True
    game = Menu(punkts, sfx)
    game.menu(flag=True)
    while done:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quit()

        window.fill('#FFAE9A')
        screen.fill('#FFAE9A')
        info.fill('#FFAE9A')

        window.blit(info, (0, 0))
        pygame.display.flip()
    quit()
    pygame.display.flip()

