import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from board import *


board = ChessBoard()
while not board.isVictory():
    board.PRINTBOARD()
    allMoves = board.getAllMoves(board.getOppositeFaction(board.whoMoved))
    print(allMoves)
    x = input("Type X of piece to move")
    y = input("Type Y of piece to move")
    newX = input("Type X where to move")
    newY = input("type Y where to move")
    while not board.movePiece(board.getPiece(int(x), int(y)), int(newX), int(newY)):
        x = input("Type X of piece to move")
        y = input("Type Y of piece to move")
        newX = input("Type X where to move")
        newY = input("type Y where to move")