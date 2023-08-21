""" TicTacToe Game """

import pygame
import random
import os
import time

pygame.init()

screen_width, screen_height = 600, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("TIC TAC TOE")
pygame.display.set_icon(pygame.image.load(os.path.join('Assets', 'tictactoe_icon.png')))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (102, 178, 255)
RED = (204, 0, 0)

# Fonts
start_font = pygame.font.SysFont("None", 70)
symbol_font = pygame.font.SysFont("None", 180)
game_stats_font = pygame.font.SysFont("None", 40)

# Game constants
radius = 100
X = symbol_font.render("X", True, RED)
O = symbol_font.render("O", True, RED)
GRID_SIZE = 3
CELL_SIZE = 200
GRID_LINE_WIDTH = 10
WINNER_DICT = {'x': 0, 'o': 0}

''' The function draws the game grid'''


def draw_grid():
    # Draw rows
    for row in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLUE, (50 - GRID_LINE_WIDTH, CELL_SIZE * row - GRID_LINE_WIDTH),
                         (550 + 10, CELL_SIZE * row - GRID_LINE_WIDTH), GRID_LINE_WIDTH)

    # Draw columns
    for row in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLUE, (CELL_SIZE * row - GRID_LINE_WIDTH, 50 - GRID_LINE_WIDTH),
                         (CELL_SIZE * row - GRID_LINE_WIDTH, 550 + GRID_LINE_WIDTH), GRID_LINE_WIDTH)


''' The function checks if the cells need to be updated
    because of a mouse click on the grid '''


def check_x_o(turn, cells):
    mouse_pressed = pygame.mouse.get_pressed(num_buttons=3)

    if mouse_pressed[0]:
        pos_x, pos_y = pygame.mouse.get_pos()

        cell_indices = get_cell(pos_x, pos_y, cells)

        if cell_indices is not None:
            row_idx, col_idx = cell_indices

            if turn == 'x':
                if cells[row_idx][col_idx] == 0:  # Check if the cell is empty
                    cells[row_idx][col_idx] = 'x'
                    turn = 'o'  # Switch the turn to 'o'

            elif turn == 'o':
                if cells[row_idx][col_idx] == 0:  # Check if the cell is empty
                    cells[row_idx][col_idx] = 'o'
                    turn = 'x'  # Switch the turn to 'x'

    return turn


''' The function returns the cell indices for the given mouse click position '''


def get_cell(pos_x, pos_y, cells):
    for row_idx, row in enumerate(cells):
        for col_idx, cell_value in enumerate(row):
            if col_idx * CELL_SIZE < pos_x < (col_idx + 1) * CELL_SIZE and row_idx * CELL_SIZE < pos_y < (
                    row_idx + 1) * CELL_SIZE:
                return row_idx, col_idx


''' The function draws a x or o symbol to the screen'''


def draw_symbol(row_idx, col_idx, symbol):
    # Calculate the center coordinates for the O
    center_x = (col_idx + 1) * CELL_SIZE - 100
    center_y = (row_idx + 1) * CELL_SIZE - 100

    # Create a new Rect with the center coordinates
    symbol_rect = symbol.get_rect(center=(center_x, center_y))

    # Blit (draw) the X onto the screen using the new Rect
    screen.blit(symbol, symbol_rect)


''' The function draws the current x's and o's to the game screen '''


def draw_x_o(cells):
    for row_idx, row in enumerate(cells):
        for col_idx, cell_value in enumerate(row):
            if cell_value == 'x':
                draw_symbol(row_idx, col_idx, X)
            elif cell_value == 'o':
                draw_symbol(row_idx, col_idx, O)


''' The function draws the current turn on the screen'''


