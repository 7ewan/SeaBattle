from Boards import Board
from StartScreen import terminate, start_screen
from FinishWindow import show_finish_window
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
        self.timer_font = pygame.font.SysFont(None, 36)
        self.player1_hits = 0
        self.player2_hits = 0

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
                self.player1_hits += 1
            else:
                self.player2_hits += 1
            self.mark_destroyed_ship(x, y)
        else:
            self.hits[y][x] = 'x'

    def on_click(self, cell_coords, player):
        if cell_coords:
            x, y = cell_coords
            # Проверяем, была ли клетка уже атакована
            if self.hits[y][x] != '0':
                print("Сюда уже стреляли!")
                return False  # Клетка уже атакована, выстрел не засчитывается

            print(f'Игрок {player} выстрел в клетку: ({x}, {y})')
            hit = isinstance(self.board[y][x], int) and self.board[y][x] > 0
            self.register_hit(x, y, hit, player)
            if hit:
                print("Попадание! (X)")
            else:
                print("Промах (x)")
            return True  # Возвращаем True, если выстрел был выполнен
        return False  # Если клик был вне поля, считаем это промахом

    def get_click(self, mouse_pos, player):
        cell = self.get_cell(mouse_pos)
        return self.on_click(cell, player)

    def mark_destroyed_ship(self, x, y):
        ship_id = self.board[y][x]
        ship_cells = []
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == ship_id:
                    ship_cells.append((col, row))
        if all(self.hits[cy][cx] == 'X' for cx, cy in ship_cells):
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for cx, cy in ship_cells:
                for dx, dy in directions:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if self.board[ny][nx] == 0 and self.hits[ny][nx] == '0':  # Если пустая клетка
                            self.hits[ny][nx] = 'x'

    def check_win(self):
        if self.player1_hits == 20:
            return 1  # Победил Игрок 1
        elif self.player2_hits == 20:
            return 2  # Победил Игрок 2
        return 0  # Победителя пока нет


def fight_board_loop(fight_board_one, fight_board_two):
    running = True
    current_player = 1
    turn_start_time = pygame.time.get_ticks()
    turn_duration = 30000

    while running:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - turn_start_time

        if elapsed_time >= turn_duration:
            print(f"Время вышло! Ход переходит к Игроку {3 - current_player}.")
            current_player = 3 - current_player
            turn_start_time = pygame.time.get_ticks()  # Сбрасываем таймер

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левый клик мыши (выстрел)
                    mouse_pos = pygame.mouse.get_pos()
                    if current_player == 1:
                        # Обрабатываем клик только по полю Игрока 2
                        if fight_board_two.get_cell(mouse_pos):
                            shot_result = fight_board_two.get_click(mouse_pos, current_player)
                            if shot_result:
                                winner = fight_board_two.check_win()
                                if winner:
                                    if show_finish_window(winner):
                                        return True
                                    else:
                                        terminate()
                                # Обновление таймера при попадании или промахе
                                hit = fight_board_two.hits[fight_board_two.get_cell(mouse_pos)[1]][
                                          fight_board_two.get_cell(mouse_pos)[0]] == 'X'
                                if hit:
                                    turn_start_time = pygame.time.get_ticks()
                                else:
                                    current_player = 3 - current_player
                                    turn_start_time = pygame.time.get_ticks()
                    else:
                        if fight_board_one.get_cell(mouse_pos):
                            shot_result = fight_board_one.get_click(mouse_pos, current_player)
                            if shot_result:
                                winner = fight_board_one.check_win()
                                if winner:
                                    if show_finish_window(winner):
                                        return True
                                    else:
                                        terminate()

                                hit = fight_board_one.hits[fight_board_one.get_cell(mouse_pos)[1]][
                                          fight_board_one.get_cell(mouse_pos)[0]] == 'X'
                                if hit:
                                    turn_start_time = pygame.time.get_ticks()
                                else:
                                    current_player = 3 - current_player
                                    turn_start_time = pygame.time.get_ticks()

        screen.fill('white')
        font = pygame.font.SysFont(None, 36)
        player1_text = font.render("Игрок 1", True, ('blue'))
        player2_text = font.render("Игрок 2", True, ('red'))

        screen.blit(player1_text, (
        fight_board_one.left + fight_board_one.width * fight_board_one.cell_size // 2 - 40, fight_board_one.top - 80))
        screen.blit(player2_text, (
        fight_board_two.left + fight_board_two.width * fight_board_two.cell_size // 2 - 40, fight_board_two.top - 80))

        fight_board_one.render(screen)
        fight_board_two.render(screen)
        turn_text = pygame.font.SysFont(None, 32).render(f"Ход игрока {current_player}", True, 'black')
        screen.blit(turn_text, (WIDTH // 2 - 100, 20))
        remaining_time = max(0, turn_duration - elapsed_time)
        timer_text = fight_board_one.timer_font.render(f"Осталось: {remaining_time // 1000} сек", True, (0, 0, 0))
        if current_player == 1:
            screen.blit(timer_text, (
                fight_board_two.left, fight_board_two.top + fight_board_two.height * fight_board_two.cell_size + 20))
        else:
            screen.blit(timer_text, (
                fight_board_one.left, fight_board_one.top + fight_board_one.height * fight_board_one.cell_size + 20))

        pygame.display.flip()
        clock.tick(FPS)

    return False
