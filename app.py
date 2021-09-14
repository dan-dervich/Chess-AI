import chess
import chess.svg
import chess.polyglot
import time
import traceback
import chess.pgn
import chess.engine
from flask import Flask, Response, request
import webbrowser
import pyttsx3
import datetime


pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]
bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]
rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]
queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]
kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]
def evaluate_board():
    if board.is_checkmate():
            if board.turn:
                return -9999
            else:
                return 9999
    if board.is_stalemate():
            return 0
    if board.is_insufficient_material():
            return 0
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))

    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)
    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                        for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                            for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                            for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                        for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                            for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                        for i in board.pieces(chess.KING, chess.BLACK)])

    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if board.turn:
        return eval
    else:
        return -eval
    try:
        move = chess.polyglot.MemoryMappedReader("C:/Users/Messi/OneDrive/Documents/Desktop/chess ai/books/human.bin").weighted_choice(board).move
        return move
    except:
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            board.push(move)
            boardValue = -alphabeta(-beta, -alpha, depth - 1)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if (boardValue > alpha):
                alpha = boardValue
            board.pop()
        return bestMove

def alphabeta(alpha, beta, depthleft):
    bestscore = -9999
    if (depthleft == 0):
        return quiesce(alpha, beta)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha, depthleft - 1)
        board.pop()
        if (score >= beta):
            return score
        if (score > bestscore):
            bestscore = score
        if (score > alpha):
            alpha = score
    return bestscore

def quiesce(alpha, beta):
    stand_pat = evaluate_board()
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat 
        for move in board.legal_moves:
            if board.is_capture(move):
                board.push(move)
                score = -quiesce(-beta, -alpha)
                board.pop()
                if (score >= beta):
                    return beta
                if (score > alpha):
                    alpha = score
    return alpha
def selectmove(depth):
    try:
        move = chess.polyglot.MemoryMappedReader("C:/Users/Messi/OneDrive/Documents/Desktop/chess ai/human.bin").weighted_choice(board).move
        # move = chess.polyglot.MemoryMappedReader("C:/Users/your_path/books/computer.bin").weighted_choice(board).move
        # move = chess.polyglot.MemoryMappedReader("C:/Users/your_path/books/pecg_book.bin").weighted_choice(board).move
        return move
    except:
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            board.push(move)
            boardValue = -alphabeta(-beta, -alpha, depth - 1)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if (boardValue > alpha):
                alpha = boardValue
            board.pop()
        return bestMove
# mov = selectmove(3)
# board.push(mov)
# board# use this for human move, where e5 is the example move
count = 0
movehistory = []
game = chess.pgn.Game()
board = chess.Board() 
while not board.is_game_over(claim_draw=True):
    if board.turn:
        count += 1
        print(f'\n{count}]\n')
        move = selectmove(3)
        board.push(move)
        print(board)
        print()
    else:
        move = selectmove(3)
        board.push(move)
        print(board)
        game.add_line(movehistory)
game.headers["Event"] = "Self Tournament 2020"
game.headers["Site"] = "Pune"
game.headers["Date"] = str(datetime.datetime.now().date())
game.headers["Round"] = 1
game.headers["White"] = "Ai"
game.headers["Black"] = "Ai"
game.headers["Result"] = str(board.result(claim_draw=True))
print(game)
# SVG(chess.svg.board(board=board,size=400))
count = 0
movehistory = []
game = chess.pgn.Game()
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci("/mnt/c/users/messi/onedrive/documents/desktop/chess ai/stockfish.exe")
while not board.is_game_over(claim_draw=True):
    if board.turn:
        count += 1
        print(f'\n{count}]\n')
        move = engine.play(board, chess.engine.Limit(time=0.1))
        movehistory.append(move.move)
        board.push(move.move)
        print(board)
    else:
        move = selectmove(3)
        movehistory.append(move)
        board.push(move)
        print(board)
        game.add_line(movehistory)
game.headers["Result"] = str(board.result(claim_draw=True))
print(game)
# SVG(chess.svg.board(board=board, size=400))
# board.push_san("e5")
board


def aimove():
    move = selectmove(3)
    board.push(move)# Searching Stockfish's Move
def stockfish():
    engine = chess.engine.SimpleEngine.popen_uci(
        "C:/Users/Messi/OneDrive/Documents/Desktop/chess ai/stockfish.exe")
    move = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(move.move)
app = Flask(__name__)# Front Page of the Flask Web Page
@app.route("/")
def main():
    global count, board
    ret = '<html><head>'
    ret += '<style>input {font-size: 20px; } button { font-size: 20px; }</style>'
    ret += '</head><body>'
    ret += '<img width=510 height=510 src="/board.svg?%f"></img></br></br>' % time.time()
    ret += '<form action="/game/" method="post"><button name="New Game" type="submit">New Game</button></form>'
    ret += '<form action="/undo/" method="post"><button name="Undo" type="submit">Undo Last Move</button></form>'
    ret += '<form action="/move/"><input type="submit" value="Make Human Move:"><input name="move" type="text"></input></form>'
    ret += '<form action="/dev/" method="post"><button name="Comp Move" type="submit">Make Ai Move</button></form>'
    ret += '<form action="/engine/" method="post"><button name="Stockfish Move" type="submit">Make Stockfish Move</button></form>'
    return ret# Display Board
@app.route("/board.svg/")
def board():
    return Response(chess.svg.board(board=board, size=700), mimetype='image/svg+xml')# Human Move
@app.route("/move/")
def move():
    try:
        move = request.args.get('move', default="")
        board.push_san(move)
    except Exception:
        traceback.print_exc()
    return main()# Make Ai’s Move
@app.route("/dev/", methods=['POST'])
def dev():
    try:

        aimove()
    except Exception:
        traceback.print_exc()
    return main()# Make UCI Compatible engine's move
@app.route("/engine/", methods=['POST'])
def engine():
    try:
        stockfish()
    except Exception:
        traceback.print_exc()
    return main()# New Game
@app.route("/game/", methods=['POST'])
def game():
    board.reset()
    return main()# Undo
@app.route("/undo/", methods=['POST'])
def undo():
    try:
        board.pop()
    except Exception:
        traceback.print_exc()
    return main()


board = chess.Board()
webbrowser.open("http://127.0.0.1:5000/")
if __name__ == "__main":
    app.run()
