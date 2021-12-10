import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 300
        self.top = 30
        self.cell_size = 30


        self.paused = True
        self.screen = screen
        self.cell_size = 32
        for i in range(16):
            self.board[16][i] = -1

    # настройка внешнего вида
    def set_view(self, left=10, top=10, cell_size=30):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                x = j * self.cell_size + self.left
                y = i * self.cell_size + self.top
                if self.board[i][j] > 0:
                    pygame.draw.rect(screen, pygame.Color(pygame.Color('#ABBABF')), (x, y, self.cell_size, self.cell_size))
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
                if event.unicode == 's':
                    self.top -= 10
                if event.unicode == 'w':
                    self.top += 10
                if event.unicode == 'd':
                    self.left -= 10
                if event.unicode == 'a':
                    self.left += 10
        self.screen.fill((0, 0, 0))
        self.render(screen)
        pygame.display.flip()
        if not self.paused:
            pass
    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
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
board = Board(16, 17)
clock = pygame.time.Clock()
while True:
    board.tick()
    clock.tick(10)
