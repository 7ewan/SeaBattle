from LoadImage import load_image
import pygame, sys


def terminate():
    pygame.quit()
    sys.exit()


size = WIDTH, HEIGT = 1000, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 60

pygame.init()


def start_screen():
    intro_text = ["МОРСКОЙ БОЙ",
                  'НАЖМИТЕ "SPACE" ДЛЯ НАЧАЛА ИГРЫ', ]

    fon = pygame.transform.scale(load_image('banner5.jpg'), (WIDTH, HEIGT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = WIDTH / 2 - intro_rect.width / 2
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
        clock.tick(FPS)

