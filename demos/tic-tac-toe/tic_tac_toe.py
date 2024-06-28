import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("---------")

def check_winner(board, player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def get_player_move(board):
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            row, col = divmod(move, 3)
            if 0 <= move < 9 and board[row][col] == " ":
                return row, col
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")

def get_computer_move(board):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return random.choice(empty_cells)

def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)
        
        if current_player == "X":
            row, col = get_player_move(board)
        else:
            row, col = get_computer_move(board)
            print(f"Computer chose: {row * 3 + col + 1}")

        board[row][col] = current_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"{'You' if current_player == 'X' else 'Computer'} win!")
            break
        elif is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    print("Welcome to Tic-Tac-Toe!")
    play_game()