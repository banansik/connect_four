from stale import *
import random
from main_functions import *
import math

def calc_field(field, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if field.count(piece) == 4:
		score += 1000
	elif field.count(piece) == 3 and field.count(EMPTY) == 1:
		score += 10
	elif field.count(piece) == 2 and field.count(EMPTY) == 2:
		score += 5

	if field.count(opp_piece) == 3 and field.count(EMPTY) == 1:
		score -= 50
	if field.count(opp_piece) == 2 and field.count(EMPTY) == 2:
		score -= 10


	return score

def board_state(board, piece):
	score = 0

	## centralna kolumna
	center_array = []
	for i in list(board[:,3]):
		center_array.append(int(i))
	center_count = center_array.count(piece)
	score += center_count * 6

	## oblicz ruchy w poziomie
	for r in range(diag):
		row_array = []
		for i in list(board[r,:]):
			row_array.append(int(i))
		for c in range(col_le - 3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += calc_field(window, piece)

	## oblicz ruchy w pionie
	for c in range(col_le):
		col_array = []
		for i in list(board[:,c]):
			col_array.append(int(i))
		for r in range(diag - 3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += calc_field(window, piece)

	## oblicz po skosie gora
	for r in range(diag - 3):
		for c in range(col_le - 3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += calc_field(window, piece)

	## po skosie w dol
	for r in range(diag - 3):
		for c in range(col_le - 3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += calc_field(window, piece)

	return score



def get_valid_locations(board):
	valid_locations = []
	for col in range(col_le):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def select_best_option(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = board_state(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col
