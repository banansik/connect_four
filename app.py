from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import random
import math
from stale import *
from main_functions import *
from computer_moves import *

app = Flask(__name__)
games = {}
gameNumber = 1
app.secret_key = 'lol'


def multi_start():
    global current_player_object
    global current_player
    global komputer
    global gameNumber
    global games
    global game
    global game_mode
    global kolejka
    kolejka = -1
    game_mode = 3
    game = {'komputer': False,
            'current_player': 'first',
            'current_player_object': '',
            'multi': False,
            'full': False,
            'began': False,
            'number': gameNumber}

    games[gameNumber] = game
    session['game'] = gameNumber





def win_check():
    global board
    if win_checker(board, turn + 1):
        return True

@app.route('/siec')
def siec():
    global games
    return render_template('siec.html', games=games)

@app.route('/create')
def create():
    global board, turn, game_mode
    global games
    global gameNumber
    game_mode = 3
    turn = 0
    board = create_board()
    if len(games)!=0 and games[session['game']]['full'] == True:
        turn = 0
        player = session['player']
        return render_template('index.html',board = board,player = player, gra=games[session['game']])
    multi_start()
    session['player'] = 'first'
    session['game'] = gameNumber
    games[session['game']]['multi'] = True #games[1][multi]=True
    return render_template('poczekalnia.html', gra=games[session['game']])


@app.route('/join')
def join():
    global games
    gameNumber = request.args.get('gameNumber')
    if games[int(gameNumber)]['full'] == False:
        session['game'] = int(gameNumber)
        session['player'] = 'second'
        games[session['game']]['full'] = True
        games[int(gameNumber)]['began'] = True
        game = games[session['game']]
    if games[int(gameNumber)] == games[int(session['game'])] and games[int(gameNumber)]['began'] == True:
        pass
    return redirect(url_for('wait'))

@app.route('/wait')
def wait():
    global games, board, kolejka, turn, win
    game = request.args.get('gra')
    game = games[session['game']]
    dziala = session['player']
    full0 = ' '
    if board[5][0] > 0:
        full0 = 1
    full1 = ' '
    if board[5][1] > 0:
        full1 = 1
    full2 = ' '
    if board[5][2] > 0:
        full2 = 1
    full3 = ' '
    if board[5][3] > 0:
        full3 = 1
    full4 = ' '
    if board[5][4] > 0:
        full4 = 1
    full5 = ' '
    if board[5][5] > 0:
        full5 = 1
    full6 = ' '
    if board[5][6] > 0:
        full6 = 1
    if win_check() and kolejka == 1:
        win = 1
        return render_template('win.html',board = np.flip(board), turn = win+1)
    if win_check() and kolejka == 0:
        win = 0
        return render_template('win.html',board = np.flip(board), turn = win+1)
    if session['player'] == 'first' and kolejka == 0:

            return render_template('index.html',kolejka=kolejka, board = np.flip(board),full6 = full6,full5 = full5, full4 = full4, full3 = full3, full2 = full2,full1 = full1,full0 = full0, game_mode = game_mode)

    if session['player'] == 'second' and kolejka == 1:

        return render_template('index.html', board = np.flip(board),full6 = full6,full5 = full5, full4 = full4, full3 = full3, full2 = full2,full1 = full1,full0 = full0, game_mode = game_mode)
    if games[session['game']]['current_player'] == session['player']:

        return render_template('wait.html',board = np.flip(board), gra=game, dziala=dziala)



    return render_template('wait.html',board = np.flip(board), gra=game, dziala = dziala)


@app.route("/test", methods=['POST', 'GET'] )
def test():
    global board, vs, game_mode
    board = create_board()
    game_mode=int(request.form.get('mode'))

    return redirect('new_game')

@app.route('/revange_AI')
def revange():
    global board, game_mode, turn
    board = create_board()
    game_mode=1
    turn = 0
    return  render_template('index.html', board = board)



@app.route("/")
def main():
    global turn
    multi_start()
    turn = 0
    return render_template('start.html')

@app.route("/AI")
def AI():
    global game_mode, board
    game_mode = 1
    board = make_board()
    return  render_template('index.html', board = board)

@app.route("/vs")
def vs():
    global game_mode, board
    board = make_board()
    game_mode = 0
    return  render_template('index.html', board = board)


@app.route("/echo", methods=['POST', 'GET'])
def echo():
    global turn, prev_turn, board,kolejka
    refresh = 0

    if game_mode == 0:
        if turn == 0:
            player = 'player two'
            col=int(request.form.get('col'))
            if is_valid_location(board,col):

                row = get_next_open_row(board,col)
                drop_piece(board, row, col, PLAYER_PIECE)
        else:
            player = 'player one'
            col=int(request.form.get('col'))
            if is_valid_location(board, col):

                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)



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


            col = select_best_option(board, AI_PIECE)
            row = get_next_open_row(board, col)
            player = 'player one'
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
    if game_mode == 3:
        if turn == 0:
            player = 'player two'
            col, minimax_score = minimax(board,3, -math.inf, math.inf, True)
            #col=int(request.form.get('col'))
            if is_valid_location(board,col):

                row = get_next_open_row(board,col)
                drop_piece(board, row, col, PLAYER_PIECE)
                if win_checker(board, turn + 1):
                    win = 1
                    return render_template('win.html', turn = win, board = np.flip(board) )
                kolejka = 1

                turn += 1
                turn = turn % 2


                return redirect(url_for('wait'))


        else:

            player = 'player one'
            col=int(request.form.get('col'))
            if is_valid_location(board, col):

                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                if win_checker(board, turn + 1):
                    win = 2
                    return render_template('win.html', turn = win, board = np.flip(board))
                kolejka = 0
                turn += 1
                turn = turn % 2


                return redirect(url_for('wait'))





    if win_checker(board, turn + 1) and turn == 0:
        win = 'player 1 win'
        return render_template('win.html', board = np.flip(board), turn = turn+1 )
    elif win_checker(board, turn + 1) and turn == 1 and game_mode == 1:
        win = 'player 2 win'
        return render_template('win.html', board = np.flip(board), turn = 'AI' )
    elif win_checker(board, turn + 1) and turn == 1:
        win = 'player 2 win'
        return render_template('win.html', board = np.flip(board), turn = turn+1 )
    else:
        win = ''
    full0 = ' '
    if board[5][0] > 0:
        full0 = 1
    full1 = ' '
    if board[5][1] > 0:
        full1 = 1
    full2 = ' '
    if board[5][2] > 0:
        full2 = 1
    full3 = ' '
    if board[5][3] > 0:
        full3 = 1
    full4 = ' '
    if board[5][4] > 0:
        full4 = 1
    full5 = ' '
    if board[5][5] > 0:
        full5 = 1
    full6 = ' '
    if board[5][6] > 0:
        full6 = 1

    turn += 1
    prev_turn += 1
    turn = turn % 2
    prev_turn = prev_turn % 2
    global full_cols
    full ={}
    full = full_check(board)

    return render_template('index.html',board = np.flip(board),col = col, player = player, win = win, full6 = full6, refresh = refresh,full5 = full5, full4 = full4, full3 = full3, full2 = full2,full1 = full1,full0 = full0, game_mode = game_mode)

def full_check(board):
    full_cols = {'lol':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0}
    for n in range(col_le):
        if board[0][n] > 0:
            full_cols[n] = 1
    return full_cols





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=True)
