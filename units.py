import pygame

import common
from common import dprint, load_image


def yeet():
    dprint('yeet')


class BaseUnit(pygame.sprite.Sprite):
    def __init__(self, player, textures, group, cords, *smth):
        super().__init__(*smth)

        self.player = player

        self.cords = cords

        self.input_textures = textures
        self.texture = []
        for i in self.input_textures:
            self.texture.append(load_image(i))
        self.current_texture = 0
        self.image = self.texture[self.current_texture]

        self.attack_points = 2
        self.defense_points = 1

        self.health = 3

        self.range = 1

        self.reachable_cells = []

        dprint('UNIT NEW', player, textures, *group, self)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0

        self.add(group)

    def set_cords(self, cords):
        self.cords = cords
        self.update_range()

    def update(self):
        dprint('UNIT UPDATE', self.cords, self)
        self.current_texture += common.animation_k
        if self.current_texture >= len(self.texture):
            self.current_texture = 0
        self.image = self.texture[int(self.current_texture)]

    def set_pos(self, x, y):
        self.rect.x, self.rect.y = x, y
        dprint('UNIT SET', self.cords, self, self.rect.x, self.rect.y)

    def interact(self):
        dprint('UNIT INTERACT', self.cords, self)

    def resize(self):
        for i in range(len(self.input_textures)):
            self.texture[i] = load_image(self.input_textures[i])
        self.image = self.texture[int(self.current_texture)]
        self.rect = self.image.get_rect()

    def update_range(self):
        self.reachable_cells = []
        for x in range(self.cords[0] - self.range, self.cords[0] + self.range):
            for y in range(self.cords[1] - self.range, self.cords[1] + self.range):
                self.reachable_cells.append((x, y))
        dprint('UNIT REACHABLE', self.cords, self.reachable_cells, self)

    def attack(self, x, y):
        self.update_range()
        dprint('UNIT ATTACK', self.cords, (x, y), self)
        if (x, y) in self.reachable_cells:

            opponent = self.player.manager.board.get_units(x, y)[-1]
            opponent.health -= self.attack_points
            self.health -= opponent.defense_points
            dprint('UNIT ATTACK SUCCESS', self.cords, self.health, self)

    def dstats(self):
        dprint('UNIT STATS', self.cords, self.health, 'hp', self)
