from flask import Flask, render_template, request, redirect,url_for
import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

app = Flask(__name__)
def make_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT), dtype =int)
    return board

game_over = False
turn = 0
prev_turn = 1
def is_free(board, col):
    return board[5][0] == 0

def next_free_place(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def drop_piece(board, row, col, piece):
    board[row][col] == piece

board = make_board()

def winning_move(board,piece):
    #sprawdzenie horyzontalnie
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    #sprawdzenie wertkalne
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    for c in range(COLUMN_COUNT-3):
        for r in range(3,ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def winning_move_two(board,piece):
    #sprawdzenie horyzontalnie
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    #sprawdzenie wertkalne
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == 1 and board[r+1][c+1] == 2 and board[r+2][c+2] == 2 and board[r+3][c+3] == 2:
                return True

    for c in range(COLUMN_COUNT-3):
        for r in range(3,ROW_COUNT):
            if board[r][c] == 2 and board[r-1][c+1] == 2 and board[r-2][c+2] == 2 and board[r-3][c+3] == 2:
                return True
@app.route('/testa')
def test():
    global board
    board = make_board()
    return redirect('siemaa')
@app.route('/siemaa')
def hej():
    return  render_template('index1v1.html', board = board)

@app.route("/")
def main():

    return render_template('start.html')
def lol():
    global board
    board = make_board()
    return board


@app.route("/versus", methods=['POST'])
def echo():
    global turn, prev_turn
    global board
    col=int(request.form.get('col'))
    row = next_free_place(board, col)






    if turn == 0:
         player = 'player two'
         if is_free(board,col):
             board[row][col] = 1


    else:
        player = 'player one'
        if is_free(board, col):
            row = next_free_place(board, col)
            board[row][col] = 2


    if winning_move(board,turn+1) and turn == 0:
        win = 'player 1 win'
    elif winning_move(board,turn+1) and turn == 1:
        win = 'player 2 win'
    else:
        win = ' '

    turn += 1
    prev_turn +=1
    turn = turn %2
    prev_turn = prev_turn %2
    return render_template('index.html',board = np.flip(board),col = col, player = player, win = win )

if __name__== "__main__":
    app.run(debug=True)