def draw_curr_turn(curr_turn):
    pygame.draw.line(screen, BLACK, (0, screen_height - 35), (screen_width, screen_height - 35), 2)
    curr_turn_text = game_stats_font.render(f"Current Turn: {curr_turn.upper()}", True, BLACK)
    curr_turn_text_rect = curr_turn_text.get_rect(center=(screen_width // 2, screen_height - 20))
    screen.blit(curr_turn_text, curr_turn_text_rect)


''' The function draws the total win count '''


def draw_win_count():
    x_win_count = game_stats_font.render(f"X Wins: {WINNER_DICT['x']}", True, RED)
    o_win_count = game_stats_font.render(f"O Wins: {WINNER_DICT['o']}", True, RED)

    x_win_rect = x_win_count.get_rect(left=20, top=10)
    o_win_rect = o_win_count.get_rect(right=screen_width - 20, top=10)

    screen.blit(x_win_count, x_win_rect)
    screen.blit(o_win_count, o_win_rect)


''' The function draws the main game window '''


def draw_window(curr_turn, cells):
    screen.fill(WHITE)

    draw_grid()
    draw_x_o(cells)
    draw_curr_turn(curr_turn)
    draw_win_count()

    pygame.display.update()


''' The function checks if there is a winner '''


def check_winner(cells):
    # Check rows
    for row in cells:
        if row.count('x') == 3:
            return 'x'
        elif row.count('o') == 3:
            return 'o'

    # Check columns
    for col in range(3):
        if all(cells[row][col] == 'x' for row in range(3)):
            return 'x'
        elif all(cells[row][col] == 'o' for row in range(3)):
            return 'o'

    # Check diagonals
    if all(cells[i][i] == 'x' for i in range(3)) or all(cells[i][2 - i] == 'x' for i in range(3)):
        return 'x'
    elif all(cells[i][i] == 'o' for i in range(3)) or all(cells[i][2 - i] == 'o' for i in range(3)):
        return 'o'

    # If no winner yet, return None (game ongoing or draw)
    return None


''' The functon draws the winner ending screen'''


def draw_winner(winner):
    pygame.time.delay(1000)
    screen.fill(WHITE)
    winner_text = symbol_font.render(f"{winner.upper()} WON!", True, RED)
    winner_rect = winner_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(winner_text, winner_rect)

    pygame.display.update()
    pygame.time.delay(2500)


''' The function checks if there is a draw'''


def check_draw(cells):
    for row in cells:
        for cell in row:
            if cell == 0:
                return False

    return True


''' The function draws the draw ending screen'''


def draw_draw():
    pygame.time.delay(1000)
    screen.fill(WHITE)
    draw_text = symbol_font.render(f"DRAW", True, BLUE)
    draw_rect = draw_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(draw_text, draw_rect)

    pygame.display.update()
    pygame.time.delay(2500)


''' The function draws the start window '''


def show_start_window():
    screen.fill(WHITE)
    game_header_text = "TicTacToe"
    start_text = "Press ENTER To Play"

    game_header_text_rendered = symbol_font.render(game_header_text, True, RED)
    start_text_rendered = start_font.render(start_text, True, BLUE)

    start_rect = start_text_rendered.get_rect(center=(screen_width // 2, screen_height // 2))
    game_header_rect = game_header_text_rendered.get_rect(center=(screen_width // 2, 100))

    screen.blit(game_header_text_rendered, game_header_rect)
    screen.blit(start_text_rendered, start_rect)
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True
            if event.type == pygame.QUIT:
                return False


def main():
    # Start window
    running = show_start_window()
    while True:
        # Initialize board
        cells = [[0 for _ in range(3)] for _ in range(3)]

        # Choose turn
        curr_turn = random.choice(['x', 'o'])

        winner = None
        clock = pygame.time.Clock()

        # Main game loop
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    running = False

            # Update turn if needed
            curr_turn = check_x_o(curr_turn, cells)

            winner = check_winner(cells)
            draw = check_draw(cells)

            # Draw game window
            draw_window(curr_turn, cells)

            # Check for winner
            if winner is not None:
                draw_winner(winner)
                break

            # Check for draw
            if draw:
                draw_draw()
                break

        # Update win count
        if winner is not None:
            WINNER_DICT[winner] += 1

        if not running:
            break
    pygame.quit()


if __name__ == '__main__':
    main()
