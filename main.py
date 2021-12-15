import pygame


class Board:
    # создание поля
    def __init__(self, width, height, world=None):
        self.width = width
        self.height = height

        # формат клетки: [id_биома, [что стоит], id_ресурса]
        self.board = [[[0, [], 0]] * height for _ in range(width)]
        # значения по умолчанию
        self.x = 300
        self.y = 30
        self.cell_size = 32
        self.ground_tiles = ['#00bfff', '#7cfc00', '#fce883', '#fffafa', '#228b22', '#808080']

        self.screen = screen

        skybox = pygame.image.load('assets/skybox.png')
        self.skybox = pygame.transform.scale(skybox, self.screen.get_size())
        self.paused = True

    def get_biome(self, x, y):
        return self.board[x][y][0]

    # настройка внешнего вида
    def set_view(self, x=10, y=10, cell_size=30):
        self.x = x
        self.y = y
        self.cell_size = cell_size

    def render(self):
        for x in range(self.width):
            for y in range(self.height):
                dx = x * self.cell_size + self.x
                dy = y * self.cell_size + self.y
                biome = self.get_biome(x, y)
                print(x, y, dx, dy, biome)

                # Цвет тайла
                color = pygame.Color(self.ground_tiles[biome])
                pygame.draw.rect(self.screen, color, (dx, dy, self.cell_size, self.cell_size))

                # Цвет обводки тайла
                hsv = color.hsva
                color.hsva = (hsv[0], hsv[1], hsv[2] - 10, hsv[3])

                # рисуем обводку
                pygame.draw.rect(self.screen, color, (dx, dy, self.cell_size, self.cell_size), 1)

        for x in range(self.width):
            dx = x * self.cell_size + self.x
            dy = self.height * self.cell_size + self.y
            ground = pygame.Color('#663300')

            pygame.draw.rect(self.screen, ground, (dx, dy, self.cell_size, self.cell_size))

            # Цвет обводки тайла
            hsv = ground.hsva
            color.hsva = (hsv[0], hsv[1], hsv[2] - 10, hsv[3])

            # рисуем обводку
            pygame.draw.rect(self.screen, color, (dx, dy, self.cell_size, self.cell_size), 1)

        pygame.display.flip()

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.get_click(event.pos)
                elif event.button == 3:
                    self.paused = not self.paused
            if event.type == pygame.KEYDOWN:
                if event.unicode == ' ':
                    self.paused = not self.paused

        self.do_movement()
        self.screen.blit(self.skybox, (0, 0))
        self.render()
        pygame.display.flip()
        if not self.paused:
            pass

    def do_movement(self):
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            self.y += 10
        if keys[pygame.K_a]:
            self.x -= 10
        if keys[pygame.K_w]:
            self.y -= 10
        if keys[pygame.K_d]:
            self.x += 10

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.x) // self.cell_size
        y = (mouse_pos[1] - self.y) // self.cell_size
        if x < 0 or x >= self.width:
            return None
        if y < 0 or y >= self.height:
            return None
        return x, y

    def on_click(self, cell):
        print('paint!', cell)
        try:
            self.board[cell[0]][cell[1]][0] = int(not self.board[cell[0]][cell[1]][0])
        except Exception:
            pass
        self.render()


pygame.init()
size = 1200, 600
screen = pygame.display.set_mode(size)
# поле 5 на 7
board = Board(12, 12)
clock = pygame.time.Clock()
while True:
    board.tick()
    clock.tick(30)
