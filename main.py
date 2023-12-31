import math
import random

import numpy as np
import pygame
import sys

# Global variables
# ----------------

global ROWS
global COLS


PLUSINF = math.inf
MINUSINF = -math.inf

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_GRAY = (169, 169, 169)
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

try:
    opponent = sys.argv[1]
    ROWS = int(sys.argv[2])
    COLS = int(sys.argv[3])
    print(ROWS)
    print(COLS)
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
    screen_width = COLS * Piece_size
    screen_height = (ROWS + 2) * Piece_size  # Increased by one row for the text and one for the board shift
    screen = pygame.display.set_mode((screen_width, screen_height))

    return screen


def draw_border(screen, color):

    border_thickness = 5
    border_color = color

    # Top border
    pygame.draw.rect(screen, border_color, (0, 0, COLS * Piece_size, border_thickness))

    # Bottom border
    pygame.draw.rect(screen, border_color, (0, (ROWS + 1) * Piece_size - border_thickness, COLS * Piece_size, border_thickness))

    # Left border
    pygame.draw.rect(screen, border_color, (0, 0, border_thickness, (ROWS + 1) * Piece_size))

    # Right border
    pygame.draw.rect(screen, border_color, ((COLS * Piece_size) - border_thickness, 0, border_thickness, (ROWS + 1) * Piece_size))

    pygame.display.update()


def draw_board(screen, board):

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

    pygame.draw.rect(screen, DARK_GRAY, (0, 0, COLS * Piece_size, Piece_size))

    if turn == PLAYER_ONE:
        pygame.draw.circle(screen, RED, (mouse_x, int(Piece_size / 2)), RADIUS)
    elif turn == PLAYER_TWO:
        pygame.draw.circle(screen, YELLOW, (mouse_x, int(Piece_size / 2)), RADIUS)


# Main game functions player vs player

