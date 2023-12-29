import math
import random

import numpy as np
import pygame
import sys

# Global variables
# ----------------

global ROWS
global COLS
try:
    opponent = sys.argv[1]
    ROWS = int(sys.argv[2])
    COLS = int(sys.argv[3])
    print(ROWS)
    print(COLS)
except ValueError:
    print("Rows and columns must be integers.")
    sys.exit(1)
PLUSINF = math.inf
MINUSINF = -math.inf
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
# ----------------

# Players
PLAYER_ONE = 0
PLAYER_TWO = 1
AI_PLAYER = 1
# ----------------

# Pieces
EMPTY = 0
PLAYER_ONE_PIECE = 1
PLAYER_TWO_PIECE = 2
AI_PLAYER_PIECE = 2

# Game elements
Piece_size = 100
RADIUS = int(Piece_size / 2 - 5)
global PLAYING
PLAYING = True
# ----------------


# Board configuration functions

def initialize_rows_cols():
    try:
       # ROWS= int(sys.argv[2])
       # COLS= int(sys.argv[3])
        ROWS=7
        COLS=6
    except ValueError:
        print("Rows and columns must be integers.")
        sys.exit(1)


def create_board():
    board = np.zeros((ROWS, COLS))
    return board


def print_board(board):
    print(np.flip(board, 0))


def is_valid_location(board, col):
    return board[ROWS - 1][col] == 0


def get_next_open_row(board, col):
    for row in range(ROWS):
        if board[row][col] == 0:
            return row
    return -1


def add_piece(board, row, col, piece):
    board[row][col] = piece


def is_tie(board):
    for col in range(COLS):
        if board[ROWS - 1][col] == 0:
            return False
    return True


# Game GUI functions

def board_setup():
    pygame.init()
    pygame.display.set_caption('Connect 4')
    screen = pygame.display.set_mode((COLS * Piece_size, (ROWS + 1) * Piece_size))
    return screen


def draw_board(screen, board):
    height = (ROWS + 1) * Piece_size
    for col in range(COLS):
        for row in range(ROWS):
            x = col * Piece_size
            y = (ROWS - row - 1) * Piece_size + Piece_size
            pygame.draw.rect(screen, BLUE, (x, y, Piece_size, Piece_size))
            circle_x = x + int(Piece_size / 2)
            circle_y = y + int(Piece_size / 2)
            pygame.draw.circle(screen, BLACK, (circle_x, circle_y), RADIUS)

            piece = board[row][col]
            if piece == PLAYER_ONE_PIECE:
                piece_color = RED
            elif piece == PLAYER_TWO_PIECE:
                piece_color = YELLOW
            else:
                continue

            pygame.draw.circle(screen, piece_color, (circle_x, circle_y), RADIUS - 5)  # Smaller circle
    pygame.display.update()


def draw_hover_piece(screen, col, turn):
    mouse_x = col * Piece_size + int(Piece_size / 2)

    pygame.draw.rect(screen, BLACK, (0, 0, COLS * Piece_size, Piece_size))

    if turn == PLAYER_ONE:
        pygame.draw.circle(screen, RED, (mouse_x, int(Piece_size / 2)), RADIUS)
    elif turn == PLAYER_TWO:
        pygame.draw.circle(screen, YELLOW, (mouse_x, int(Piece_size / 2)), RADIUS)


# Main game functions player vs player

def Game_over(board, piece):
    # Check horizontal locations for win
    for col in range(COLS - 3):
        for row in range(ROWS):
            if board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece and \
                    board[row][col + 3] == piece:
                return True

    # Check vertical locations for win
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == piece and board[row + 1][col] == piece and board[row + 2][col] == piece and \
                    board[row + 3][col] == piece:
                return True

    # Check positively sloped diaganols
    for col in range(COLS - 3):
        for row in range(ROWS - 3):
            if board[row][col] == piece and board[row + 1][col + 1] == piece and board[row + 2][col + 2] == piece and \
                    board[row + 3][col + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for col in range(COLS - 3):
        for row in range(3, ROWS):
            if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece and \
                    board[row - 3][col + 3] == piece:
                return True

    return False


def display_message(screen, message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(COLS * Piece_size // 2, Piece_size // 2))
    screen.blit(text, text_rect)
    pygame.display.update()


def game_two_players(screen, board):
    turn = PLAYER_ONE
    game_over = Game_over(board, PLAYER_ONE_PIECE)
    draw_board(screen, board)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if is_tie(board):
                game_over = True
                break
            if event.type == pygame.MOUSEMOTION:
                col = int(event.pos[0] / Piece_size)
                draw_hover_piece(screen, col, turn)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if turn == PLAYER_ONE:
                    col = int(event.pos[0] / Piece_size)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        add_piece(board, row, col, PLAYER_ONE_PIECE)
                        if Game_over(board, PLAYER_ONE_PIECE):
                            print("PLAYER 1 WINS!")
                            game_over = True
                        turn = PLAYER_TWO

                else:
                    col = int(event.pos[0] / Piece_size)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        add_piece(board, row, col, PLAYER_TWO_PIECE)
                        if Game_over(board, PLAYER_TWO_PIECE):
                            print("PLAYER 2 WINS!")
                            game_over = True
                        turn = PLAYER_ONE

                print_board(board)
                draw_board(screen, board)
                pygame.display.update()

                col = int(event.pos[0] / Piece_size)
                draw_hover_piece(screen, col, turn)
                pygame.display.update()
    if game_over:
        if Game_over(board, PLAYER_ONE_PIECE):
            display_message(screen, "PLAYER 1 WINS!")
        elif Game_over(board, PLAYER_TWO_PIECE):
            display_message(screen, "PLAYER 2 WINS!")
        elif is_tie(board):
            display_message(screen, "IT'S TIE")

    # after 5 seconds close the game
    pygame.time.wait(5000)
    pygame.quit()

def main():


    initialize_rows_cols()
    board = create_board()
    pygame.init()
    screen = pygame.display.set_mode((COLS * Piece_size, (ROWS + 1) * Piece_size))
    pygame.display.set_caption('Connect 4')
    game_two_players(screen, board)




if __name__ == '__main__':
    main()
