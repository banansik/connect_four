import numpy as np
from stale import *


def make_board():
    board = np.zeros((diag, col_le), dtype =int)
    return board

def create_board():
	board = np.zeros((diag, col_le), dtype = int)
	return board
def chceck_col(board):
    if board[diag - 1][col_le - 1] != 0:
        return True

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[diag - 1][col] == 0

def get_next_open_row(board, col):
	#zwraca nasteny wolne miejsce na zeton w danej kolumnie
	for r in range(diag):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def win_checker(board, piece):
	# poziomo
	for c in range(col_le - 3):
		for r in range(diag):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# pionowo
	for c in range(col_le):
		for r in range(diag - 3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# po skosie w gore
	for c in range(col_le - 3):
		for r in range(diag - 3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# po skosie w dol
	for c in range(col_le - 3):
		for r in range(3, diag):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True
