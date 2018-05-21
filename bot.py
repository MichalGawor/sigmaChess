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
        self.isCheckmate = False

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
        if self.isCheckmate and not other.isCheckmate:
            return True
        if self.isCheckmate and other.isCheckmate:
            return False
        if self.isCheckmate and other.isCheckmate:
            return False
        return self.pointAdvantage > other.pointAdvantage

    def __lt__(self, other):
        if not self.isCheckmate and other.isCheckmate:
            return True
        if self.isCheckmate and not other.isCheckmate:
            return False
        if self.isCheckmate and other.isCheckmate:
            return False
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
        if self.board.factionLost(self.board.getOppositeFaction(self.side)):
            node.isCheckmate = True

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
        return self.alphaBeta(node, -1e8, 1e8)

    def alphaBeta(self, node, alpha, beta):
        if not node.children:
            return node.pointAdvantage
        if node.children[0].depth % 2 == 0: #enemy move
            for child in node.children:
                beta = min(beta, self.alphaBeta(child, alpha, beta))
                if alpha >= beta:
                    break
            return beta
        else:
            for child in node.children:
                alpha = max(alpha, self.alphaBeta(child, alpha, beta))
                if alpha >= beta:
                    break
            return alpha

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
