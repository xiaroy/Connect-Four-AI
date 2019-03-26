import numpy as np
import math
import random

# variables
boardWidth = 7
boardHeight = 6
game_over = False
turn = 0


def create_game_board():
    board = np.zeros((boardHeight, boardWidth))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def remove_piece(board, col):
    for x in range(boardHeight-1, -1, -1):
        board[x][col] = board[x-1][col]
    board[0][col] = 0


def is_valid(board, col):
    return board[boardHeight-1][col] == 0


def is_valid_remove(board, col, piece):
    return board[boardHeight-boardHeight][col] == piece



def get_next_open_row(board, col):
    for x in range(boardHeight):
        if board[x][col] == 0:
            return x


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    for c in range(boardWidth - 3):
        for r in range(boardHeight):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

        # Check vertical locations for win
    for c in range(boardWidth):
        for r in range(boardHeight - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

        # Check positively sloped diaganols
    for c in range(boardWidth - 3):
        for r in range(boardHeight - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

        # Check negatively sloped diaganols
    for c in range(boardWidth - 3):
        for r in range(3, boardHeight):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


print("")
print("Initial " + str(boardHeight) + " by " + str(boardWidth) + " board")
print("")
board = create_game_board()
print(board)


while not game_over:

    if turn == 0:
        print("")
        col = int(input("Player 1 select 0-6 to place 7-13 to remove"))
        if 0 <= col <= 6:
            if is_valid(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)
                print("inserted")
                if winning_move(board, 1):
                    game_over = True
                    print("Player 1 wins")
        else:
            col -= 7
            if is_valid_remove(board, col, 1):
                remove_piece(board, col)
                print("removed")
                if winning_move(board, 1):
                    game_over = True
                    print("Player 1 wins")
        turn += 1

    else:
        print("")
        col = int(input("Player 2 select 0-6 to place 7-13 to remove"))
        if 0 <= col <= 6:
            if is_valid(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                print("inserted")
                if winning_move(board, 2):
                    game_over = True
                    print("Player 2 wins")
        else:
            col -= 7
            if is_valid_remove(board, col, 2):
                remove_piece(board, col)
                print("removed")
                if winning_move(board, 2):
                    game_over = True
                    print("Player 2 wins")
        turn -= 1

    print_board(board)
