import sys
import importlib
import numpy as np
import pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Game board size
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS


def draw_lines(screen, color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)


def draw_figures(screen, board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(
                    screen,
                    WHITE,
                    (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                    SQUARE_SIZE // 3,
                    15,
                )
            elif board[row][col] == 2:
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                pygame.draw.line(
                    screen,
                    WHITE,
                    (x + SQUARE_SIZE // 4, y + SQUARE_SIZE // 4),
                    (x + 3 * SQUARE_SIZE // 4, y + 3 * SQUARE_SIZE // 4),
                    15,
                )
                pygame.draw.line(
                    screen,
                    WHITE,
                    (x + 3 * SQUARE_SIZE // 4, y + SQUARE_SIZE // 4),
                    (x + SQUARE_SIZE // 4, y + 3 * SQUARE_SIZE // 4),
                    15,
                )


def get_winner(board):
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] != 0:
            return board[row][0]

    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] != 0:
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]

    return None


def is_board_full(board):
    return not np.any(board == 0)


def minimax(board, depth, is_maximizing):
    winner = get_winner(board)
    if winner == 2:
        return 10 - depth
    if winner == 1:
        return depth - 10
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax(board, depth + 1, False)
                    board[row][col] = 0
                    best_score = max(best_score, score)
        return best_score

    best_score = float("inf")
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 1
                score = minimax(board, depth + 1, True)
                board[row][col] = 0
                best_score = min(best_score, score)
    return best_score


def best_move(board):
    best_score = -float("inf")
    best_choice = None

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    best_choice = (row, col)

    return best_choice


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")
    screen.fill(BLACK)

    board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)
    player = 1
    game_over = False
    winner = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = event.pos
                row = mouse_y // SQUARE_SIZE
                col = mouse_x // SQUARE_SIZE

                if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS and board[row][col] == 0:
                    board[row][col] = player
                    winner = get_winner(board)

                    if winner is not None:
                        game_over = True
                    elif is_board_full(board):
                        game_over = True
                    else:
                        player = 2

                    if not game_over and player == 2:
                        move = best_move(board)
                        if move is not None:
                            board[move[0]][move[1]] = 2
                            winner = get_winner(board)
                            if winner is not None:
                                game_over = True
                            elif is_board_full(board):
                                game_over = True
                            else:
                                player = 1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)
                player = 1
                winner = None
                game_over = False

        screen.fill(BLACK)
        draw_lines(screen)
        draw_figures(screen, board)

        if game_over and winner == 1:
            draw_lines(screen, GREEN)
        elif game_over and winner == 2:
            draw_lines(screen, RED)
        elif game_over:
            draw_lines(screen, GRAY)

        pygame.display.update()


if __name__ == "__main__":
    main()
