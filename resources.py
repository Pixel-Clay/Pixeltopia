import pygame

from common import dprint, load_image


class BaseResource(pygame.sprite.Sprite):
    def __init__(self, biome, texture, group, *smth):
        super().__init__(*smth)

        self.biome = biome

        self.id = 1

        self.texture = texture
        self.image = load_image(texture)

        self.population = 0
        self.remove_cost = 0

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


    def resize(self):
        self.image = load_image(self.texture)
        self.rect = self.image.get_rect()


class Mountain(BaseResource):
    def __init__(self, biome, group, *smth):
        super().__init__(biome, 'assets/mountain.png', group, *smth)

        self.remove_cost = 7
        self.population = 2
