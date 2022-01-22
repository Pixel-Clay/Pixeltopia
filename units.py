import pygame

import common


def yeet():
    common.dprint('yeet')


class BaseUnit(pygame.sprite.Sprite):
    def __init__(self, player, textures, group, cords, *smth):
        super().__init__(*smth)

        self.is_active = True

        self.type = 'unit'

        self.player = player
        self.cords = cords

        self.input_textures = textures
        self.texture = []
        for i in self.input_textures:
            self.texture.append(common.load_image(i))
        self.current_texture = 0
        self.image = self.texture[self.current_texture]

        self.attack_points = 2
        self.defense_points = 1

        self.health = 3
        self.range = 1
        self.cost = 0

        self.reachable_cells = []

        common.dprint('UNIT NEW', player, textures, group, self)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0

        self.add(group)

    def set_cords(self, cords):
        self.cords = cords
        self.update_range()

    def update(self):
        common.dprint('UNIT UPDATE', self.cords, self)
        self.current_texture += common.animation_k
        if self.current_texture >= len(self.texture):
            self.current_texture = 0
        self.image = self.texture[int(self.current_texture)]

    def set_pos(self, x, y):
        self.rect.x, self.rect.y = x, y
        common.dprint('UNIT SET', self.cords, self, self.rect.x, self.rect.y)

    def interact(self):
        common.dprint('UNIT INTERACT', self.cords, self)

    def resize(self):
        for i in range(len(self.input_textures)):
            self.texture[i] = common.load_image(self.input_textures[i])
        self.image = self.texture[int(self.current_texture)]
        self.rect = self.image.get_rect()

    def update_range(self):
        self.reachable_cells = []
        for x in range(self.cords[0] - self.range, self.cords[0] + self.range + 1):
            for y in range(self.cords[1] - self.range, self.cords[1] + self.range + 1):
                self.reachable_cells.append((x, y))
        common.dprint('UNIT REACHABLE', self.cords, self.reachable_cells, self)
        return self.reachable_cells

    def attack(self, x, y):
        if self.is_active:
            self.update_range()
            common.dprint('UNIT ATTACK', self.cords, (x, y), self)
            if (x, y) in self.reachable_cells:
                opponent = self.player.manager.board.get_units(x, y)[-1]
                opponent.health -= self.attack_points
                self.health -= opponent.defense_points
                common.dprint('UNIT ATTACK SUCCESS', self.cords, self.health, self)
                self.is_active = False
                return True
        return False

    def dstats(self):
        common.dprint('UNIT STATS', self.cords, self.health, 'hp', self)


class Warrior(BaseUnit):
    def __init__(self, player, group, cords, *smth):
        textures = [common.assets.texture_unit_warrior_1, common.assets.texture_unit_warrior_2]
        super(Warrior, self).__init__(player, textures, group, cords, *smth)
        self.health = 10
        self.attack_points = 2
        self.defense_points = 2
        self.range = 1
        self.cords = cords
        self.cost = 2
        self.update_range()


class Archer(BaseUnit):
    def __init__(self, player, group, cords, *smth):
        textures = [common.assets.texture_unit_archer_1, common.assets.texture_unit_archer_2]
        super(Archer, self).__init__(player, textures, group, cords, *smth)
        self.health = 10
        self.attack_points = 2
        self.defense_points = 1
        self.range = 2
        self.cords = cords
        self.cost = 3
        self.update_range()


class Swordsman(BaseUnit):
    def __init__(self, player, group, cords, *smth):
        textures = [common.assets.texture_unit_swordsman_1, common.assets.texture_unit_swordsman_2]
        super(Swordsman, self).__init__(player, textures, group, cords, *smth)
        self.health = 15
        self.attack_points = 3
        self.defense_points = 3
        self.range = 1
        self.cords = cords
        self.cost = 3
        self.update_range()


class Mage(BaseUnit):
    def __init__(self, player, group, cords, *smth):
        textures = [common.assets.texture_unit_mage_1, common.assets.texture_unit_mage_2]
        super(Mage, self).__init__(player, textures, group, cords, *smth)
        self.health = 10
        self.attack_points = 4
        self.defense_points = 0
        self.range = 3
        self.cords = cords
        self.cost = 8
        self.update_range()
