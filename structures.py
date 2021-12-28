import pygame

import common


class BaseStructure(pygame.sprite.Sprite):
    def __init__(self, biome, texture, *group):
        super().__init__(*group)

        self.biome = biome
        self.texture = common.load_image(texture)

        self.rect = self.texture.get_rect()
        self.rect.x, self.rect.y = 0, 0


    def update(self):
        pass

    def draw(self, x, y):
        self.rect.x, self.rect.y = self.x, self.y

    def interact(self):
        pass
