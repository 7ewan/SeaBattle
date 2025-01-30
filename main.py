import pygame
from StartScreen import start_screen, terminate, clock, screen, FPS
from Boards import Board
from Ships import Ship, ships_sprites
from FightBoard import FightBoard
from FightBoard import fight_board_loop

pygame.init()

start_screen()

reset_button_rect = pygame.Rect(800, 550, 150, 50)
reset_button_color = (200, 0, 0)  # Красная кнопка
reset_button_font = pygame.font.SysFont(None, 36)

button_rect = pygame.Rect(800, 500, 150, 50)
button_color = (0, 128, 255)
button_font = pygame.font.SysFont(None, 36)

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
fight_mode = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if reset_button_rect.collidepoint(mouse_pos):  # Кнопка сброса
                    for ship in ships:
                        ship.reset_position()
                    board_player_one.reset_board()
                    board_player_one.print_board()
                if button_rect.collidepoint(mouse_pos):
                    fight_mode = True
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
                        previous_position = (ship.rect.x, ship.rect.y)
                        board_player_one.remove_ship(ship)
                        if ship.orientation == "horizontal":
                            if ship.rect.y - (ship.size - 1) * ship.cell_size < board_player_one.top:
                                print("Не хватает места! Отмена поворота.")
                                board_player_one.place_ship(ship)
                                continue
                        elif ship.orientation == "vertical":
                            if ship.rect.x + (
                                    ship.size - 1) * ship.cell_size > board_player_one.left + board_player_one.width * board_player_one.cell_size:
                                print("Не хватает места! Отмена поворота.")
                                board_player_one.place_ship(ship)
                                continue

                        ship.rotate()

                        if ship.check_collision(ships, board_player_one):
                            print("Корабль пересекается с другим! Отмена поворота.")
                            ship.rotate()
                            ship.rect.x, ship.rect.y = previous_position
                            board_player_one.place_ship(ship)
                            continue

                        board_player_one.place_ship(ship)
                        board_player_one.save_board_to_file()
                        board_player_one.print_board()


        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_pos = pygame.mouse.get_pos()
                dragging.rect.x = mouse_pos[0] + offset_x
                dragging.rect.y = mouse_pos[1] + offset_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging:
                mouse_pos = pygame.mouse.get_pos()
                cell = board_player_one.get_cell(mouse_pos)
                if cell:
                    cell_x, cell_y = cell
                    board_player_one.remove_ship(dragging)
                    if dragging.orientation == "horizontal":
                        if cell_x + dragging.size - 1 < board_player_one.width:
                            left_bottom_x, left_bottom_y = board_player_one.get_bottom_left_coordinates(cell_x, cell_y)
                            dragging.rect.x = left_bottom_x
                            dragging.rect.y = left_bottom_y - board_player_one.cell_size
                        else:
                            print("Выходит за границы! Оставляем на месте.")
                    elif dragging.orientation == "vertical":
                        if cell_y + dragging.size - 1 < board_player_one.height:
                            left_bottom_x, left_bottom_y = board_player_one.get_bottom_left_coordinates(cell_x, cell_y)
                            dragging.rect.x = left_bottom_x
                            dragging.rect.y = left_bottom_y - board_player_one.cell_size
                        else:
                            print("Выходит за границы! Оставляем на месте.")
                    board_player_one.place_ship(dragging)
                    board_player_one.print_board()
                    if dragging:
                        board_player_one.save_board_to_file()
                dragging = None

    if fight_mode:
        running = False
        fight_board_one = FightBoard(10, 10, 40, 100, 40)
        fight_board_two = FightBoard(10, 10, 560, 100, 40)
        fight_board_one.load_board_state('board_state.txt')
        fight_board_loop(fight_board_one, fight_board_two)

    screen.fill('white')

    board_player_one.render(screen)

    for ship in ships:
        screen.blit(ship.image, ship.rect)
    ships_sprites.draw(screen)
    screen.blit(ship1_1.image, ship1_1.rect)

    pygame.draw.rect(screen, reset_button_color, reset_button_rect)
    reset_button_text = reset_button_font.render("Сброс", True, (255, 255, 255))
    screen.blit(reset_button_text, (reset_button_rect.x + 40, reset_button_rect.y + 10))

    pygame.draw.rect(screen, button_color, button_rect)
    button_text = button_font.render("В бой!", True, (255, 255, 255))
    screen.blit(button_text, (button_rect.x + 30, button_rect.y + 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
