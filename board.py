from pieces import *
import os.path


class ChessBoard:
    def __init__(self):
        self.boardArray = [[]]
        self.boardArray = self.__spawnPieces()
        self.whoMoved = factionColor.FACTION_BLACK

        # lastMoves is a stack that stores tuples
        # (movingPiece, startingPositionX, startingPositionY, targetPiece, targetPositionX, targetPositionY)
        self.lastMoves = []

    def __createEmptyArray(self):
        hArray = []
        for i in range(8):
            hArray.append([])
            for k in range(8):
                hArray[i].append(None)
        return hArray

    def __spawnPieces(self):
        Path = os.path.dirname(os.path.abspath(__file__))
        boardArray = self.__createEmptyArray()
        boardtemplate = open(Path+ "/boardtemplate.txt", "r")
        for y in range(8):
            line = boardtemplate.readline()
            for x in range(8):
                whatPiece = line[x]
                if whatPiece == "O":
                    boardArray[x][y] = None
                elif whatPiece == "P":
                    if y <= 3:
                        boardArray[x][y] = piecePawn(x, y, factionColor.FACTION_WHITE)
                    else:
                        boardArray[x][y] = piecePawn(x, y, factionColor.FACTION_BLACK)
                elif whatPiece == "R":
                    if y <= 3:
                        boardArray[x][y] = pieceRook(x, y, factionColor.FACTION_WHITE)
                    else:
                        boardArray[x][y] = pieceRook(x, y, factionColor.FACTION_BLACK)
                elif whatPiece == "N":
                    if y <= 3:
                        boardArray[x][y] = pieceKnight(x, y, factionColor.FACTION_WHITE)
                    else:
                        boardArray[x][y] = pieceKnight(x, y, factionColor.FACTION_BLACK)
                elif whatPiece == "B":
                    if y <= 3:
                        boardArray[x][y] = pieceBishop(x, y, factionColor.FACTION_WHITE)
                    else:
                        boardArray[x][y] = pieceBishop(x, y, factionColor.FACTION_BLACK)
                elif whatPiece == "Q":
                    if y <= 3:
                        boardArray[x][y] = pieceQueen(x, y, factionColor.FACTION_WHITE)
                    else:
                        boardArray[x][y] = pieceQueen(x, y, factionColor.FACTION_BLACK)
                elif whatPiece == "K":
                    if y <= 3:
                        boardArray[x][y] = pieceKing(x, y, factionColor.FACTION_WHITE)
                    else:
                        boardArray[x][y] = pieceKing(x, y, factionColor.FACTION_BLACK)
        return boardArray

    def getAllMoves(self, faction):
        '''
        This function finds all possible moves for a given faction

        :param faction: faction for which all moves are to be returned
        :return: [coords, move] where coords is a tuple of (actualX, actualY) coordinates of piece and move is (newX, nexY) tuple
        is a tuple (newX, newY) of coordinates where it can move
        '''

        legalMoves = []
        for x in range(8):
            for y in range(8):
                if self.boardArray[x][y] is not None:
                    piece = self.getPiece(x, y)
                    # Pawn
                    if type(piece) == piecePawn and piece.faction == faction:
                        # Tuples of moves which may be possible for pawn
                        pawnPossibleMoves = [(0, 1), (0, -1), (0, 2), (0, -2)]
                        # Tuples of attacks which may be possible for pawn
                        pawnPossibleAttacks = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
                        for move in pawnPossibleMoves:
                            if piece.checkMove(self.boardArray, coordHorizontal=(x + move[0]) % len(self.boardArray[0]),
                                               coordVert=(y + move[1]) % len(self.boardArray[0])):
                                legalMove = ((x, y), ((x + move[0]) % 8, (y + move[1]) % 8))
                                legalMoves.append(legalMove)
                        for attack in pawnPossibleAttacks:
                            if piece.checkAttack(self.boardArray, coordHorizontal=(x + attack[0]) % len(self.boardArray[0]),
                                                 coordVert=(y + attack[1]) % len(self.boardArray[0])):
                                legalMove = ((x, y), ((x + attack[0]) % 8, (y + attack[1]) % 8))
                                legalMoves.append(legalMove)
                        continue

                    # Rook
                    if type(piece) == pieceRook and piece.faction == faction:
                        # Tuples of moves which may be possible for rook (works as attack as well)
                        rookPossibleMoves = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
                                             (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)]
                        for move in rookPossibleMoves:
                            if piece.checkMove(self.boardArray, coordHorizontal=(x + move[0]) % len(self.boardArray[0]),
                                               coordVert=(y + move[1]) % len(self.boardArray[0])):
                                legalMove = ((x, y), ((x + move[0]) % 8, (y + move[1]) % 8))
                                legalMoves.append(legalMove)
                        continue

                    # Knight
                    if type(piece) == pieceKnight and piece.faction == faction:
                        # Tuples of moves which may be possible for knight (works as attack as well)
                        knightPossibleMoves = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
                        for move in knightPossibleMoves:
                            if piece.checkMove(self.boardArray, coordHorizontal=(x + move[0]) % len(self.boardArray[0]),
                                               coordVert=(y + move[1]) % len(self.boardArray[0])):
                                legalMove = ((x, y), ((x + move[0]) % 8, (y + move[1]) % 8))
                                legalMoves.append(legalMove)
                        continue

                    # Bishop
                    if type(piece) == pieceBishop and piece.faction == faction:
                        # Tuples of moves which may be possible for bishop (works as attack as well)
                        bishopPossibleMoves = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                               (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7),
                                               (8, -8)]
                        for move in bishopPossibleMoves:
                            if piece.checkMove(self.boardArray, coordHorizontal=(x + move[0]) % 8, coordVert=(y + move[1]) % 8):
                                legalMove = ((x, y), ((x + move[0]) % 8, (y + move[1]) % 8))
                                legalMoves.append(legalMove)
                        continue


                    # Queen
                    if type(piece) == pieceQueen and piece.faction == faction:
                        # Tuples of moves which may be possible for queen (works as attack as well)
                        queenPossibleMoves = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                              (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (8, -8),
                                              (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
                                              (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)]
                        for move in queenPossibleMoves:

                            if piece.checkMove(self.boardArray, coordHorizontal=(x + move[0]) % len(self.boardArray[0]),
                                               coordVert=(y + move[1]) % len(self.boardArray[0])):
                                legalMove = ((x, y), ((x + move[0]) % 8, (y + move[1]) % 8))
                                legalMoves.append(legalMove)
                        continue

                    # King
                    if type(piece) == pieceKing and piece.faction == faction:
                        #Tuples of moves which may be possible for king
                        kingPossibleMoves = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
                        #Tuples of attacks which may be possible for king
                        kingPossibleAttacks = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
                        for move in kingPossibleMoves:
                            if piece.checkMove(self.boardArray, coordHorizontal=(x + move[0]) % len(self.boardArray[0]),
                                               coordVert=(y + move[1]) % len(self.boardArray[0])):
                                if not self.tileIsChecked((x + move[0]) % 8, (y + move[1]) % 8, self.getOppositeFaction(piece.faction)):
                                    legalMove = ((x, y), ((x + move[0]) % 8, (y + move[1]) % 8))
                                    legalMoves.append(legalMove)

                        for attack in kingPossibleAttacks:
                            if piece.checkAttack(self.boardArray, coordHorizontal=(x + attack[0]) % len(self.boardArray[0]),
                                               coordVert=(y + attack[1]) % len(self.boardArray[0])):
                                if not self.tileIsChecked((x + attack[0]) % 8, (y + attack[1]) % 8, self.getOppositeFaction(piece.faction)):
                                    legalMove = ((x, y), ((x + attack[0]) % 8, (y + attack[1]) % 8))
                                    legalMoves.append(legalMove)
                        continue
        return legalMoves

    def movePiece(self, pieceToMove, xNew, yNew):
        """this method  performs both attack and move"""
        # check if it can move
        isAttack = pieceToMove.checkAttack(self.boardArray, coordHorizontal=xNew, coordVert=yNew)
        if isAttack == True and pieceToMove.faction != self.whoMoved:
            self.__move(pieceToMove, xNew, yNew)
            return True

        # check if it can attack
        isLegal = pieceToMove.checkMove(self.boardArray, coordHorizontal=xNew, coordVert=yNew)
        if isLegal == True and pieceToMove.faction != self.whoMoved:
            self.__move(pieceToMove, xNew, yNew)
            return True

        # cant do neither
        return False

    def __move(self, pieceToMove, xNew, yNew):
        xCurrent = pieceToMove.x
        yCurrent = pieceToMove.y
        lastMove = (pieceToMove, xCurrent, yCurrent, self.boardArray[xNew][yNew], xNew, yNew)
        self.lastMoves.append(lastMove)

        #change coords inside piece object
        pieceToMove.x=xNew
        pieceToMove.y=yNew

        self.boardArray[xNew][yNew] = pieceToMove
        self.whoMoved = pieceToMove.faction
        self.boardArray[xCurrent][yCurrent] = None
        if type(self.boardArray[xNew][yNew]) == piecePawn:
            self.pawnPromotion(xNew, yNew)

    def pawnPromotion(self, xNew, yNew):
        if yNew == 7:
            self.boardArray[xNew][yNew] = pieceQueen(xNew, yNew, factionColor.FACTION_WHITE)
        elif yNew == 0:
            self.boardArray[xNew][yNew] = pieceQueen(xNew, yNew, factionColor.FACTION_BLACK)

    def getPiece(self,coordHorizontal, coordVert):
        return self.boardArray[coordHorizontal][coordVert]

    def PRINTBOARD(self):
        for i in range(8):
            print("")
            for j in range(8):
                if type(self.boardArray[j][7 - i]) is piecePawn:
                    print("P", end="")
                elif type(self.boardArray[j][7-i]) is pieceKing:
                    print("K", end="")
                elif type(self.boardArray[j][7-i]) is pieceBishop:
                    print("B", end="")
                elif type(self.boardArray[j][7-i]) is pieceKnight:
                    print("N", end="")
                elif type(self.boardArray[j][7-i]) is pieceRook:
                    print("R", end="")
                elif type(self.boardArray[j][7-i]) is pieceQueen:
                    print("Q",end="")
                else:
                    print("-", end="")

    def isVictory(self):
        whiteExist = False
        blackExist = False
        for i in range(8):
            for j in range(8):
                piece = self.getPiece(i, j)
                if piece is None:
                    continue
                if type(piece) == pieceKing and piece.faction == factionColor.FACTION_WHITE:
                    whiteExist = True
                if type(piece) == pieceKing and piece.faction == factionColor.FACTION_BLACK:
                    blackExist = True

        if not whiteExist:
            print("Black victory!")
            return True
        if not blackExist:
            print("White victory!")
            return True
        return False

    #function checks if square (x,y) is attacked by faction.
    def tileIsAttacked(self, x, y):
        square=self.boardArray[x][y]
        for i in range(8):
            for j in range(8):
                if self.boardArray[i][j]==None:
                    continue
                if self.boardArray[i][j].faction == square.faction:
                    continue
                if self.boardArray[i][j].faction is not square.faction:
                    if self.getPiece(i, j).checkAttack(self.boardArray, x, y):
                        return True
                    else:
                        continue
        return False

    #function denermines the position of the king belonging to a faction
    def getKing(self, faction):
        for i in range(8):
            for j in range(8):
                king = self.getPiece(i, j)
                if (type(king) == pieceKing) and (king.faction == faction):
                    return i, j


    #function checks whether a king from a faction is under attack
    def isChecked(self, faction):
        king=self.getKing(faction)
        if self.tileIsAttacked(king[0], king[1]):
            return True
        else:
            return False

    #function checks if tile is attacked by given faction
    def tileIsChecked(self, x, y, faction):
        for i in range(8):
            for j in range(8):
                if self.boardArray[i][j] is None:
                    continue
                if self.boardArray[i][j].faction == faction:
                    if self.getPiece(i, j).checkAttack(self.boardArray, x, y):
                        return True
                    else:
                        continue
        return False

    #function which gets opposite faction to the piece's faction
    def getOppositeFaction(self, faction):
        if faction == factionColor.FACTION_BLACK:
            return factionColor.FACTION_WHITE
        else:
            return factionColor.FACTION_BLACK

    # function which undoes move
    def undoMove(self):
        if self.lastMoves:
            lastMove = self.lastMoves[-1]
            movingPiece = lastMove[0]
            startingX = lastMove[1]
            startingY = lastMove[2]
            targetPiece = lastMove[3]
            targetX = lastMove[4]
            targetY = lastMove[5]
            self.lastMoves.pop()

            movingPiece.x = startingX
            movingPiece.y = startingY
            self.boardArray[startingX][startingY] = movingPiece
            self.whoMoved = self.getOppositeFaction(self.whoMoved)
            if targetPiece is not None:
                targetPiece.x = targetX
                targetPiece.y = targetY
                self.boardArray[targetX][targetY] = targetPiece
            else:
              self.boardArray[targetX][targetY] = None


