import pygame
from random import randint
from time import process_time
from datetime import datetime


import units

debug = False
show_menu = True
do_parity_check = True

cell_size = 40
music_volume = 0.2
music_counter = 0
animation_k = 0.03
turns = 15
start_stars = 2

next_turn_flag = False


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
        self.sfx_pickupStar = 'assets/sounds/sfx/pickupStar.wav'
        self.sfx_tick = 'assets/sounds/sfx/tick.wav'
        self.sfx_jump = 'assets/sounds/sfx/jump.wav'
        self.sfx_no = 'assets/sounds/sfx/blipNo.wav'
        self.sfx_next_turn = 'assets/sounds/sfx/nextTurn.wav'

        # Текстуры строений
        self.texture_city1 = 'assets/textures/terrain/city1.png'
        self.texture_city2 = 'assets/textures/terrain/city2.png'

        # Текстуры ресурсов
        self.texture_mountain = 'assets/textures/resources/mountain.png'
        self.texture_fruit = 'assets/textures/resources/fruit/fruit.png'
        self.texture_forest = 'assets/textures/resources/forest.png'
        self.texture_fox = 'assets/textures/resources/animal/fox.png'
        self.texture_whale = 'assets/textures/resources/animal/whale.png'
        self.texture_fish = 'assets/textures/resources/fruit/fish.png'



        # Текстуры юнитов
        self.texture_unit_warrior_1 = 'assets/textures/units/warrior/warrior1.png'
        self.texture_unit_warrior_2 = 'assets/textures/units/warrior/warrior2.png'

        self.texture_unit_archer_1 = 'assets/textures/units/archer/archer1.png'
        self.texture_unit_archer_2 = 'assets/textures/units/archer/archer2.png'

        self.texture_unit_swordsman_1 = 'assets/textures/units/swordsman/swordsman1.png'
        self.texture_unit_swordsman_2 = 'assets/textures/units/swordsman/swordsman2.png'

        self.texture_unit_mage_1 = 'assets/textures/units/mage/mage1.png'
        self.texture_unit_mage_2 = 'assets/textures/units/mage/mage2.png'

        # Дефолтные (служебные) текстуры
        self.texture_skybox = 'assets/textures/skybox.png'
        self.texture_missing = 'assets/textures/missing.png'

        # Шрифты
        self.font = 'assets/font/font.ttf'


assets = Assets()

pygame.font.init()
font = pygame.font.Font(assets.font, 14)


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


log = open('logs/' + str(datetime.now()) + '.txt', 'w')


def dprint(*args):
    if debug:
        print('[' + str(process_time()) + ']', *args)
    else:
        print('[' + str(process_time()) + ']', *args, file=log)


def check_parity(sprites):
    for i in sprites:
        if i.rect.x == i.rect.y == 0:
            dprint('PARITY CHECK FAILED', i)
            i.kill()


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


def draw_hud(manager, screen):
    player = font.render(str('Текущий игрок: ' + manager.current_player.name), True, '#FFFFFF')

    score = font.render(str('Звезды: ' + str(manager.current_player.stars) + '(' + str(
        manager.current_player.star_per_turn) + ' звезд в следующий ход)'), True, '#FFFFFF')

    cords = manager.board.selected
    stats = ''
    if len(manager.board.get_units(*cords)) > 0:
        resource = manager.board.get_units(*cords)[0]
        if resource.type == 'resource':
            stats = 'Ресурс, ' + str(resource.remove_cost) + ' звезды за снос, +' + str(
                resource.stars) + ' к очкам в следующий ход'
            if manager.current_player.stars >= resource.remove_cost:
                stats += ', можно снести'
        elif resource.type == 'unit':
            active = 'может ходить' if resource.is_active else 'уже сходил'
            stats = 'Юнит, ' + str(resource.health) + ' здоровья, ' + str(
                resource.attack_points) + ' очков атаки, ' + str(resource.defense_points) + ' очков защиты, ' + active
        elif resource.type == 'city':
            stats = 'Город игрока ' + str(resource.player.name)
    else:
        if manager.board.get_biome(*cords) == 0:
            stats = 'Океан, просто вода'
        else:
            stats = 'Равнина, просто равнина'

    turn = 'Ход ' + str(int(manager.current_turn / len(manager.players))) + '(из ' + str(
        int(manager.total_turns / len(manager.players))) + ')'
    turn_counter = font.render(turn, True, '#FFFFFF')
    stat_line = font.render(stats, True, '#FFFFFF')
    screen.blit(score, (5, 5))
    screen.blit(player, (5, 25))
    screen.blit(turn_counter, (5, 45))
    screen.blit(font.render('1 - Воин 2☆', True, '#FFFFFF'), (5, screen.get_size()[1] - 100))
    screen.blit(font.render('2 - Лучник 3☆', True, '#FFFFFF'), (5, screen.get_size()[1] - 80))
    screen.blit(font.render('3 - Мечник 3☆', True, '#FFFFFF'), (5, screen.get_size()[1] - 60))
    screen.blit(font.render('4 - Маг 4☆', True, '#FFFFFF'), (5, screen.get_size()[1] - 40))
    screen.blit(stat_line, (5, screen.get_size()[1] - 20))


