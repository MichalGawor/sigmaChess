
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from board import *

##test if piecePawn can move one square
##TODO add test for both factions

board= ChessBoard()

board.PRINTBOARD()
print("\n")

piece = board.getPiece(1,1)
board.movePiece(piece,1,2)
piece = board.getPiece(0,6)
board.movePiece(piece,0,5)

piece= board.getPiece(2,0)
board.movePiece(piece,0,2)

board.PRINTBOARD()


