import pygame

debug = False
cell_size = 32

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