class Player:
    def __init__(self, manager, name, stars):
        self.name = name
        self.manager = manager
        self.units = []
        self.cities = []
        self.stars = 0
        self.star_per_turn = stars
        self.total_stars = self.stars

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
    def __init__(self, player, texture, cords, group, *smth):
        super().__init__(*smth)

        self.type = 'city'

        self.cords = cords

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

    def __init__(self, player_count, turns, board, city_count, sfx, sprite_group):

        self.players = [Player(self, str('Player ' + str(i + 1)), start_stars) for i in range(player_count)]
        self.board = board
        self.sfx = sfx

        self.turn = 0

        self.total_turns = turns * player_count
        self.current_turn = 0

        self.city_count = city_count

        self.current_player = self.players[self.turn]
        self.generate_cities(sprite_group)
        self.board.manager = self

    def next_turn(self):
        self.sfx[6].play()
        self.current_turn += 1
        self.current_units_force_active()
        dprint('NEXT TURN')
        self.turn += 1
        if self.turn >= len(self.players):
            self.turn = 0
        self.current_player = self.players[self.turn]
        self.current_player.stars += self.current_player.star_per_turn
        dprint('PLAYER STARS', self.current_player.stars, 'stars')

    def current_units_force_active(self):
        for unit in self.current_player.units:
            unit.is_active = True

    def harvest(self, cords):
        def harvest_subroutine(resource):
            if resource.type == 'resource':
                for unit in self.current_player.units:
                    if unit.cords != cords:
                        unit.update_range()
                        if cords in unit.reachable_cells:
                            if self.current_player.stars >= resource.remove_cost:
                                self.sfx[1].play()
                                self.current_player.star_per_turn += resource.stars
                                self.current_player.stars -= resource.remove_cost
                                try:
                                    self.board.board[cords[0]][cords[1]][1][0].kill()
                                except IndexError:
                                    self.sfx[5].play()
                                self.board.board[cords[0]][cords[1]][1] = self.board.board[cords[0]][cords[1]][1][1::]
                            else:
                                self.sfx[5].play()
            elif resource.type == 'unit':
                for unit in self.current_player.units:
                    if unit.cords != cords:
                        unit.update_range()
                        if cords in unit.reachable_cells:
                            if unit.attack(*cords):
                                self.sfx[0].play()
                    else:
                        mouse = pygame.mouse.get_pos()
                        dest = self.board.get_cell(mouse)
                        unit.update_range()
                        if dest in unit.reachable_cells:
                            self.move_unit(cords, dest)
                        else:
                            self.sfx[5].play()

        if len(self.board.get_units(*cords)) > 0:
            resource = self.board.get_units(*cords)[0]
            if resource.type in ('resource', 'unit'):
                harvest_subroutine(resource)
            elif resource.type == 'city':
                if len(self.board.get_units(*cords)) >= 2:
                    resource = self.board.get_units(*cords)[1]
                    harvest_subroutine(resource)

    def is_city_current(self, cords):
        for city in self.current_player.cities:
            if city.cords == cords:
                return True
        return False

    def tick(self):
        global next_turn_flag
        if next_turn_flag:
            self.next_turn()
            next_turn_flag = False
        self.update_player_units()
        self.board.tick()
        self.current_player.tick()
        self.remove_dead()

    def update_player_units(self):
        reachable_cells = []
        for unit in self.current_player.units:
            reachable_cells += unit.reachable_cells
        self.board.player_units = reachable_cells

    def remove_dead(self):
        for player in self.players:
            for unit in player.units:
                if unit.health <= 0:
                    buffer = []
                    for i in player.units:
                        if i != unit:
                            buffer.append(i)
                    player.units = buffer
                    cords = unit.cords
                    self.board.board[cords[0]][cords[1]][1][-1].kill()
                    self.board.board[cords[0]][cords[1]][1] = self.board.board[cords[0]][cords[1]][1][:1:]
        for i in range(len(self.board.board)):
            for j in range(len(self.board.board)):
                for unit in self.board.board[i][j][1]:
                    if unit.type == 'unit' and unit.health <= 0:
                        self.board.board[i][j][1] = self.board.board[i][j][1][:-2:]

    def generate_cities(self, sprite_group):
        for i in self.players:
            self.players.index(i)
            textures = [assets.texture_city1, assets.texture_city2]
            for _ in range(self.city_count // len(self.players)):
                flag = True
                while flag:
                    x, y = random(0, len(self.board.board) - 1), random(0, len(self.board.board) - 1)
                    if self.board.get_biome(x, y) != 0:
                        city = City(i, textures[self.players.index(i)], (x, y), sprite_group)
                        i.add_city(city)
                        self.board.board[x][y][1] = [city]
                        flag = False
        for player in self.players:
            city = player.cities[int(chance(50))]
            self.add_unit(units.Warrior(player, sprite_group, city.cords), city.cords, player=player)
        self.players[0].stars = start_stars

    def add_unit(self, unit, cords, player=None):
        if player is None:
            player = self.current_player
        player.add_unit(unit)
        self.board.add_unit(unit, *cords)

    def move_unit(self, orig, dest):
        unit = self.board.get_units(*orig)[-1]
        if unit.type == 'unit' and unit.is_active and len(self.board.get_units(*dest)) < 1:
            self.sfx[4].play()
            self.board.board[dest[0]][dest[1]][1].append(self.board.board[orig[0]][orig[1]][1][-1])
            self.board.board[orig[0]][orig[1]][1] = self.board.board[orig[0]][orig[1]][1][:-2:]
            unit.cords = dest
            unit.update_range()
            unit.is_active = False
            self.update_player_units()
        else:
            self.sfx[5].play()

    def buy_unit(self, unit, cords):
        if self.current_player.stars >= unit.cost:
            self.add_unit(unit, cords)
            self.current_player.stars -= unit.cost
        else:
            self.sfx[5].play()
            del unit
