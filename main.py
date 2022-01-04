import pygame
import os
import sys

FPS = 30

pygame.init()
size = width, height = 720, 480
screen = pygame.display.set_mode(size)
screen.fill((255, 170, 255))


def load_image(name, color_key=-1):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
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


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


class Miniature(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image("zas2.png")
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 1)

    def update(self):
        self.rect.y -= 5
        if self.rect.top <= 10:
            self.rect.top = 10


class Play(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image("play.png")
        self.rect = self.image.get_rect()
        self.rect.center = (width / 4, height / 1)

    def update(self):
        self.rect.y -= 5
        if self.rect.top <= 190:
            self.rect.top = 190


class Pravila(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image("правила.png")
        self.rect = self.image.get_rect()
        self.rect.center = (width / 4, height / 1)

    def update(self):
        self.rect.y -= 5
        if self.rect.top <= 290:
            self.rect.top = 290


class Exit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image("exit.png")
        self.rect = self.image.get_rect()
        self.rect.center = (width / 4, height / 1)

    def update(self):
        self.rect.y -= 5
        if self.rect.top <= 390:
            self.rect.top = 390


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("pixeltopia")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Miniature()
all_sprites.add(player)

play2 = Play()
all_sprites.add(play2)

pravila = Pravila()
all_sprites.add(pravila)

exit = Exit()
all_sprites.add(exit)
# Цикл игры
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()

    # Рендеринг
    screen.fill((250, 170, 250))
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
