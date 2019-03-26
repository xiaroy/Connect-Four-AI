import numpy as np
import math
import random

# variables
ROW_COUNT = 6
COLUMN_COUNT = 7
game_over = False
turn = 0
EMPTY = 0
player = 0
ai = 1
player_piece = 1
ai_piece = 2
WINDOW_LENGTH = 4


def create_game_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def remove_piece(board, col):
    for x in range(ROW_COUNT-1, -1, -1):
        board[x][col] = board[x+1][col]
    board[ROW_COUNT][col] = 0


def is_valid(board, col):
    return board[ROW_COUNT-1][col] == 0


def is_terminal_node(board):
	return winning_move(board, player_piece) or winning_move(board, ai_piece) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, ai_piece):
                return (None, 100000000000000)
            elif winning_move(board, ai_piece):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, ai_piece))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, ai_piece)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, ai_piece)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value



def is_valid_remove(board, col, piece):
    return board[ROW_COUNT-ROW_COUNT][col] == piece



def get_next_open_row(board, col):
    for x in range(ROW_COUNT):
        if board[x][col] == 0:
            return x


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

        # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

        # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

        # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


def evaluate_window(window, piece):
    score = 0
    opp = player_piece
    if piece == player_piece:
        opp = ai_piece

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp) == 3 and window.count(EMPTY) == 1:
        score -= 10

    return score

def score_position(board, piece):
    score = 0

    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window,piece)

    for c in range (COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range (WINDOW_LENGTH)]
            score += evaluate_window(window,piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range (WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    return score



def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -1000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row ,col ,piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


print("")
print("Initial " + str(ROW_COUNT) + " by " + str(COLUMN_COUNT) + " board")
print("")
board = create_game_board()
print(board)

turn = random.randint(player, ai)

while not game_over:

    if turn == player:
        print("")
        col = int(input("Player 1 select 0-6 to place 7-13 to remove"))
        if 0 <= col <= 6:
            if is_valid(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, player_piece)
                print("Player move inserted")
                if winning_move(board, player_piece):
                    game_over = True
                    print("Player 1 Wins")
        else:
            col -= 7
            if is_valid_remove(board, col, player_piece):
                remove_piece(board, col)
                print("removed")
                if winning_move(board, player_piece):
                    game_over = True
                    print("Player 1 Wins")
        turn += 1

    if turn == ai and not game_over:
        print("")
        col, minimax_score = minimax(board, 6, -math.inf, math.inf, True)
        if is_valid(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, ai_piece)
            print("Ai move inserted")

            if winning_move(board, ai_piece):
                game_over = True
                print("AI Player Wins")

        turn -= 1

    print_board(board)
