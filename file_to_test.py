import math
import random

import numpy as np
import pygame
import sys

# Global variables
# ----------------

global ROWS
global COLS
ROWS=7
COLS=6
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


