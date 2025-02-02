import pygame
from StartScreen import start_screen, terminate, clock, screen, FPS
from Boards import Board
from Ships import Ship
from FightBoard import FightBoard, fight_board_loop

pygame.init()


def reset_game():
    board_player_one = Board(10, 10, 40, 100, 40)
    board_player_two = Board(10, 10, 40, 100, 40)

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

    ships_1 = [ship1_1, ship1_2, ship1_3, ship1_4, ship2_1, ship2_2, ship2_3, ship3_1, ship3_2, ship4]
    ships_2 = [ship1_1, ship1_2, ship1_3, ship1_4, ship2_1, ship2_2, ship2_3, ship3_1, ship3_2, ship4]

    board_player_one.reset_board("board_state_1.txt")
    board_player_two.reset_board("board_state_2.txt")

    for ship in ships_1 + ships_2:
        ship.reset_position()

    return board_player_one, board_player_two, ships_1, ships_2


def main_game_loop():
    while True:
        board_player_one, board_player_two, ships_1, ships_2 = reset_game()

        start_screen()

        reset_button_rect = pygame.Rect(800, 550, 150, 50)
        reset_button_color = (200, 0, 0)
        reset_button_font = pygame.font.SysFont(None, 36)

        player2_button_rect = pygame.Rect(800, 500, 150, 50)
        player2_button_color = (0, 128, 255)
        player2_button_font = pygame.font.SysFont(None, 36)

        fight_button_rect = pygame.Rect(800, 500, 150, 50)
        fight_button_color = (0, 128, 255)
        fight_button_font = pygame.font.SysFont(None, 36)

        dragging = None
        offset_x = 0
        offset_y = 0

        running = True
        placing_player_two = False
        fight_mode = False

        while running:
            board = board_player_two if placing_player_two else board_player_one
            ships = ships_2 if placing_player_two else ships_1
            board_state_file = "board_state_2.txt" if placing_player_two else "board_state_1.txt"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()

                        if reset_button_rect.collidepoint(mouse_pos):
                            for ship in ships:
                                ship.reset_position()
                            board.reset_board(board_state_file)
                            board.print_board()

                        elif player2_button_rect.collidepoint(mouse_pos) and not placing_player_two:
                            if all(board_player_one.is_ship_on_board(ship) for ship in ships_1):
                                placing_player_two = True
                                for ship in ships_2:
                                    ship.reset_position()
                                board_player_two.reset_board("board_state_2.txt")
                                board_player_two.print_board()
                            else:
                                board.set_warning_message("Не спеши матрос! Не весь флот готов к бою")

                        elif fight_button_rect.collidepoint(mouse_pos) and placing_player_two:
                            if all(board_player_two.is_ship_on_board(ship) for ship in ships_2):
                                fight_mode = True
                            else:
                                board.set_warning_message("Не спеши матрос! Не весь флот готов к бою")

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
                                board.remove_ship(ship)

                                if ship.orientation == "horizontal":
                                    new_y = ship.rect.y - (ship.size - 1) * ship.cell_size
                                    if new_y < board.top:
                                        board.set_warning_message("Куда собрался? Таким манёвром ты покинешь поле боя")
                                        board.place_ship(ship)
                                        continue
                                elif ship.orientation == "vertical":
                                    new_x = ship.rect.x + ship.size * ship.cell_size
                                    if new_x > board.left + board.width * board.cell_size:
                                        board.set_warning_message("Куда собрался? Таким манёвром ты покинешь поле боя")
                                        board.place_ship(ship)
                                        continue

                                ship.rotate()

                                if ship.check_adjacent_ships(ships, board):
                                    board.set_warning_message("Спокойно салага, таким разворот заденешь товарища!")
                                    ship.rotate()
                                    ship.rect.x, ship.rect.y = previous_position
                                    board.place_ship(ship)
                                    continue

                                board.place_ship(ship)
                                board.save_board_to_file(board_state_file)
                                board.clear_warning_message()
                                board.print_board()
                                break

                elif event.type == pygame.MOUSEMOTION:
                    if dragging:
                        mouse_pos = pygame.mouse.get_pos()
                        dragging.rect.x = mouse_pos[0] + offset_x
                        dragging.rect.y = mouse_pos[1] + offset_y

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and dragging:
                        mouse_pos = pygame.mouse.get_pos()
                        cell = board.get_cell(mouse_pos)
                        if cell:
                            cell_x, cell_y = cell
                            board.remove_ship(dragging)

                            if dragging.orientation == "horizontal":
                                if cell_x + dragging.size - 1 < board.width:
                                    left_bottom_x, left_bottom_y = board.get_bottom_left_coordinates(cell_x, cell_y)
                                    dragging.rect.x = left_bottom_x
                                    dragging.rect.y = left_bottom_y - board.cell_size
                                else:
                                    dragging.rect.x, dragging.rect.y = dragging.initial_position
                            elif dragging.orientation == "vertical":
                                if cell_y + dragging.size - 1 < board.height:
                                    left_bottom_x, left_bottom_y = board.get_bottom_left_coordinates(cell_x, cell_y)
                                    dragging.rect.x = left_bottom_x
                                    dragging.rect.y = left_bottom_y - board.cell_size
                                else:
                                    dragging.rect.x, dragging.rect.y = dragging.initial_position

                            # Проверяем соседние корабли
                            if dragging.check_adjacent_ships(ships, board):
                                dragging.rect.x, dragging.rect.y = dragging.initial_position
                                board.remove_ship(dragging)
                                board.print_board()
                                board.set_warning_message("Юнга, не стоит ставить корабли так близко!")
                            else:
                                board.place_ship(dragging)
                                board.print_board()
                                board.clear_warning_message()
                                board.save_board_to_file(board_state_file)

                        dragging = None

            if fight_mode:
                running = False
                fight_board_one = FightBoard(10, 10, 40, 100, 40)
                fight_board_two = FightBoard(10, 10, 560, 100, 40)
                fight_board_one.load_board_state("board_state_1.txt")
                fight_board_two.load_board_state("board_state_2.txt")
                fight_result = fight_board_loop(fight_board_one, fight_board_two)
                if fight_result:
                    break
                else:
                    terminate()

            screen.fill("white")
            board.render(screen)

            if not placing_player_two:
                for ship in ships_1:
                    screen.blit(ship.image, ship.rect)
            else:
                for ship in ships_2:
                    screen.blit(ship.image, ship.rect)

            pygame.draw.rect(screen, reset_button_color, reset_button_rect)
            screen.blit(reset_button_font.render("Сброс", True, (255, 255, 255)),
                        (reset_button_rect.x + 40, reset_button_rect.y + 10))

            if not placing_player_two:
                if all(board_player_one.is_ship_on_board(ship) for ship in ships_1):
                    pygame.draw.rect(screen, player2_button_color, player2_button_rect)
                    screen.blit(player2_button_font.render("Игрок 2", True, (255, 255, 255)),
                                (player2_button_rect.x + 30, player2_button_rect.y + 10))
            else:
                pygame.draw.rect(screen, fight_button_color, fight_button_rect)
                screen.blit(fight_button_font.render("В бой!", True, (255, 255, 255)),
                            (fight_button_rect.x + 30, fight_button_rect.y + 10))

            pygame.display.flip()
            clock.tick(FPS)


main_game_loop()
