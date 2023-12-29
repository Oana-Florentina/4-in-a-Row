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