def is_game_over(board, piece):
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
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(COLS * Piece_size // 2, Piece_size // 2))
    screen.blit(text, text_rect)
    pygame.display.update()


def game_two_players(screen, board):
    turn = PLAYER_ONE
    game_over = is_game_over(board, PLAYER_ONE_PIECE)
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
                        if is_game_over(board, PLAYER_ONE_PIECE):
                            print("PLAYER 1 WINS!")
                            game_over = True
                        else:
                            turn = PLAYER_TWO

                else:
                    col = int(event.pos[0] / Piece_size)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        add_piece(board, row, col, PLAYER_TWO_PIECE)
                        if is_game_over(board, PLAYER_TWO_PIECE):
                            print("PLAYER 2 WINS!")
                            game_over = True
                        else:
                            turn = PLAYER_ONE

                print_board(board)
                draw_board(screen, board)
                col = int(event.pos[0] / Piece_size)
                draw_hover_piece(screen, col, turn)
                pygame.display.update()

    if game_over:
        if is_game_over(board, PLAYER_ONE_PIECE):
            display_message(screen, "PLAYER 1 WINS!")
            draw_border(screen, RED)

        elif is_game_over(board, PLAYER_TWO_PIECE):
            display_message(screen, "PLAYER 2 WINS!")
            draw_border(screen, YELLOW)

        elif is_tie(board):
            display_message(screen, "IT'S TIE")
            draw_border(screen, WHITE)


    # after 5 seconds close the game
    pygame.time.wait(5000)
    pygame.quit()


# Main game functions player vs AI

def evaluate_block(window, piece):
    piece_count = np.count_nonzero(window == piece)
    empty_count = np.count_nonzero(window == EMPTY)
    score = 0
    opp_piece = PLAYER_ONE_PIECE if piece == AI_PLAYER_PIECE else AI_PLAYER_PIECE

    if piece_count == 4:
        score += 100
    elif piece_count == 3 and empty_count == 1:
        score += 50
    elif piece_count == 2 and empty_count == 2:
        score += 10


    opposite_count = np.count_nonzero(window == opp_piece)
    if opposite_count == 3 and empty_count == 1:
        score -= 50

    return score


def extract_blocks(board):
    windows = []
    rows, cols = ROWS, COLS

    # Horizontal windows
    for r in range(rows):
        for c in range(cols - 3):
            window = board[r][c:c + 4]
            windows.append(window)

    # Vertical windows
    for c in range(cols):
        for r in range(rows - 3):
            window = [board[r + i][c] for i in range(4)]
            windows.append(window)

    # Positive sloped diagonal windows
    for r in range(rows - 3):
        for c in range(cols - 3):
            window = [board[r + i][c + i] for i in range(4)]
            windows.append(window)

    # Negative sloped diagonal windows
    for r in range(rows - 3):
        for c in range(cols - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            windows.append(window)

    return windows


def calculate_score(board, piece):
    score = 0
    blocks = extract_blocks(board)

    for window in blocks:
        score += evaluate_block(window, piece)

    # Additional strategies for controlling center and edges
    center_column = COLS // 2
    for row in range(ROWS):
        if board[row][center_column] == piece:
            score += 10  # Encourage control of the center column

        if row == 0 or row == ROWS - 1:
            for col in range(COLS):
                if board[row][col] == piece:
                    score += 5  # Encourage controlling edge positions

    return score


def is_terminal_node(board):
    return is_game_over(board, PLAYER_ONE_PIECE) or is_game_over(board, AI_PLAYER_PIECE) or len(
        get_valid_locations(board)) == 0


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def evaluate_terminal(board):
    if is_game_over(board, AI_PLAYER_PIECE):
        return 100000000000000
    elif is_game_over(board, PLAYER_ONE_PIECE):
        return -10000000000000
    else:
        return 0


def evaluate_depth_zero(board):
    return calculate_score(board, AI_PLAYER_PIECE)


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if is_terminal:
        return None, evaluate_terminal(board)
    if depth == 0:
        return None, evaluate_depth_zero(board)

    if maximizingPlayer:
        value = MINUSINF
        random.shuffle(valid_locations)
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            add_piece(board_copy, row, col, AI_PLAYER_PIECE)
            new_score = minimax(board_copy, depth - 1, alpha, beta, False)[1]

            if new_score > value:
                value, column = new_score, col

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return column, value

    else:  # Minimizing player
        value = PLUSINF

        random.shuffle(valid_locations)
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            add_piece(board_copy, row, col, PLAYER_ONE_PIECE)
            new_score = minimax(board_copy, depth - 1, alpha, beta, True)[1]

            if new_score < value:
                value, column = new_score, col

            beta = min(beta, value)
            if alpha >= beta:
                break

        return column, value


def game_vs_AI(screen, board, difficulty, first_player):
    depth = 5
    turn = AI_PLAYER
    random_move = False
    if difficulty == "easy":
        random_move = True
    elif difficulty == "medium":
        depth = 1
    elif difficulty == "hard":
        depth = 5
    if first_player == "human":
        turn = PLAYER_ONE
    else:
        turn = AI_PLAYER

    game_over = is_game_over(board, PLAYER_ONE_PIECE)
    draw_board(screen, board)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEMOTION and turn == PLAYER_ONE:
                col = int(event.pos[0] / Piece_size)
                draw_hover_piece(screen, col, turn)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER_ONE:
                col = int(event.pos[0] / Piece_size)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    add_piece(board, row, col, PLAYER_ONE_PIECE)
                    if is_game_over(board, PLAYER_ONE_PIECE):
                        print("PLAYER 1 WINS!")
                        game_over = True
                        break
                    else:
                        turn = AI_PLAYER

                    if is_tie(board):
                        game_over = True
                        print("TIE!")
                        break

                    draw_board(screen, board)
                    pygame.display.update()

            if turn == AI_PLAYER:
                if not random_move:
                    col = minimax(board, depth, -math.inf, math.inf, True)[0]
                else:
                    col = random.randint(0, COLS - 1)  # Random move cause how else can I make the game easy?
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    pygame.time.wait(500)
                    add_piece(board, row, col, AI_PLAYER_PIECE)
                    if is_game_over(board, AI_PLAYER_PIECE):
                        print("PLAYER 2 WINS!")
                        game_over = True
                        break
                    else:
                        turn = PLAYER_ONE
                    if is_tie(board):
                        game_over = True
                        print("tie!")
                        break

        draw_board(screen, board)
        pygame.display.update()

    if game_over:
        if is_game_over(board, PLAYER_ONE_PIECE):
            display_message(screen, "PLAYER 1 WINS!")
            draw_border(screen, RED)

        elif is_game_over(board, AI_PLAYER_PIECE):
            display_message(screen, "COMPUTER WINS!")
            draw_border(screen, YELLOW)

        elif is_tie(board):
            display_message(screen, "IT'S TIE")
            draw_border(screen, BLUE)


    # after 5 seconds close the game
    pygame.time.wait(5000)
    pygame.quit()


def check_difficulty_is_valid(difficulty):
    if difficulty == "easy" or difficulty == "medium" or difficulty == "hard":
        return True
    else:
        return False


def check_first_player_is_valid(first_player):
    if first_player == "human" or first_player == "computer":
        return True
    else:
        return False


def main():
    board = create_board()
    pygame.init()

    if ROWS < 4 or COLS < 4 or ROWS > 10 or COLS > 10:
        print("Rows and columns must be between 4 and 10.")
        sys.exit(1)

    screen = pygame.display.set_mode((COLS * Piece_size, (ROWS + 1) * Piece_size))


    pygame.display.set_caption('Connect 4 - Made by Flory')

    if len(sys.argv) < 3:
        print("Invalid number of arguments.")
        print("Usage: python main.py <opponent> <rows> <columns> [<first_player> <difficulty>]")
        sys.exit(1)

    opponent = sys.argv[1]

    if opponent == "human":
        if len(sys.argv) != 4:
            print("Invalid number of arguments for player vs. player game.")
            print("Usage: python main.py human <rows> <columns>")
            sys.exit(1)
        game_two_players(screen, board)
    elif opponent == "computer":
        if len(sys.argv) != 6:
            print("Invalid number of arguments for player vs. AI game.")
            print("Usage: python main.py computer <rows> <columns> <first_player> <difficulty>")
            sys.exit(1)

        difficulty = sys.argv[5]
        first_player = sys.argv[4]

        if not check_difficulty_is_valid(difficulty):
            print("Invalid difficulty. Choose from 'easy', 'medium', or 'hard'.")
            sys.exit(1)
        if not check_first_player_is_valid(first_player):
            print("Invalid first player. Choose from 'human' or 'computer'.")
            sys.exit(1)

        while True:
            game_vs_AI(screen, board, difficulty, first_player)
    else:
        print("Invalid opponent. Choose from 'human' or 'computer'.")
        sys.exit(1)


if __name__ == '__main__':
    main()
