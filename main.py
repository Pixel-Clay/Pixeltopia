import csv

import pygame

# общие функции
import common

# Классы природных обьектов(горы итд)
import resources

# Классы юнитов
import units

import menu

# Классы ресурсов
from common import dprint

sprites = pygame.sprite.Group()

units.yeet()


class Board:
    # создание поля
    def __init__(self, width, height, world):
        self.width = width
        self.height = height

        # загрузка карты
        dprint('MAP LOAD', world)
        self.board = []
        self.generate_map(world)
        dprint(self.board)
        dprint('MAP LOADED')

        # значения по умолчанию
        self.screen = screen
        self.render_world = True

        self.prev_selected = (0, 0)
        self.selected = (0, 0)

        self.player_units = []

        self.manager = None

        # биомы              Океан      Луга       Пустыня    Снег       Тайга      Горы
        self.ground_tiles = ['#00bfff', '#7cfc00', '#fce883', '#fffafa', '#228b22', '#808080']

        # скайбокс
        dprint('SKYBOX LOAD')
        self.skybox = pygame.image.load(common.assets.texture_skybox).convert()

        self.resize_routine()

        # центрируемся
        self.x = screen.get_size()[0] / 2 - len(self.board) / 2 * common.cell_size
        self.y = common.cell_size

    # загрузка карты
    def generate_map(self, world):
        # открываем CSV
        with open('assets/map1.csv', encoding="utf8") as csvfile:
            # чистим карту
            self.board = []

            # читаем карту
            reader = csv.reader(csvfile, delimiter=',')
            for index, row in enumerate(reader):
                if index == 0:
                    self.player_count = int(str(row[0])[0])
                    continue
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
                    # формат тайла: [id_биома, [что стоит], id_ресурса, выбран]
                    self.board[index - 1].append([biome, sprite, 0, False])

            self.board = list(zip(*self.board))

    def get_biome(self, x, y):
        return self.board[x][y][0]

    def get_selected(self, x, y):
        return self.board[x][y][3]

    def get_units(self, x, y):
        return self.board[x][y][1]

    def add_unit(self, unit, x, y):
        self.board[x][y][1].append(unit)

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

                thiccness = 1

                if self.render_world:
                    # Цвет тайла
                    color = pygame.Color(self.ground_tiles[biome])
                    pygame.draw.rect(self.screen, color, (dx, dy, common.cell_size, common.cell_size))

                    if self.get_selected(x, y):
                        color = '#FE8692'
                        thiccness = 3
                        size = common.cell_size - 1

                    elif (x, y) in self.player_units:
                        color = '#8b00ff'
                        thiccness = 2
                        size = common.cell_size - 1

                    else:
                        # Цвет обводки тайла
                        hsv = color.hsva
                        color.hsva = (hsv[0], hsv[1], hsv[2] - 10, hsv[3])
                        size = common.cell_size

                    # рисуем обводку
                    pygame.draw.rect(self.screen, color, (dx, dy, size, size), thiccness)

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
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.get_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    common.next_turn_flag = True
                elif event.key == pygame.K_e:
                    self.manager.harvest(self.selected)
            if event.type == pygame.VIDEORESIZE:
                self.resize_routine()
            if event.type == pygame.constants.USEREVENT:
                common.do_music_routine()

        if self.selected != self.prev_selected:
            self.deselect_selected(self.prev_selected)
        self.prev_selected = self.selected

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

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        dprint('FUNC get_click', cell)
        self.on_click(cell)

    def deselect_selected(self, cell):
        self.board[cell[0]][cell[1]][3] = False

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.x) // common.cell_size
        y = (mouse_pos[1] - self.y) // common.cell_size
        if x < 0 or x >= self.width:
            return None
        if y < 0 or y >= self.height:
            return None
        return int(x), int(y)

    def on_click(self, cell):
        try:
            self.board[cell[0]][cell[1]][3] = not self.board[cell[0]][cell[1]][3]
            sfx_click.play()
            self.selected = cell
        except TypeError:
            dprint('TYPE ERROR on_click', cell)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)
sfx_click = pygame.mixer.Sound(common.assets.sfx_click)
sfx_click.set_volume(0.4)

sfx_hurt = pygame.mixer.Sound(common.assets.sfx_hurt)
sfx_hurt.set_volume(0.4)

sfx_star = pygame.mixer.Sound(common.assets.sfx_pickupStar)
sfx_star.set_volume(0.4)

resolution = (1200, 800)
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
pygame.display.set_caption('Pixeltopia')
while True:
    if common.show_menu:
        menu.show_menu()

    board = Board(16, 16, None)

    turn_manager = common.TurnManager(2, board, 4, (sfx_star, sfx_hurt), sprites)

    clock = pygame.time.Clock()

    pygame.mixer.music.load(common.assets.music1)
    pygame.mixer.music.set_volume(common.music_volume)
    pygame.mixer.music.play()
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)

    textures = [common.assets.texture_unit_warrior_1, common.assets.texture_unit_warrior_2]

    turn_manager.add_unit(units.BaseUnit(turn_manager.current_player, textures, sprites, (1, 0)), (1, 0))
    turn_manager.next_turn()
    turn_manager.add_unit(units.BaseUnit(turn_manager.current_player, textures, sprites, (1, 1)), (1, 1))

    while True:
        turn_manager.tick()
        if common.do_parity_check:
            common.check_parity(sprites)
        clock.tick(30)
