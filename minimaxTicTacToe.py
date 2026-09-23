def print_board(board):
    print("\n")
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i + 1]} | {board[i + 2]} ")
        if i < 6:
            print("---+---+---")
    print("\n")


def check_winner(board):
    winning_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]

    for a, b, c in winning_lines:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    return None


def is_draw(board):
    return all(cell != " " for cell in board) and check_winner(board) is None


def available_moves(board):
    return [i for i, cell in enumerate(board) if cell == " "]


def get_player_move(board, player_name):
    while True:
        try:
            move = int(input(f"{player_name}, choose a square (1-9): ").strip())
        except ValueError:
            print("Please enter a valid number from 1 to 9.")
            continue

        if move not in range(1, 10):
            print("Number must be between 1 and 9.")
            continue

        index = move - 1
        if board[index] != " ":
            print("That square is already taken. Try another one.")
            continue

        return index


def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == "O":
        return 1
    if winner == "X":
        return -1
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for move in available_moves(board):
            board[move] = "O"
            score = minimax(board, False)
            board[move] = " "
            best_score = max(best_score, score)
        return best_score

    best_score = float("inf")
    for move in available_moves(board):
        board[move] = "X"
        score = minimax(board, True)
        board[move] = " "
        best_score = min(best_score, score)
    return best_score


def best_computer_move(board):
    best_score = -float("inf")
    best_move = None

    for move in available_moves(board):
        board[move] = "O"
        score = minimax(board, False)
        board[move] = " "
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def play_two_player_game():
    board = [" " for _ in range(9)]
    current_player = "X"

    while True:
        print_board(board)
        move = get_player_move(board, f"Player {current_player}")
        board[move] = current_player

        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Player {winner} wins!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"


def play_vs_computer_game():
    board = [" " for _ in range(9)]
    current_turn = "X"

    while True:
        print_board(board)

        if current_turn == "X":
            move = get_player_move(board, "Player")
            board[move] = "X"
        else:
            move = best_computer_move(board)
            print(f"Computer chooses square {move + 1}") # type: ignore
            board[move] = "O" # type: ignore

        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == "X":
                print("You win!")
            else:
                print("Computer wins!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_turn = "O" if current_turn == "X" else "X"


def main():
    print("Welcome to Tic-Tac-Toe!")
    print("1) Two players")
    print("2) Play against computer")

    while True:
        choice = input("Choose an option (1 or 2): ").strip()
        if choice == "1":
            play_two_player_game()
            break
        if choice == "2":
            play_vs_computer_game()
            break
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
