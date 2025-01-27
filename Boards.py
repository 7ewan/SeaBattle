import pygame


class Board:
    def __init__(self, width, height, left, top, cell_size, text_color='black'):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, 24)  # Устанавливаем шрифт для текста

    def render(self, screen):
        # Рисуем рамку доски
        pygame.draw.rect(screen, 'black',
                         (self.left, self.top, self.cell_size * self.width, self.cell_size * self.height), 3)

        # Добавляем нумерацию сверху (1–10)
        for x in range(self.width):
            number_text = self.font.render(str(x + 1), True, self.text_color)
            number_x = self.left + x * self.cell_size + self.cell_size // 2 - number_text.get_width() // 2
            number_y = self.top - self.cell_size // 2 - number_text.get_height() // 2
            screen.blit(number_text, (number_x, number_y))

        # Добавляем нумерацию слева (а–к)
        letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'к']
        for y in range(self.height):
            letter_text = self.font.render(letters[y], True, self.text_color)
            letter_x = self.left - self.cell_size // 2 - letter_text.get_width() // 2
            letter_y = self.top + y * self.cell_size + self.cell_size // 2 - letter_text.get_height() // 2
            screen.blit(letter_text, (letter_x, letter_y))

        # Рисуем клетки доски
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, 'black', (
                    (self.left + self.cell_size * x), (self.top + self.cell_size * y), self.cell_size, self.cell_size),
                                 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if (x < self.left) or (x > self.left + self.width * self.cell_size) or (y < self.top) or (
                y > self.top + self.cell_size * self.height):
            return None
        get_cell_x = (x - self.left) // self.cell_size
        get_cell_y = (y - self.top) // self.cell_size
        return get_cell_x, get_cell_y

    def get_bottom_left_coordinates(self, cell_x, cell_y):
        bottom_left_x = self.left + cell_x * self.cell_size
        bottom_left_y = self.top + (cell_y + 1) * self.cell_size
        return bottom_left_x, bottom_left_y

    def on_click(self, cell_coords):
        print(cell_coords)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)
