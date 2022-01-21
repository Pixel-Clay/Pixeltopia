import pygame
import sys

import common

window = pygame.display.set_mode((1200, 800))
screen = pygame.Surface(pygame.display.get_window_size())
info = pygame.Surface(pygame.display.get_window_size())


class Sprite:
    def __init__(self, x, y, filename):
        self.x = x
        self.y = y
        self.bitmap = pygame.image.load(filename)
        self.bitmap.set_colorkey((0, 0, 0))

    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))


class Menu:
    def __init__(self, points):
        self.points = points

    def render(self, surface, font, num_points):
        for i in self.points:
            if num_points == i[5]:
                surface.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                surface.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self, sfx):
        global done, world
        font_menu = pygame.font.Font(common.assets.font, 50)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        point = 0
        prev = 0
        while done:
            info.fill('#FFAE9A')
            screen.fill('#FFAE9A')

            mp = pygame.mouse.get_pos()
            for i in self.points:
                if i[0] < mp[0] < i[0] + 155 and i[1] < mp[1] < i[1] + 50:
                    point = i[5]
            self.render(screen, font_menu, point)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif e.key == pygame.K_UP:
                        if point > 0:
                            point -= 1
                    elif e.key == pygame.K_DOWN:
                        if point < len(self.points) - 1:
                            point += 1
                    elif e.key == pygame.K_RETURN:
                        if point == 0:
                            done = False
                            world = 0
                        elif point == 1:
                            done = False
                            world = 1
                        elif point == 2:
                            exit()

                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if point == 0:
                        done = False
                        world = 0
                    elif point == 1:
                        done = False
                        world = 1
                    elif point == 2:
                        exit()

                if prev != point:
                    sfx[3].play()
                    prev = point
                    # elif point == 2:
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
    points = [(10, size[1] - 400, 'Карта 1', '#F50E69', '#29073E', 0),
              (10, size[1] - 300, 'Карта 2', '#F50E69', '#29073E', 1),
              (10, size[1] - 200, 'Выход', '#F50E69', '#29073E', 2),
              (0, 150, 'The Battle of Pixeltopia', '#510F58', '#510F58', 3)
              ]

    global done
    done = True
    game = Menu(points)
    game.menu(sfx)
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
    sfx[2].play()
    return world


def show_end_screen(score, player):
    pass
