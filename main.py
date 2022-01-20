import pygame, sys
import pygame as pg


def Intersect(x1, x2, y1, y2, db1, db2):
    if (x1 > x2 - db1) and (x1 < x2 + db2) and (y1 > y2 - db1) and (y1 < y2 + db2):
        return 1
    else:
        return 0


window = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('pixelpotia')
screen = pygame.Surface((1200, 800))
info = pygame.Surface((1200, 800))

class Sprite:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap = pygame.image.load(filename)
        self.bitmap.set_colorkey((0, 0, 0))

    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))


class Menu:
    def __init__(self, punkts=[1200, 800, u'Punkts', (2, 400, 30), (200, 250, 250)]):
        self.punkts = punkts

    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        done = True
        font_menu = pygame.font.Font(None, 50)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        punkt = 0
        while done:
            info.fill((0, 0, 128))
            screen.fill((0, 0, 128))

            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    punkt = i[5]
            self.render(screen, font_menu, punkt)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        exit()
                    # elif punkt == 2:
                    #     s = pg.image.load('regu.png')
                    #     window.blit(s, info)
            window.blit(info, (0, 0))
            window.blit(screen, (0, 30))
            pygame.display.flip()


pygame.font.init()

punkts = [(10, 450, u'Играть', (255, 255, 0), (0, 255, 128), 0),
          (10, 550, u'Выход', (255, 255, 0), (0, 255, 128), 1),
          (10, 650, u'Правила', (255, 255, 0), (0, 255, 128), 2),
          (380, 10, u'THE BATTLE OF PIXELPOTIA', (255, 255, 0), (0, 255, 128), 3)
          ]

game = Menu(punkts)
game.menu()

done = True
pygame.key.set_repeat(1, 1)
while done:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            done = False
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                game.menu()

    screen.fill((0, 0, 128))
    info.fill((0, 0, 128))

    window.blit(info, (0, 0))
    pygame.display.flip()
