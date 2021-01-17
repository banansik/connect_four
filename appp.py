from flask import Flask, render_template, request, redirect,url_for
import numpy as np
import random
import math
from stale import *
from main_functions import *
from computer_moves import *

app = Flask(__name__)






@app.route("/test", methods=['POST', 'GET'] )
def test():
    global board, vs, game_mode
    board = create_board()
    game_mode=int(request.form.get('mode'))

    return redirect('new_game')


@app.route('/new_game')
def hej():
    return  render_template('index.html', board = board)

@app.route("/")
def main():
    return render_template('start.html')


@app.route("/echo", methods=['POST', 'GET'])
def echo():
    global turn, prev_turn, board
    refresh = 0

    if game_mode == 0:
        if turn == 0:
            player = 'player two'
            col=int(request.form.get('col'))
            if is_valid_location(board,col):

                row = get_next_open_row(board,col)
                drop_piece(board, col, row, PLAYER_PIECE)
        else:
            player = 'player one'
            col=int(request.form.get('col'))
            if is_valid_location(board, col):

                row = get_next_open_row(board, col)
                drop_piece(board, col, row, AI_PIECE)



    if game_mode == 1:
        if turn == 0:
            col = int(request.form.get('col'))
            row = get_next_open_row(board, col)
            player = 'player two'
            if is_valid_location(board, col):
                row=get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)
            refresh = 1

        else:
            col, minimax_score = minimax(board,2, -math.inf, math.inf, True)
            row = get_next_open_row(board, col)
            player = 'player one'
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)



    if winning_move(board, turn+1) and turn == 0:
        win = 'player 1 win'
    elif winning_move(board, turn+1) and turn == 1:
        win = 'player 2 win'
    else:
        win = ''
    full = ' '
    if board[5][0] > 0:
        full = 1

    turn += 1
    prev_turn += 1
    turn = turn % 2
    prev_turn = prev_turn % 2

    return render_template('index.html',board = np.flip(board),col = col, player = player, win = win, full=full, refresh = refresh )



if __name__== "__main__":
    app.run(debug=True)
