from board import ChessBoard
from pieces import *
import random

class MoveNode:
    def __init__(self, move, children, parent):
        self.actualCoordinates = move[0]
        self.targetCoordinates = move[1]
        self.children = children
        self.parent = parent
        self.pointAdvantage = None
        self.depth = 1

    def getDepth(self):
        depth = 1
        highestNode = self
        while True:
            if highestNode.parent is not None:
                highestNode = highestNode.parent
                depth += 1
            else:
                return depth

    def getActualCoordinates(self):
        return self.actualCoordinates

    def getTargetCoorinates(self):
        return self.targetCoordinates

    def __gt__(self, other):
        return self.pointAdvantage > other.pointAdvantage

    def __lt__(self, other):
        return self.pointAdvantage < other.pointAdvantage

    def __eq__(self, other):
        return self.pointAdvantage == other.pointAdvantage



class Bot:
    def __init__(self, depth, side, board, isSecondBot=False):
        self.board = board
        self.depth = depth
        self.side = side
        self.isSecondBot = isSecondBot

    def getActualBoard(self):
        return self.board

    def setActualBoard(self, board):
        self.board = board

    def generateMoveTree(self):
        moveTree = []
        allMoves = self.board.getAllMoves(self.side)
        for move in allMoves:
            moveTree.append(MoveNode(move, [], None))
        for node in moveTree:
            self.board.movePiece(self.board.getPiece(node.actualCoordinates[0], node.actualCoordinates[1]),
                                 node.targetCoordinates[0], node.targetCoordinates[1])
            self.populateNodeChildren(node)
            self.board.undoMove()
        return moveTree

    def populateNodeChildren(self, node):
        node.pointAdvantage = self.evaluateMove(self.side)
        node.depth = node.getDepth()
        if node.depth == self.depth:
            return

        currentFaction = self.board.getOppositeFaction(self.board.whoMoved)
        legalMoves = self.board.getAllMoves(currentFaction)
        if len(legalMoves) == 0:
            node.pointAdvantage = 0
            return

        for move in legalMoves:
            node.children.append(MoveNode(move, [], node))
            pieceToMove = self.board.getPiece(move[0][0], move[0][1])
            self.board.movePiece(pieceToMove, move[1][0], move[1][1])
            self.populateNodeChildren(node.children[-1])
            self.board.undoMove()

    def evaluateMove(self, faction):
        moveValue = 0
        moveValue += 0.5 * len(self.board.getAllMoves(faction))
        for i in range(8):
            for j in range(8):
                piece = self.board.getPiece(i, j)
                if piece is not None:
                    if type(piece) == piecePawn:
                        if piece.faction == faction:
                            moveValue += 1
                            continue
                        else:
                            moveValue -= 1
                            continue
                    if type(piece) == pieceBishop or type(piece) == pieceKnight:
                        if piece.faction == faction:
                            moveValue += 3
                            continue
                        else:
                            moveValue -= 3
                            continue
                    if type(piece) == pieceRook:
                        if piece.faction == faction:
                            moveValue += 5
                            continue
                        else:
                            moveValue -= 5
                            continue
                    if type(piece) == pieceQueen:
                        if piece.faction == faction:
                            moveValue += 9
                            continue
                        else:
                            moveValue -= 9
                            continue
                    if type(piece) == pieceKing:
                        if piece.faction == faction:
                            moveValue += 200
                            continue
                        else:
                            moveValue -= 200
                            continue
        return moveValue

    def getOptimalPointAdvantage(self, node):
        if node.children:
            for child in node.children:
                child.pointAdvantage = self.getOptimalPointAdvantage(child)
            if not self.isSecondBot:
                if node.children[0].depth % 2 == 1:
                    return max(node.children).pointAdvantage
                else:
                    return min(node.children).pointAdvantage
            else:
                if node.children[0].depth % 2 == 0:
                    return max(node.children).pointAdvantage
                else:
                    return min(node.children).pointAdvantage
        else:
            return node.pointAdvantage

    def getBestMoves(self, moveTree):
        bestMoves = []
        for node in moveTree:
            node.pointAdvantage = self.getOptimalPointAdvantage(node)
            if not bestMoves:
                bestMoves.append(node)
            elif node > bestMoves[0]:
                bestMoves = []
                bestMoves.append(node)
            elif node == bestMoves[0]:
                bestMoves.append(node)

        return [(node.actualCoordinates, node.targetCoordinates) for node in bestMoves]

    def getBotMove(self):
        moveTree = self.generateMoveTree()
        bestMoves = self.getBestMoves(moveTree)
        return random.choice(bestMoves)
