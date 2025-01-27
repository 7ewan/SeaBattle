import pygame
import os
import sys


def load_image(name):
    fullname = os.path.join('data', name)  # Создаем путь к изображению
    if not os.path.isfile(fullname):  # Проверяем, существует ли файл с таким именем
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()  # Если файл отсутствует, завершаем выполнение программы
    return pygame.image.load(fullname)  # Загружаем изображение и возвращаем его
