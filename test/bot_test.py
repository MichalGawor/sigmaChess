import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from board import *
from bot import *

if __name__ == "__main__":
    actualBoard = ChessBoard()
    bot1 = Bot(3, factionColor.FACTION_WHITE, actualBoard, isSecondBot=False)
    bot2 = Bot(3, factionColor.FACTION_BLACK, actualBoard, isSecondBot=True)
    while not actualBoard.isVictory():
        bot1_move = bot1.getBotMove()

        print()
        print("BOT1 CHOOSES MOVE")
        print(bot1_move)
        print()

        pieceToMove = actualBoard.getPiece(bot1_move[0][0], bot1_move[0][1])
        print(pieceToMove)
        actualBoard.movePiece(pieceToMove, bot1_move[1][0], bot1_move[1][1])

        actualBoard.PRINTBOARD()
        print("\n")

        bot2.setActualBoard(actualBoard)
        bot2_move = bot2.getBotMove()

        print()
        print("BOT2 CHOOSES MOVE")
        print(bot2_move)
        print()

        pieceToMove = actualBoard.getPiece(bot2_move[0][0], bot2_move[0][1])
        actualBoard.movePiece(pieceToMove, bot2_move[1][0], bot2_move[1][1])

        actualBoard.PRINTBOARD()
        print("\n")