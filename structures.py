import pygame

from common import dprint, load_image


class BaseStructure(pygame.sprite.Sprite):
    def __init__(self, biome, texture, group, *smth):
        super().__init__(*smth)

        self.biome = biome
        self.image = load_image(texture)

        dprint('STRUCTURE NEW', biome, texture, *group, self)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0

        self.add(group)


    def update(self):
        dprint('STRUCTURE UPDATE', self)
        pass

    def set_pos(self, x, y):
        self.rect.x, self.rect.y = x, y
        dprint('STRUCTURE SET', self, self.rect.x, self.rect.y)

    def interact(self):
        dprint('STRUCTURE INTERACT', self)
        pass


class Mountain(BaseStructure):
    def __init__(self, biome, group, *smth):
        super().__init__(biome, 'assets/mountain.png', group, *smth)