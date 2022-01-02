import csv
from pprint import pprint

import pygame

# общие функции
import common

# Классы природных обьектов(горы итд)
import resources

# Классы юнитов
import units

# Классы ресурсов

from common import dprint

sprites = pygame.sprite.Group()


class Board:
    # создание поля
    def __init__(self, width, height, world):
        self.width = width
        self.height = height

        # загрузка карты
        dprint('MAP LOAD', world)
        self.board = []
        self.generate_map(world)
        pprint(self.board)
        dprint('MAP LOADED')

        # значения по умолчанию

        self.screen = screen
        self.paused = False
        self.render_world = True

        # биомы              Океан      Луга       Пустыня    Снег       Тайга      Горы
        self.ground_tiles = ['#00bfff', '#7cfc00', '#fce883', '#fffafa', '#228b22', '#808080']

        # скайбокс
        dprint('SKYBOX LOAD assets/skybox.png')
        self.skybox = pygame.image.load('assets/skybox.png').convert()

        self.resize_routine()

        # центрируемся
        self.x = screen.get_size()[0] / 2 - len(self.board) / 2 * common.cell_size
        self.y = common.cell_size

    # загрузка карты
    def generate_map(self, world):
        # открываем CSV
        with open(world, encoding="utf8") as csvfile:
            # чистим карту
            self.board = []
            # читаем карту
            reader = csv.reader(csvfile, delimiter=',')
            for index, row in enumerate(reader):
                self.board.append([])
                for tile in row:
                    biomes = {'o': 0, 'p': 1, 'd': 2, 's': 3, 't': 4, 'm': 5}
                    biome = biomes[tile[0]]

                    # загрузка юнита или структуры итд согласно карте
                    if tile[1] == 'm':  # обьект на тайле - вторая буква в коде тайла - t[m]
                        sprite = [resources.Mountain(biome, sprites)]

                    # ...

                    else:
                        sprite = []

                    # упаковка спрайта в клетку
                    # формат тайла: [id_биома, [что стоит], id_ресурса]
                    self.board[index].append([biome, sprite, 0])

            self.board = list(zip(*self.board))

            pprint(self.board)

    def get_biome(self, x, y):
        return self.board[x][y][0]

    def get_units(self, x, y):
        return self.board[x][y][1]

    # настройка внешнего вида
    def resize_routine(self):
        common.cell_size = screen.get_size()[1] // (len(self.board) + 3)
        self.skybox = pygame.transform.scale(self.skybox.convert(), screen.get_size())
        for i in sprites.sprites():
            i.resize()
        self.key_handler_tick()

    def render(self):
        self.screen.blit(self.skybox, (0, 0))
        for x in range(self.width):
            for y in range(self.height):
                dx = x * common.cell_size + self.x
                dy = y * common.cell_size + self.y
                biome = self.get_biome(x, y)

                if self.render_world:
                    # Цвет тайла
                    color = pygame.Color(self.ground_tiles[biome])
                    pygame.draw.rect(self.screen, color, (dx, dy, common.cell_size, common.cell_size))

                    # Цвет обводки тайла
                    hsv = color.hsva
                    color.hsva = (hsv[0], hsv[1], hsv[2] - 10, hsv[3])

                    # рисуем обводку
                    pygame.draw.rect(self.screen, color, (dx, dy, common.cell_size, common.cell_size), 1)

                for i in self.get_units(x, y):
                    i.set_pos(dx, dy)

        for x in range(self.width):
            dx = x * common.cell_size + self.x
            dy = self.height * common.cell_size + self.y
            ground = pygame.Color('#663300')

            pygame.draw.rect(self.screen, ground, (dx, dy, common.cell_size, common.cell_size))

            # Цвет обводки тайла
            hsv = ground.hsva
            ground.hsva = (hsv[0], hsv[1], hsv[2] - 10, hsv[3])

            # рисуем обводку
            pygame.draw.rect(self.screen, ground, (dx, dy, common.cell_size, common.cell_size), 1)

        sprites.update()
        sprites.draw(self.screen)
        pygame.display.flip()

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.get_click(event.pos)
                elif event.button == 3:
                    self.paused = not self.paused
            if event.type == pygame.KEYDOWN:
                if event.unicode == ' ':
                    self.paused = not self.paused
            if event.type == pygame.VIDEORESIZE:
                self.resize_routine()

        self.key_handler_tick()
        self.render()

    def key_handler_tick(self):
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        offset = common.cell_size // 4 if common.cell_size // 4 >= 0 else 1
        if keys[pygame.K_s]:
            self.y += offset
        if keys[pygame.K_a]:
            self.x -= offset
        if keys[pygame.K_w]:
            self.y -= offset
        if keys[pygame.K_d]:
            self.x += offset
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit(0)
        if keys[pygame.K_f]:
            pygame.display.toggle_fullscreen()

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.x) // common.cell_size
        y = (mouse_pos[1] - self.y) // common.cell_size
        if x < 0 or x >= self.width:
            return None
        if y < 0 or y >= self.height:
            return None
        return x, y

    def on_click(self, cell):
        try:
            self.board[cell[0]][cell[1]][0] = 5
        except TypeError:
            pass


pygame.init()
resolution = (720, 480)
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
while True:
    menu = common.MainMenu()
    game_map = menu.show_menu()
    del menu
    # поле 5 на 7
    board = Board(16, 16, game_map)
    clock = pygame.time.Clock()
    while True:
        board.tick()
        clock.tick(30)
