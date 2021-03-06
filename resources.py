import pygame

from common import dprint, load_image, assets


class BaseResource(pygame.sprite.Sprite):
    def __init__(self, biome, texture, group, *smth):
        super().__init__(*smth)

        self.type = 'resource'

        self.biome = biome

        self.id = 1

        self.texture = texture
        self.image = load_image(texture)

        self.stars = 0
        self.remove_cost = 0

        dprint('STRUCTURE NEW', biome, texture, *group, self)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0

        self.add(group)

    def update(self):
        dprint('STRUCTURE UPDATE', self)

    def set_pos(self, x, y):
        self.rect.x, self.rect.y = x, y
        dprint('STRUCTURE SET', self, self.rect.x, self.rect.y)

    def interact(self):
        dprint('STRUCTURE INTERACT', self)
        return self.stars

    def resize(self):
        self.image = load_image(self.texture)
        self.rect = self.image.get_rect()


class Mountain(BaseResource):
    def __init__(self, biome, group, *smth):
        super().__init__(biome, assets.texture_mountain, group, *smth)
        self.remove_cost = 7
        self.stars = 2


class Fruit(BaseResource):
    def __init__(self, biome, group, *smth):
        texture = assets.texture_fish if biome == 0 else assets.texture_fruit
        super().__init__(biome, texture, group, *smth)
        self.remove_cost = 2
        self.stars = 1


class Forest(BaseResource):
    def __init__(self, biome, group, *smth):
        super().__init__(biome, assets.texture_forest, group, *smth)
        self.remove_cost = 3
        self.stars = 2


class Animal(BaseResource):
    def __init__(self, biome, group, *smth):
        texture = assets.texture_whale if biome == 0 else assets.texture_fox
        super().__init__(biome, texture, group, *smth)
        self.remove_cost = 3
        self.stars = 2
