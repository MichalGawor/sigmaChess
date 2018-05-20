from tkinter import *

import sys
sys.path.append("/home/vonvirus/Documents/sigmaChess/")
print(sys.path)
from board import ChessBoard
from controller.events import EventHandler
from controller.networking.multiplayer import ConnectionHandler
from view.appwindow import AppWindow


class SigmaChess:
    def __init__(self):
        self.root = Tk()

        #board client handles logic of chess board moves and attacks
        self.boardClient = ChessBoard()
        #view client handles drawing everything
        self.viewClient= AppWindow(self.root, self.boardClient)
        self.viewClient.pack()

        # connection handler makes chess playable in multiplayer
        self.multiplayerClient = ConnectionHandler()
        #event handler handles event performed on windows
        self.eventsClient = EventHandler(self.boardClient, self.viewClient, self.multiplayerClient)
        self.root.mainloop()


    def launchSingleplayerGame(self):
        # board client handles logic of chess board moves and attacks
        self.boardClient = ChessBoard()
        # view client handles drawing everything
        self.viewClient = AppWindow(self.root, self.boardClient)
        self.viewClient.pack()

        self.bindGameEvents()

    ####TODO implement loop with windowmsgbox waiting for connection
    def launchMultiplayerGame(self):
        # connection handler makes chess playable in multiplayer
        self.multiplayerClient = ConnectionHandler()

        # board client handles logic of chess board moves and attacks
        self.boardClient = ChessBoard()
        # view client handles drawing everything
        self.viewClient = AppWindow(self.root, self.boardClient)
        self.viewClient.pack()

        self.bindGameEvents()

    def bindGameEvents(self):
        """bind events to event handler; here go every event handle"""
        self.viewClient.viewBoardClient.addBinding("<Button-1>", self.eventsClient.boardClicked)
        self.viewClient.viewNetworkClient.addBindConnectBtn(self.eventsClient.networkConnect)





############################################################################
###############################DEBUG########################################

if __name__ == "__main__":
    x = SigmaChess()

############################################################################
############################################################################