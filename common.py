import pygame
from random import randint
from time import process_time

debug = False
show_menu = False
do_parity_check = True

cell_size = 40
music_volume = 0.01
music_counter = 0
animation_k = 0.03

next_turn_flag = False


def check_parity(sprites):
    for i in sprites:
        if i.rect.x == i.rect.y == 0:
            print('PARITY CHECK FAILED', i)
            i.kill()


# Класс ассетов для игры (содержит пути ко всем файлам, создан для удобства разработки)
class Assets:
    def __init__(self):
        # Музыка
        self.music1 = 'assets/sounds/music/music1.mp3'
        self.music2 = 'assets/sounds/music/music2.mp3'
        self.music3 = 'assets/sounds/music/music3.mp3'
        self.music4 = 'assets/sounds/music/music4.mp3'

        # Звуковые эффекты
        self.sfx_click = 'assets/sounds/sfx/click.wav'
        self.sfx_hurt = 'assets/sounds/sfx/hurt.wav'

        # Текстуры строений и природных структур
        self.texture_city1 = 'assets/textures/terrain/city1.png'
        self.texture_city2 = 'assets/textures/terrain/city2.png'
        self.texture_mountain = 'assets/textures/terrain/mountain.png'

        # Текстуры юнитов
        self.texture_unit_warrior_1 = 'assets/textures/units/warrior/warrior1.png'
        self.texture_unit_warrior_2 = 'assets/textures/units/warrior/warrior2.png'

        # Дефолтные (служебные) текстуры
        self.texture_skybox = 'assets/textures/skybox.png'
        self.texture_missing = 'assets/textures/missing.png'


assets = Assets()


def do_music_routine():
    global music_counter
    music = [assets.music2, assets.music3, assets.music4, assets.music1]
    music_counter += 1
    if music_counter >= len(music):
        music_counter = 0
    dprint('MUSIC UPDATE', music_counter, music[music_counter])
    pygame.mixer.music.load(music[music_counter])
    pygame.mixer.music.play()


def window_modes(resolution=(1200, 800)):
    return resolution, pygame.RESIZABLE


def dprint(*args):
    if debug:
        print('[' + str(process_time()) + ']', *args)


def load_image(name, color_key=None):
    try:
        texture = pygame.image.load(name).convert()
        image = pygame.transform.scale(texture, (cell_size, cell_size))
    except FileNotFoundError:
        texture = pygame.image.load(assets.texture_missing).convert()
        image = pygame.transform.scale(texture, (cell_size, cell_size))

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def chance(percentage):
    i = randint(0, 100)
    if i < percentage:
        return True
    else:
        return False


random = randint


def draw_hud(player):
    pass


class Player:
    def __init__(self, manager, name, stars):
        self.name = name
        self.manager = manager
        self.units = []
        self.cities = []
        self.stars = stars
        self.star_per_turn = stars
        self.total_stars = 0

    def add_unit(self, unit):
        self.units.append(unit)

    def add_city(self, city):
        self.cities.append(city)

    def get_units(self):
        return self.units

    def remove_city(self, name):
        self.cities = [i for i in self.cities if i.name != name]

    def tick(self):
        if self.stars > self.total_stars:
            self.total_stars = self.stars


class City(pygame.sprite.Sprite):
    def __init__(self, player, texture, group, *smth):
        super().__init__(*smth)

        self.player = player

        self.id = 1

        self.texture = texture
        self.image = load_image(texture)

        self.population = 0
        self.remove_cost = 0

        dprint('CITY NEW', texture, *group, self)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0

        self.add(group)

    def update(self):
        dprint('CITY UPDATE', self)

    def set_pos(self, x, y):
        self.rect.x, self.rect.y = x, y
        dprint('CITY SET', self, self.rect.x, self.rect.y)

    def resize(self):
        self.image = load_image(self.texture)
        self.rect = self.image.get_rect()


class TurnManager:

    def __init__(self, player_count, board, city_count, sprite_group):

        self.players = [Player(self, str('Player ' + str(i + 1)), 0) for i in range(player_count)]
        self.board = board

        self.turn = 0

        self.city_count = city_count

        self.current_player = self.players[self.turn]
        self.generate_cities(sprite_group)

    def next_turn(self):
        print('Next turn')
        self.turn += 1
        if self.turn >= len(self.players):
            self.turn = 0
        self.current_player = self.players[self.turn]

    def tick(self):
        global next_turn_flag
        if next_turn_flag:
            self.next_turn()
            next_turn_flag = False
        self.board.tick()
        self.current_player.tick()

    def generate_cities(self, sprite_group):
        for i in self.players:
            self.players.index(i)
            textures = [assets.texture_city1, assets.texture_city2]
            for _ in range(self.city_count // len(self.players)):
                flag = True
                while flag:
                    x, y = random(0, len(self.board.board) - 1), random(0, len(self.board.board) - 1)
                    if self.board.get_biome(x, y) != 0:
                        city = City(i, textures[self.players.index(i)], sprite_group)
                        i.add_city(city)
                        self.board.board[x][y][1] = [city]
                        flag = False

    def add_unit(self, unit, cords):
        self.current_player.add_unit(unit)
        self.board.add_unit(unit, *cords)


class MainMenu:
    def show_menu(self):
        if show_menu:
            if input("выбор карты (1)") == 1:
                return 'assets/map1.csv'
