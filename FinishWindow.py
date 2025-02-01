import pygame

def show_finish_window(winner):
    pygame.init()
    size = WIDTH, HEIGHT = 1000, 600
    screen = pygame.display.set_mode(size)
    font = pygame.font.SysFont(None, 74)
    text = font.render(f'ИГРОК {winner} ПОБЕДИЛ!', True, (0, 255, 0))
    screen.fill((0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()