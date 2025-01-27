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
        self.ship_id = ship_id  # Уникальный идентификатор корабля
        self.orientation = "horizontal"
        self.image_name = image_name

    def rotate(self):
        bottom_left_x, bottom_left_y = self.rect.bottomleft

        if self.orientation == "horizontal":
            self.orientation = "vertical"
            # Заменяем изображение на вертикальное
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
