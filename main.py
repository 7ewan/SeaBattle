import pygame
import os
import sys

pygame.init()

def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    return pygame.image.load(fullname)

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        pygame.draw.rect(screen, 'black',
                         (self.left, self.top, self.cell_size * self.width, self.cell_size * self.height), 2)
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, 'black', (
                    (self.left + self.cell_size * x), (self.top + self.cell_size * y), self.cell_size, self.cell_size),
                                 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if (x < self.left or x > self.left + self.width * self.cell_size or
                y < self.top or y > self.top + self.height * self.cell_size):
            return None
        return (x - self.left) // self.cell_size, (y - self.top) // self.cell_size

    def get_cell_center(self, cell_pos):
        if cell_pos is None:
            return None
        cell_x, cell_y = cell_pos
        center_x = self.left + cell_x * self.cell_size + self.cell_size // 2
        center_y = self.top + cell_y * self.cell_size + self.cell_size // 2
        return center_x, center_y

    def is_valid_position(self, cell_pos, size, vertical=True):
        cell_x, cell_y = cell_pos
        if vertical:
            return 0 <= cell_x < self.width and 0 <= cell_y + size - 1 < self.height
        else:
            return 0 <= cell_x + size - 1 < self.width and 0 <= cell_y < self.height

class Ship(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, size, image_name, vertical=False):
        super().__init__(all_sprites)
        self.image = load_image(image_name)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.size = size  # Количество клеток, занимаемых кораблем
        self.vertical = vertical  # Ориентация: True — вертикально, False — горизонтально
        self.dragging = False

    def start_drag(self, pos):
        if self.rect.collidepoint(pos):
            self.dragging = True
            self.offset_x = self.rect.x - pos[0]
            self.offset_y = self.rect.y - pos[1]

    def drag(self, pos):
        if self.dragging:
            self.rect.x = pos[0] + self.offset_x
            self.rect.y = pos[1] + self.offset_y

    def stop_drag(self, board):
        self.dragging = False
        # Рассчитываем координаты клетки по центру корабля
        cell = board.get_cell((self.rect.centerx, self.rect.centery))
        if cell and self.is_valid_position(cell, board):
            cell_x, cell_y = cell
            # Выравниваем корабль по центру клетки
            if self.vertical:
                self.rect.x = board.left + cell_x * board.cell_size
                self.rect.y = board.top + cell_y * board.cell_size
            else:
                self.rect.x = board.left + cell_x * board.cell_size
                self.rect.y = board.top + cell_y * board.cell_size

    def is_valid_position(self, cell, board):
        # Проверка, помещается ли корабль на доске
        cell_x, cell_y = cell
        for i in range(self.size):
            if self.vertical:
                if cell_y + i >= board.height or board.board[cell_y + i][cell_x] != 0:
                    return False
            else:
                if cell_x + i >= board.width or board.board[cell_y][cell_x + i] != 0:
                    return False
        return True


size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

board1 = Board(10, 10)
board1.set_view(20, 100, 40)

all_sprites = pygame.sprite.Group()

# Создание кораблей
ship1 = Ship(550, 100, size=1, image_name="1XBOAT.png")
ship2 = Ship(550, 200, size=2, image_name="2XBOAT.png")
ship3 = Ship(550, 300, size=3, image_name="3XBOAT.png")
ship4 = Ship(550, 400, size=4, image_name="4XBOAT.png")

running = True
dragged_sprite = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for sprite in all_sprites:
                sprite.start_drag(event.pos)
                if sprite.dragging:
                    dragged_sprite = sprite
                    break

        elif event.type == pygame.MOUSEMOTION:
            if dragged_sprite:
                dragged_sprite.drag(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragged_sprite:
                dragged_sprite.stop_drag(board1)
                dragged_sprite = None

    screen.fill('white')
    board1.render(screen)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
