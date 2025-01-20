import pygame
import os
import sys

# Инициализация pygame
pygame.init()

# Задаем размеры игрового окна
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)  # Устанавливаем размеры окна
clock = pygame.time.Clock()  # Устанавливаем таймер для управления обновлением кадров

# Инициализация шрифтов
pygame.font.init()
font_board = pygame.font.SysFont('arial', 20)  # Инициализация шрифта для подписи клеток игрового поля
font_player_window = pygame.font.SysFont('arial', 40)  # Инициализация шрифта для подписи окна игроков


# Функция для загрузки изображений из папки 'data'
def load_image(name):
    fullname = os.path.join('data', name)  # Создаем путь к изображению
    if not os.path.isfile(fullname):  # Проверяем, существует ли файл с таким именем
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()  # Если файл отсутствует, завершаем выполнение программы
    return pygame.image.load(fullname)  # Загружаем изображение и возвращаем его


# Функция для отрисовки текста на экране с координатами и шрифтом
def draw_text(screen, text, x, y, font, color='Blue'):
    text_surface = font.render(text, True, pygame.Color(color))  # Создаем поверхность текста
    screen.blit(text_surface, (x, y))  # Отображаем текст на экране

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["МОРСКОЙ БОЙ",
                  'НАЖМИТЕ "SPACE" ДЛЯ НАЧАЛА ИГРЫ', ]

    fon = pygame.transform.scale(load_image('banner5.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = width / 2 - intro_rect.width / 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # начинаем игру
        pygame.display.flip()
        clock.tick(30)


start_screen()


# Класс для создания игрового поля игроков для расстановки кораблей
class Board:
    # Инициализация игровых параметров и их отрисовка
    def __init__(self, width, height):
        self.width = width  # Ширина игрового поля
        self.height = height  # Высота игрового поля
        self.board = [[0] * width for _ in range(height)]  # Создаем пустую игровую сетку (матрицу)
        self.left = 10  # Координата X начального положения игрового поля
        self.top = 10  # Координата Y начального положения игрового поля
        self.cell_size = 30  # Размер каждой клетки игрового поля

    # Устанавливаем параметры отображения игрового поля
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # Отрисовка игрового поля на экране
    def render(self, screen):
        # Рисуем рамку игрового поля
        pygame.draw.rect(screen, 'black',
                         (self.left, self.top, self.cell_size * self.width, self.cell_size * self.height), 3)

        # Рисуем клетки игрового поля
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, 'black', (
                    (self.left + self.cell_size * x), (self.top + self.cell_size * y), self.cell_size, self.cell_size),
                                 1)

        # Добавляем нумерацию клеток и буквы
        for i in range(self.width):
            # Номера клеток сверху
            draw_text(screen, str(i + 1), self.left + self.cell_size * i + self.cell_size // 3, self.top - 25,
                      font_board)
            # Буквы клеток слева
            draw_text(screen, chr(1040 + i), self.left - 25, self.top + self.cell_size * i + self.cell_size // 3,
                      font_board)

    # Функция для получения координат клетки, на которую нажата мышь
    def get_cell(self, mouse_pos):
        x, y = mouse_pos  # Координаты мыши
        if (x < self.left or x > self.left + self.width * self.cell_size or
                y < self.top or y > self.top + self.height * self.cell_size):
            return None  # Если курсор мыши за пределами игрового поля, возвращаем None
        return (x - self.left) // self.cell_size, (y - self.top) // self.cell_size  # Возвращаем координаты клетки

    # Функция для получения центра клетки по её координатам
    def get_cell_center(self, cell_pos):
        if cell_pos is None:
            return None
        cell_x, cell_y = cell_pos
        center_x = self.left + cell_x * self.cell_size + self.cell_size // 2
        center_y = self.top + cell_y * self.cell_size + self.cell_size // 2
        return center_x, center_y

    # Проверка, может ли корабль быть установлен на доске в данной позиции
    def is_valid_position(self, cell_pos, size, vertical=True):
        cell_x, cell_y = cell_pos
        if vertical:
            return 0 <= cell_x < self.width and 0 <= cell_y + size - 1 < self.height
        else:
            return 0 <= cell_x + size - 1 < self.width and 0 <= cell_y < self.height


# Класс для создания кораблей
class Ship(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, size, image_name, vertical=False):
        super().__init__(all_sprites)
        self.image = load_image(image_name)  # Загрузка изображения корабля
        self.rect = self.image.get_rect()  # Прямоугольник, который охватывает изображение
        self.mask = pygame.mask.from_surface(self.image)  # Маска изображения для проверки пересечений
        self.rect.x = pos_x  # Позиция X корабля
        self.rect.y = pos_y  # Позиция Y корабля
        self.size = size  # Размер корабля в клетках
        self.vertical = vertical  # Ориентация корабля (True — вертикально, False — горизонтально)
        self.dragging = False  # Флаг, обозначающий, перетаскивается ли корабль

    # Метод для поворота корабля на игровом поле
    def rotate(self, board):
        cell = board.get_cell((self.rect.x, self.rect.y))  # Проверка, над игровым полем ли корабль
        if cell:  # Если корабль над игровым полем, вращение запрещено
            return
        # Поворачиваем изображение на 90 градусов
        self.image = pygame.transform.rotate(self.image, 90)
        old_center = self.rect.center  # Сохраняем старый центр корабля
        self.rect = self.image.get_rect(center=old_center)  # Привязываем новый прямоугольник к старому центру
        self.vertical = not self.vertical  # Меняем ориентацию

    # Метод для начала перетаскивания корабля
    def start_drag(self, pos):
        if self.rect.collidepoint(pos):  # Если курсор мыши находится на корабле
            self.dragging = True  # Устанавливаем флаг перетаскивания
            self.offset_x = self.rect.x - pos[0]  # Смещение по X относительно курсора
            self.offset_y = self.rect.y - pos[1]  # Смещение по Y относительно курсора
            self.last_x = self.rect.x  # Запоминаем старую позицию X
            self.last_y = self.rect.y  # Запоминаем старую позицию Y

    # Метод для перемещения корабля с учетом перетаскивания
    def drag(self, pos):
        if self.dragging:
            self.rect.x = pos[0] + self.offset_x  # Новая позиция X
            self.rect.y = pos[1] + self.offset_y  # Новая позиция Y

    # Проверка, может ли корабль быть размещен в данной клетке на доске
    def is_valid_position(self, cell, board):
        cell_x, cell_y = cell  # Координаты клетки на доске
        for i in range(self.size):  # Проверяем, подходит ли корабль в выбранную позицию
            if self.vertical:  # Если вертикальное размещение
                if (cell_y + i >= board.height or
                        board.board[cell_y + i][cell_x] != 0 or
                        not self.is_clear_around(cell_x, cell_y + i, board)):  # Проверка соседних клеток
                    return False
            else:  # Если горизонтальное размещение
                if (cell_x + i >= board.width or
                        board.board[cell_y][cell_x + i] != 0 or
                        not self.is_clear_around(cell_x + i, cell_y, board)):  # Проверка соседних клеток
                    return False
        return True  # Если корабль можно разместить, возвращаем True

    # Проверка, свободна ли клетка вокруг корабля для его размещения
    def is_clear_around(self, x, y, board):
        for dy in range(-1, 2):  # Проверка соседних клеток
            for dx in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.width and 0 <= ny < board.height:
                    if board.board[ny][nx] != 0:  # Если в соседней клетке уже есть корабль
                        return False
        return True  # Если все клетки вокруг свободны, возвращаем True

    # Метод для окончания перетаскивания корабля
    def stop_drag(self, board):
        self.dragging = False  # Снимаем флаг перетаскивания
        previous_position = self.rect.x, self.rect.y  # Сохраняем старую позицию корабля

        cell = board.get_cell((self.rect.x, self.rect.y))  # Получаем клетку, в которой находится корабль

        # Удаляем корабль с текущего положения на доске
        self.clear_from_board(board)

        if cell and self.is_valid_position(cell, board):  # Если корабль можно разместить
            cell_x, cell_y = cell  # Клетка на доске
            self.rect.x = board.left + cell_x * board.cell_size  # Новая позиция X
            self.rect.y = board.top + cell_y * board.cell_size  # Новая позиция Y
            # Помещаем корабль на доску в новое место
            self.place_on_board(cell_x, cell_y, board)
        else:  # Если корабль не подходит для размещения
            self.rect.x, self.rect.y = previous_position  # Возвращаем корабль на предыдущее место
            self.place_on_board((self.rect.x - board.left) // board.cell_size,
                                (self.rect.y - board.top) // board.cell_size, board)

    # Удаляем корабль с доски
    def clear_from_board(self, board):
        for y in range(board.height):  # Проходим по каждой клетке доски
            for x in range(board.width):
                if board.board[y][x] == id(self):  # Если клетка занята этим кораблем
                    board.board[y][x] = 0  # Очищаем клетку

    # Размещаем корабль на доске в определенной позиции
    def place_on_board(self, cell_x, cell_y, board):
        for i in range(self.size):  # Проходим по размерам корабля
            if self.vertical:
                board.board[cell_y + i][cell_x] = id(self)  # Помещаем корабль вертикально
            else:
                board.board[cell_y][cell_x + i] = id(self)  # Помещаем корабль горизонтально


# Задаем размеры игрового окна
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)  # Устанавливаем размеры окна
clock = pygame.time.Clock()  # Устанавливаем таймер для управления обновлением кадров

# Создаем игровое поле для игроков
board1 = Board(10, 10)
board1.set_view(40, 100, 40)

all_sprites = pygame.sprite.Group()  # Группа для хранения всех спрайтов (кораблей)

# Создание кораблей и добавление их в группу спрайтов
ship1_1 = Ship(550, 220, size=1, image_name="1XBOAT.png")
ship1_2 = Ship(630, 220, size=1, image_name="1XBOAT.png")
ship1_3 = Ship(710, 220, size=1, image_name="1XBOAT.png")
ship1_4 = Ship(790, 220, size=1, image_name="1XBOAT.png")
ship2_1 = Ship(550, 300, size=2, image_name="2XBOAT.png")
ship2_2 = Ship(670, 300, size=2, image_name="2XBOAT.png")
ship2_3 = Ship(790, 300, size=2, image_name="2XBOAT.png")
ship3_1 = Ship(550, 380, size=3, image_name="3XBOAT.png")
ship3_2 = Ship(710, 380, size=3, image_name="3XBOAT.png")
ship4 = Ship(550, 460, size=4, image_name="4XBOAT.png")

running = True  # Флаг для управления циклом игры
dragged_sprite = None  # Текущий перетаскиваемый спрайт (корабль)

# Основной игровой цикл
while running:
    for event in pygame.event.get():  # Обработка событий
        if event.type == pygame.QUIT:  # Если пользователь закрыл окно
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:  # Если нажата левая кнопка мыши
                for sprite in all_sprites:  # Проверяем, находится ли курсор на корабле
                    sprite.start_drag(event.pos)
                    if sprite.dragging:  # Если корабль начался перетаскиваться
                        dragged_sprite = sprite  # Запоминаем текущий спрайт
                        break
            elif event.button == pygame.BUTTON_RIGHT:  # Если нажата правая кнопка мыши
                for sprite in all_sprites:
                    if sprite.rect.collidepoint(event.pos):  # Проверяем, находится ли курсор на корабле
                        sprite.rotate(board1)  # Поворачиваем корабль
                        break

        elif event.type == pygame.MOUSEMOTION:  # Если мышь движется
            if dragged_sprite:  # Если перетаскивается корабль
                dragged_sprite.drag(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:  # Если кнопка мыши отпущена
            if dragged_sprite:
                dragged_sprite.stop_drag(board1)  # Проверяем окончание перетаскивания корабля
                dragged_sprite = None  # Обнуляем флаг перетаскивания

    screen.fill('white')  # Очистка экрана цветом белый
    board1.render(screen)  # Отрисовка игрового поля
    draw_text(screen, "Игрок 1", 448, 10, font_player_window, color='blue')  # Отображаем имя игрока
    all_sprites.draw(screen)  # Отображаем все корабли
    all_sprites.update()  # Обновляем спрайты
    pygame.display.flip()  # Отображаем изменения на экране
    clock.tick(30)  # Устанавливаем обновление кадров в секунду

pygame.quit()  # Завершаем работу pygame
