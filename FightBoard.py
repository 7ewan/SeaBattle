from Boards import Board
from StartScreen import terminate
import pygame

size = WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode(size)
pygame.init()
clock = pygame.time.Clock()
FPS = 60


class FightBoard(Board):
    def __init__(self, width, height, left, top, cell_size, text_color='black'):
        super().__init__(width, height, left, top, cell_size, text_color)
        self.hits = [['0'] * width for _ in range(height)]
        self.font = pygame.font.SysFont(None, 32)
        self.player1_hits = 0  # Счетчик попаданий Игрока 1
        self.player2_hits = 0  # Счетчик попаданий Игрока 2

    def load_board_state(self, file_name):
        try:
            with open(file_name, 'r') as f:
                self.board = []
                for line in f:
                    row = list(map(int, line.strip().split()))
                    self.board.append(row)

            print("Загруженное поле:")
            for row in self.board:
                print(row)

        except FileNotFoundError:
            print(f"Файл {file_name} не найден!")

    def render(self, screen):
        super().render(screen)
        for y in range(self.height):
            for x in range(self.width):
                if self.hits[y][x] in ['X', 'x']:
                    cell_x = self.left + x * self.cell_size + self.cell_size // 3
                    cell_y = self.top + y * self.cell_size + self.cell_size // 4
                    hit_text = self.font.render(self.hits[y][x], True, 'red' if self.hits[y][x] == 'X' else 'blue')
                    screen.blit(hit_text, (cell_x, cell_y))

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if (x < self.left) or (x > self.left + self.width * self.cell_size) or (y < self.top) or (
                y > self.top + self.cell_size * self.height):
            return None
        get_cell_x = (x - self.left) // self.cell_size
        get_cell_y = (y - self.top) // self.cell_size
        return get_cell_x, get_cell_y

    def register_hit(self, x, y, hit, player):
        if hit:
            self.hits[y][x] = 'X'
            if player == 1:
                self.player1_hits += 1  # Увеличиваем счетчик попаданий Игрока 1
            else:
                self.player2_hits += 1  # Увеличиваем счетчик попаданий Игрока 2
        else:
            self.hits[y][x] = 'x'

    def on_click(self, cell_coords, player):
        if cell_coords:
            x, y = cell_coords
            print(f'Игрок {player} выстрел в клетку: ({x}, {y})')
            hit = isinstance(self.board[y][x], int) and self.board[y][x] > 0
            self.register_hit(x, y, hit, player)
            if hit:
                print("Попадание! (X)")
            else:
                print("Промах (x)")

    def get_click(self, mouse_pos, player):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, player)

    def check_win(self):
        if self.player1_hits >= 20:
            return 1  # Победил Игрок 1
        elif self.player2_hits >= 20:
            return 2  # Победил Игрок 2
        return 0  # Победителя пока нет


def fight_board_loop(fight_board_one, fight_board_two):
    running = True
    current_player = 1  # Начинает Игрок 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левый клик мыши (выстрел)
                    mouse_pos = pygame.mouse.get_pos()
                    if current_player == 1:
                        fight_board_two.get_click(mouse_pos, current_player)
                    else:
                        fight_board_one.get_click(mouse_pos, current_player)

                    # Проверка на победу
                    winner = fight_board_two.check_win() if current_player == 1 else fight_board_one.check_win()
                    if winner:
                        return winner  # Возвращаем номер победителя

                    # Смена игрока
                    current_player = 3 - current_player  # Переключаем между 1 и 2

        screen.fill('white')
        fight_board_one.render(screen)
        fight_board_two.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
