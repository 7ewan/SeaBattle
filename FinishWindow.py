import pygame
from LoadImage import load_image

pygame.init()

# Группа для всех спрайтов
all_sprites = pygame.sprite.Group()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, scale_factor=1.0):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.animation_speed = 100  # Скорость анимации (в миллисекундах)
        self.last_update = pygame.time.get_ticks()
        self.scale_factor = scale_factor
        self.scale_frames()  # Масштабируем кадры

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def scale_frames(self):
        # Масштабируем каждый кадр
        for i in range(len(self.frames)):
            original_size = self.frames[i].get_size()
            new_size = (int(original_size[0] * self.scale_factor), int(original_size[1] * self.scale_factor))
            self.frames[i] = pygame.transform.scale(self.frames[i], new_size)
        self.rect.size = self.frames[0].get_size()  # Обновляем размер rect

    def update(self):
        # Обновляем кадр анимации
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


def show_finish_window(winner):
    size = WIDTH, HEIGHT = 1000, 600
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 60

    # Загрузка фона
    fon = pygame.transform.scale(load_image('finish_window.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    # Шрифт для текста
    font = pygame.font.SysFont(None, 74)
    text = font.render(f'ИГРОК {winner} ПОБЕДИЛ!', True, (0, 0, 0))

    # Кнопка "Начать заново"
    button_font = pygame.font.SysFont(None, 32)
    button_text = button_font.render("Начать заново", True, (255, 255, 255))
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

    # Очищаем группу спрайтов перед созданием нового анимированного спрайта
    all_sprites.empty()

    # Создание анимированного спрайта
    waves_sheet = load_image("waves.png")
    scale_factor = 0.5  # Уменьшаем спрайт в 2 раза
    waves = AnimatedSprite(waves_sheet, 9, 5, WIDTH // 2 - 100, HEIGHT // 2 + 150, scale_factor)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_pos):
                        return True

        # Отрисовка фона
        screen.blit(fon, (0, 0))

        # Отрисовка текста
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        # Отрисовка кнопки
        pygame.draw.rect(screen, (0, 128, 255), button_rect)
        screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))

        # Обновление и отрисовка спрайтов
        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    return False