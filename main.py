import pygame
from StartScreen import start_screen, terminate, clock, screen, FPS
from Boards import Board
from Ships import Ship, ships_sprites

pygame.init()

start_screen()

board_player_one = Board(10, 10, 40, 100, 40)
ship1_1 = Ship(550, 220, image_name="1XBOAT.png", ship_id=1, size=1, cell_size=40)
ship1_2 = Ship(630, 220, image_name="1XBOAT.png", ship_id=2, size=1, cell_size=40)
ship1_3 = Ship(710, 220, image_name="1XBOAT.png", ship_id=3, size=1, cell_size=40)
ship1_4 = Ship(790, 220, image_name="1XBOAT.png", ship_id=4, size=1, cell_size=40)
ship2_1 = Ship(550, 300, image_name="2XBOAT.png", ship_id=5, size=2, cell_size=40)
ship2_2 = Ship(670, 300, image_name="2XBOAT.png", ship_id=6, size=2, cell_size=40)
ship2_3 = Ship(790, 300, image_name="2XBOAT.png", ship_id=7, size=2, cell_size=40)
ship3_1 = Ship(550, 380, image_name="3XBOAT.png", ship_id=8, size=3, cell_size=40)
ship3_2 = Ship(710, 380, image_name="3XBOAT.png", ship_id=9, size=3, cell_size=40)
ship4 = Ship(550, 460, image_name="4XBOAT.png", ship_id=10, size=4, cell_size=40)

ships = [ship1_1, ship1_2, ship1_3, ship1_4, ship2_1, ship2_2, ship2_3, ship3_1, ship3_2, ship4]

dragging = None
offset_x = 0
offset_y = 0

running = True
dragged_sprite = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левый клик мыши
                mouse_pos = pygame.mouse.get_pos()
                for ship in ships:
                    if ship.rect.collidepoint(mouse_pos):
                        dragging = ship
                        offset_x = ship.rect.x - mouse_pos[0]
                        offset_y = ship.rect.y - mouse_pos[1]
                        break
            elif event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                for ship in ships:
                    if ship.rect.collidepoint(mouse_pos):
                        if ship.orientation == "horizontal":
                            if ship.rect.y - (ship.size - 1) * ship.cell_size < board_player_one.top:
                                print(
                                    "Недостаточно места для поворота корабля. Верхняя часть выходит за пределы поля.")
                                continue
                        elif ship.orientation == "vertical":
                            if ship.rect.x + (
                                    ship.size - 1) * ship.cell_size > board_player_one.cell_size * board_player_one.width:
                                print("Недостаточно места для поворота корабля. Правая часть выходит за пределы поля.")
                                continue
                        ship.rotate()
                        print(
                            f'{ship.ship_id}: ({ship.rect.x // ship.cell_size}, {((ship.rect.y - board_player_one.top) // ship.cell_size) + 1})')
                        break




        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_pos = pygame.mouse.get_pos()
                dragging.rect.x = mouse_pos[0] + offset_x
                dragging.rect.y = mouse_pos[1] + offset_y


        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Левый клик мыши
                if dragging:  # Проверяем, что dragging не None
                    mouse_pos = pygame.mouse.get_pos()
                    cell = board_player_one.get_cell(mouse_pos)
                    if cell:  # Если кликнут на допустимую клетку
                        cell_x, cell_y = cell

                        # Проверка для горизонтального корабля
                        if dragging.orientation == "horizontal":
                            if cell_x + dragging.size - 1 < board_player_one.width:  # Проверяем правую границу
                                left_bottom_x, left_bottom_y = board_player_one.get_bottom_left_coordinates(cell_x,
                                                                                                            cell_y)
                                dragging.rect.x = left_bottom_x
                                dragging.rect.y = left_bottom_y - board_player_one.cell_size  # Чтобы корабль оказался в верхней части клетки
                                print(
                                    f'({dragging.rect.x // 40}, {((dragging.rect.y - board_player_one.top) // 40) + 1})')
                            else:
                                print("Корабль выходит за границы доски (горизонтально), возврат на прежнюю позицию.")
                                dragging.rect.x = dragging.rect.x
                                dragging.rect.y = dragging.rect.y


                        elif dragging.orientation == "vertical":
                            if cell_y + dragging.size - 1 < board_player_one.height:  # Проверяем нижнюю границу
                                left_bottom_x, left_bottom_y = board_player_one.get_bottom_left_coordinates(cell_x,
                                                                                                            cell_y)
                                dragging.rect.x = left_bottom_x
                                dragging.rect.y = left_bottom_y - board_player_one.cell_size
                                print(f'({dragging.rect.x // 40}, {((dragging.rect.y - board_player_one.top) // 40)}')
                            else:
                                print("Корабль выходит за границы доски (вертикально), возврат на прежнюю позицию.")
                                dragging.rect.x = dragging.rect.x
                                dragging.rect.y = dragging.rect.y
                    dragging = None

    screen.fill('white')
    board_player_one.render(screen)
    for ship in ships:
        screen.blit(ship.image, ship.rect)
    ships_sprites.draw(screen)
    screen.blit(ship1_1.image, ship1_1.rect)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
