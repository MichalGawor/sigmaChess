from tkinter import *

class LauncherWindow(Frame):
    """window responsible for letting user pick game mode"""
    def __init__(self,master):
        super().__init__(master)
        #the callback used for connect button
        self.singleplayerCallback=None
        self.multiplayerCallback=None

        self.singplayerButton= Button(self,text="Singleplayer", command=self.addBindSingleplayer)
        self.singplayerButton.pack()

        self.multiplayerButton= Button(self,text="Multiplayer", command=self.addBindMultiplayer)
        self.multiplayerButton.pack()


    def addBindSingleplayer(self, callback):
        self.singleplayerCallback=callback
    def addBindMultiplayer(self,callback):
        self.multiplayerCallback=callback