import pygame
from LoadImage import load_image

ships_sprites = pygame.sprite.Group()


class Ship(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_name, ship_id=None, size=1, cell_size=40):
        super().__init__(ships_sprites)  # Добавляем в группу спрайтов
        self.size = size  # Размер корабля (в клетках)
        self.cell_size = cell_size  # Размер одной клетки
        self.image = load_image(image_name)  # Загружаем изображение
        self.rect = self.image.get_rect()  # Получаем прямоугольник для позиционирования
        self.mask = pygame.mask.from_surface(self.image)  # Маска для столкновений
        self.rect.x = pos_x  # Позиция по оси X
        self.rect.y = pos_y  # Позиция по оси Y
        self.initial_position = (pos_x, pos_y)
        self.ship_id = ship_id  # Уникальный идентификатор корабля
        self.orientation = "horizontal"  # Начальная ориентация
        self.image_name = image_name  # Изображение корабля

    def rotate(self):
        bottom_left_x, bottom_left_y = self.rect.bottomleft
        if self.orientation == "horizontal":
            self.orientation = "vertical"
            vertical_image_name = self.image_name.replace(".png",
                                                          "v.png")
            self.image = load_image(vertical_image_name)
            self.image = pygame.transform.scale(
                self.image,
                (self.cell_size, self.cell_size * self.size)
            )
        else:
            self.orientation = "horizontal"
            self.image = load_image(self.image_name)
            self.image = pygame.transform.scale(
                self.image,
                (self.cell_size * self.size, self.cell_size)
            )

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (bottom_left_x, bottom_left_y)

    def check_adjacent_ships(self, ships, board):
        for ship in ships:
            if ship == self:
                continue
            if self.rect.colliderect(ship.rect.inflate(self.cell_size * 2, self.cell_size * 2)):
                return True
        return False

    def reset_position(self):
        if self.orientation == "vertical":
            self.rotate()  # Поворачиваем обратно, если повернут
        self.rect.topleft = self.initial_position
