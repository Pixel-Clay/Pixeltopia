import pygame
from random import randint

debug = False
fullscreen = True
cell_size = 40


def window_modes(resolution=(1200, 800)):
    if fullscreen:
        return resolution, pygame.FULLSCREEN, pygame.RESIZABLE
    else:
        return resolution, pygame.RESIZABLE


def dprint(*args):
    if debug:
        print(*args)


def load_image(name, color_key=None):
    try:
        texture = pygame.image.load(name).convert()
        image = pygame.transform.scale(texture, (cell_size, cell_size))
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def random(percentage):
    chance = randint(0, 100)
    if chance < percentage:
        return True
    else:
        return False


def draw_hud(player):
    pass
