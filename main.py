import csv
from pprint import pprint

import pygame

# Классы природных обьектов(горы итд)
import structures

# Классы юнитов
import units

# Классы ресурсов
import structures

from common import dprint, cell_size

sprites = pygame.sprite.Group()


class Board:
    # создание поля
    def __init__(self, width, height, world, cell_size):
        self.width = width
        self.height = height

        # загрузка карты
        dprint('MAP LOAD', world)
        self.board = []
        self.generate_map(world)
        pprint(self.board)
        dprint('MAP LOADED')

        # значения по умолчанию
        self.x = 300
        self.y = 30
        self.screen = screen
        self.cell_size = cell_size
        self.paused = False
        self.render_world = True

        # биомы              Океан      Луга       Пустыня    Снег       Тайга      Горы
        self.ground_tiles = ['#00bfff', '#7cfc00', '#fce883', '#fffafa', '#228b22', '#808080']

        # скайбокс
        dprint('SKYBOX LOAD assets/skybox.png')
        skybox = pygame.image.load('assets/skybox.png')
        self.skybox = pygame.transform.scale(skybox, self.screen.get_size())

    # загрузка карты
    def generate_map(self, world):
        # открывает CSVшку
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
                        sprite = structures.Mountain(biome, sprites)

                    # ...

                    # упаковка спрайта в клетку
                    entities = [sprite] if tile[1] != 'p' else []

                    # формат тайла: [id_биома, [что стоит], id_ресурса]
                    self.board[index].append([biome, entities, 0])

            self.board = list(zip(*self.board))

    def get_biome(self, x, y):
        return self.board[x][y][0]

    def get_units(self, x, y):
        return self.board[x][y][1]

    # настройка внешнего вида
    def set_view(self, x=10, y=10, cell_size=30):
        self.x = x
        self.y = y
        self.cell_size = cell_size

    def render(self):
        for x in range(self.width):
            for y in range(self.height):
                dx = x * self.cell_size + self.x
                dy = y * self.cell_size + self.y
                biome = self.get_biome(x, y)

                if self.render_world:
                    # Цвет тайла
                    color = pygame.Color(self.ground_tiles[biome])
                    pygame.draw.rect(self.screen, color, (dx, dy, self.cell_size, self.cell_size))

                    # Цвет обводки тайла
                    hsv = color.hsva
                    color.hsva = (hsv[0], hsv[1], hsv[2] - 10, hsv[3])

                    # рисуем обводку
                    pygame.draw.rect(self.screen, color, (dx, dy, self.cell_size, self.cell_size), 1)

                for i in self.get_units(x, y):
                    i.set_pos(dx, dy)

        for x in range(self.width):
            dx = x * self.cell_size + self.x
            dy = self.height * self.cell_size + self.y
            ground = pygame.Color('#663300')

            pygame.draw.rect(self.screen, ground, (dx, dy, self.cell_size, self.cell_size))

            # Цвет обводки тайла
            hsv = ground.hsva
            ground.hsva = (hsv[0], hsv[1], hsv[2] - 10, hsv[3])

            # рисуем обводку
            pygame.draw.rect(self.screen, ground, (dx, dy, self.cell_size, self.cell_size), 1)

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

        self.do_movement()
        self.screen.blit(self.skybox, (0, 0))
        self.render()
        pygame.display.flip()

    def do_movement(self):
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            self.y += 10
        if keys[pygame.K_a]:
            self.x -= 10
        if keys[pygame.K_w]:
            self.y -= 10
        if keys[pygame.K_d]:
            self.x += 10
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit(0)
        if keys[pygame.K_f]:
            pygame.display.toggle_fullscreen()
        self.render()

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.x) // self.cell_size
        y = (mouse_pos[1] - self.y) // self.cell_size
        if x < 0 or x >= self.width:
            return None
        if y < 0 or y >= self.height:
            return None
        return x, y

    def on_click(self, cell):
        try:
            self.board[cell[0]][cell[1]][0] = 5
        except Exception:
            pass
        self.render()


pygame.init()

screen = pygame.display.set_mode((1200, 800))

# поле 5 на 7
board = Board(16, 16, 'assets/map1.csv', cell_size)
clock = pygame.time.Clock()
while True:
    board.tick()
    clock.tick(30)
