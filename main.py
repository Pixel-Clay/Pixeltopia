import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.x = 300
        self.y = 30
        self.cell_size = 64
        self.keyboard = []

        self.skybox = pygame.image.load('assets/skybox.png')
        self.paused = True
        self.screen = screen
        for i in range(self.width):
            self.board[self.height - 1][i] = -1

    # настройка внешнего вида
    def set_view(self, x=10, y=10, cell_size=30):
        self.x = x
        self.y = y
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                x = j * self.cell_size + self.x
                y = i * self.cell_size + self.y
                if self.board[i][j] > 0:
                    pygame.draw.rect(screen, pygame.Color(pygame.Color('#ABBABF')),
                                     (x, y, self.cell_size, self.cell_size))
                elif self.board[i][j] == 0:
                    pygame.draw.rect(screen, pygame.Color(pygame.Color('#7cfc00')),
                                     (x, y, self.cell_size, self.cell_size))
                    pygame.draw.rect(screen, pygame.Color(pygame.Color('#71e300')),
                                     (x, y, self.cell_size, self.cell_size), 1)
                elif self.board[i][j] == -1:
                    pygame.draw.rect(screen, pygame.Color(pygame.Color('#804000')),
                                     (x, y, self.cell_size, self.cell_size))
                    pygame.draw.rect(screen, pygame.Color(pygame.Color('#663300')),
                                     (x, y, self.cell_size, self.cell_size), 1)
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
                elif event.unicode in ['w', 'a', 's', 'd']:
                    self.keyboard.append(event.unicode)
            if event.type == pygame.KEYUP:
                if event.unicode in ['w', 'a', 's', 'd']:
                    try:
                        self.keyboard.remove(event.unicode)
                    except Exception:
                        pass

        self.do_movement()

        self.screen.blit(self.skybox, (0, 0))
        self.render(screen)
        pygame.display.flip()
        if not self.paused:
            pass

    def do_movement(self):
        if 's' in self.keyboard:
            self.y -= 5
        elif 'a' in self.keyboard:
            self.x -= 5
        elif 'w' in self.keyboard:
            self.y += 5
        elif 'd' in self.keyboard:
            self.x += 5

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
        try:
            self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2
        except Exception:
            pass
        self.render(self.screen)


pygame.init()
size = 1200, 600
screen = pygame.display.set_mode(size)
# поле 5 на 7
board = Board(12, 13)
clock = pygame.time.Clock()
while True:
    board.tick()
    clock.tick(30)
