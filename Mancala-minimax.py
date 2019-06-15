import tkinter as tk
import copy


class Mancala(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.title("Mancala")
        self.geometry("500x500")
        setattr(Mancala, MenuPage.__name__, MenuPage(container, self))
        getattr(Mancala, MenuPage.__name__).grid(row=0, column=0, sticky="nsew")
        getattr(Mancala, MenuPage.__name__).tkraise()

        
class MenuPage(tk.Frame):
    #create MenuPage Frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.playerName = tk.StringVar()
        self.opponentName = tk.StringVar()
        self.vsRadioButton = tk.IntVar()
        self.holeNum = tk.IntVar()
        self.seedNum = tk.IntVar()
        
        tk.Label(self, text="Mancala", font=('Helvetica','18')).place(x=190, y=30)
        tk.Label(self, text="Player Name:", font=('Helvetica','12')).place(x=130, y=100)
        tk.Entry(self, font=('Helvetica','12'), textvariable=self.playerName).place(x=240, y=102, width=100)
        tk.Label(self, text="VS:", font=('Helvetica','12')).place(x=95, y=165)
        tk.Radiobutton(self, text="Computer", variable=self.vsRadioButton, value=0, font=('Helvetica','12'), command=lambda:self.vsEntry.config(state=tk.DISABLED)).place(x=135, y=150)
        tk.Radiobutton(self, text="Player Name:", variable=self.vsRadioButton, value=1, font=('Helvetica','12'), command=lambda:self.vsEntry.config(state=tk.NORMAL)).place(x=135, y=175)
        self.vsEntry = tk.Entry(self, font=('Helvetica','12'), textvariable=self.opponentName, state=tk.DISABLED)
        self.vsEntry.place(x=265, y=177, width=100)
        tk.Label(self, text="Number of holes\n(4-8 per row):", font=('Helvetica','12'), justify=tk.RIGHT).place(x=130, y=220)
        tk.Entry(self, font=('Helvetica','12'), textvariable=self.holeNum).place(x=260, y=239, width=30)
        tk.Label(self, text="Number of seeds\n(4-10 per hole):", font=('Helvetica','12'), justify=tk.RIGHT).place(x=130, y=280)
        tk.Entry(self, font=('Helvetica','12'), textvariable=self.seedNum).place(x=260, y=299, width=30)
        tk.Button(self, text="Start Game", font=('Helvetica','16'), command=self.startClicked).place(x=175, y=360)
        self.msg = tk.Label(self, font=('Helvetica','10'), fg="red")
        self.msg.place(x=345, y=101)
            
    def startClicked(self):
        self.msg.config(text="")
        if not self.playerName.get():
            self.msg.config(text="Enter player name")
        elif self.vsRadioButton.get() == 1 and not self.opponentName.get():
            self.msg.config(text="Enter player name")
            self.msg.place(x=370, y=177)
        elif self.playerName.get() == self.opponentName.get():
            self.msg.config(text="Enter different name")
            self.msg.place(x=370, y=177)
        elif self.holeNum.get() < 4 or self.holeNum.get() > 8:
            self.msg.config(text="Enter number 4-8")
            self.msg.place(x=302, y=239)
        elif self.seedNum.get() < 4 or self.seedNum.get() > 10:
            self.msg.config(text="Enter number 4-10")
            self.msg.place(x=302, y=299)
        else:
            frame = Board(self.parent, self.controller)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()


class Player:

    def __init__(self, name, isBot, isTurn):
        self.name = name
        self.isBot = isBot
        self.isTurn = isTurn
        self.holes = [None] * (Mancala.MenuPage.holeNum.get())
        self.score = tk.IntVar()

        
class Hole(tk.Button):

    def __init__(self, board, row, col, seed):
        self.board = board
        self.row = row
        self.col = col
        self.seed = seed
        self.btnText = tk.StringVar()
        tk.Button.__init__(self, board, textvariable=self.btnText, font=('Helvetica','12'), height=2, width=4, command=lambda:self.board.holeClicked(self.row, self.col))
        self.btnText.set(self.seed)

    def setSeed(self, i):
        self.seed = i
        self.btnText.set(self.seed)
        self.update()
        self.after(500)


class MinimaxBoard:

    def __init__(self, holeList, playerSeed, botSeed):
        self.holeList = holeList
        self.playerSeed = playerSeed
        self.botSeed = botSeed
        self.initialHoleList = holeList.copy()
        self.initialPlayerSeed = playerSeed
        self.initialBotSeed = botSeed
        self.isBotTurn = True

    def findBestMove(self):
        bestVal = -1000
        bestCol = -1
        moveVal = 0
        row = 1
        for col in range(len(self.holeList[row])):
            print(self.holeList[row][col])
            if self.holeList[row][col] != 0:                                    # correct
                self.distributeSeed(row, col)                                   # i guess correct
                moveVal = self.minimax(self, self.isBotTurn)
                self.holeList = self.initialHoleList.copy()
                self.playerSeed = self.initialPlayerSeed
                self.botSeed = self.initialBotSeed
                print(moveVal)
                if moveVal > bestVal:
                    bestVal = moveVal
                    bestCol = col
        print(bestCol)
        return bestCol

    def distributeSeed(self, row, col):     #stop when hole is empty
        seed = self.holeList[row][col]
        while seed != 0:
            self.holeList[row][col] = 0
            for i in range(seed):
                col = col - 1 if row == 0 else col + 1
                row, col = self.checkOutOfRange(row, col)
                self.holeList[row][col] += 1
            col = col - 1 if row == 0 else col + 1
            row, col = self.checkOutOfRange(row, col)
            seed = self.holeList[row][col]
        #print(self.holeList)                                                   #hole list wrong
        #hole is empty, assign next hole's seed to player
        col = col - 1 if row == 0 else col + 1
        row, col = self.checkOutOfRange(row, col)
        nextHoleSeed = self.holeList[row][col]
        self.holeList[row][col] = 0
        
        if self.isBotTurn:
            self.botSeed += nextHoleSeed
        else:
            self.playerSeed += nextHoleSeed
        self.isBotTurn = not self.isBotTurn
                                                                        #correct, seed is increasing 

    def checkOutOfRange(self, row, col):
        if row == 0 and col < 0:
            row, col = 1, 0
        if row == 1 and col > len(self.holeList[row]) - 1:
            row, col = 0, len(self.holeList[row]) - 1
        return row, col

    def evaluate(self, board):
        if self.isEndGame(board):
            if self.botSeed > self.playerSeed:
                return 20
            else:
                return -20
        return 0

    def isEndGame(self, board):
        row = 1 if self.isBotTurn else 0
        for hole in board.holeList[row]:
            if hole != 0:
                return False
        return True

    def minimax(self, board, isMax):
        iniBoard = copy.copy(board)

        minimaxScore = self.evaluate(board)         ##buggg, tie

        if minimaxScore == 20 or minimaxScore == -20:
            return minimaxScore

        if isMax:
            best = -1000
            for col in range(len(board.holeList[1])):
                if board.holeList[1][col] != 0:
                    board.distributeSeed(1, col)
                    best = max(best, self.minimax(board, False))
                    board = copy.copy(iniBoard)
            return best
        else:
            best = 1000
            for col in range(len(board.holeList[0])):
                if board.holeList[0][col] != 0:
                    board.distributeSeed(0, col)
                    best = min(best, self.minimax(board, True))
                    board = copy.copy(iniBoard)
            return best
        
    
class Board(tk.Frame):
    #create Game Board Frame
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.holeNum = Mancala.MenuPage.holeNum.get()
        self.seedNum = Mancala.MenuPage.seedNum.get()
        self.player = Player(Mancala.MenuPage.playerName, False, True)
        self.botName = tk.StringVar()
        self.botName.set("Bot")
        self.opponent = Player(self.botName, True, False) if Mancala.MenuPage.vsRadioButton.get() == 0 else Player(Mancala.MenuPage.opponentName, False, False)
        self.playerList = [self.player, self.opponent]
        self.holeList = [[None] * self.holeNum] + [[None] * self.holeNum]

        tk.Label(self, text="Player:", font=('Helvetica','12')).grid(row=0, column=0)
        tk.Label(self, textvariable=self.player.name, font=('Helvetica','12')).grid(row=0, column=1, columnspan=10, sticky=tk.W)
        tk.Label(self, text="Score:", font=('Helvetica','12')).grid(row=1, column=0)
        tk.Label(self, textvariable=self.player.score, font=('Helvetica','12')).grid(row=1, column=1, columnspan=5, sticky=tk.W)
        tk.Label(self, text="Player:", font=('Helvetica','12')).grid(row=5, column=0)
        tk.Label(self, textvariable=self.opponent.name, font=('Helvetica','12')).grid(row=5, column=1, sticky=tk.W)
        tk.Label(self, text="Score:", font=('Helvetica','12')).grid(row=6, column=0)
        tk.Label(self, textvariable=self.opponent.score, font=('Helvetica','12')).grid(row=6, column=1, sticky=tk.W)
        self.msg = tk.Label(self, text=self.player.name.get() + "'s Turn.", font=('Helvetica','12'), fg="blue")
        self.msg.grid(row=10, column=0, columnspan=15, sticky=tk.W)
        self.msg2 = tk.Label(self, font=('Helvetica','12'), fg="blue")
        self.msg2.grid(row=11, column=0, columnspan=15, sticky=tk.W)

        #create Hole Button
        for i in range(len(self.playerList)):
            for j in range(self.holeNum):
                hole = Hole(self, i, j, self.seedNum)
                self.holeList[i][j] = hole
                if i == 0:
                    self.player.holes[j] = hole
                else:
                    self.opponent.holes[j] = hole
                hole.grid(padx=5, pady=5, row=i+3, column=j)
        
        for player in self.playerList:
            if not player.isTurn:
                for hole in player.holes:
                    hole.config(state=tk.DISABLED)
        
    def holeClicked(self, row, col):
        for holes in self.holeList:
            for hole in holes:
                hole.config(state=tk.DISABLED)  #once a Hole clicked, disable all button click

        for player in self.playerList:
            if player.isTurn:
                self.msg.config(text=player.name.get() + "'s Turn.")
                if player.isBot:
                    self.update()
                    self.after(800)
                    self.msg2.config(text="Bot pick Hole col " + str(col+1))

        self.startBoard(row, col)

    def distributeSeed(self, row, col):
        s = self.holeList[row][col].seed     #get current Hole's seed
        while s != 0:       #while the Hole is not empty, distribute seed; stop when Hole is empty
            row, col = self.updateBoard(row, col)
            col = col - 1 if row == 0 else col + 1
            row, col = self.checkOutOfRange(row, col)
            s = self.holeList[row][col].seed

        return row, col
    
    def updateBoard(self, row, col):
        s = self.holeList[row][col].seed
        self.holeList[row][col].setSeed(0)
        for i in range(s):
            col = col - 1 if row == 0 else col + 1
            row, col = self.checkOutOfRange(row, col)
            self.holeList[row][col].setSeed(self.holeList[row][col].seed + 1)
            
        return row, col

    def takeTurn(self, row, col):
        self.playerList.sort(key=lambda player: player.isTurn, reverse=True)    #sort player's index to the first if it is the player's turn 
        for player in self.playerList:
            if player.isTurn:
                col = col - 1 if row == 0 else col + 1
                row, col = self.checkOutOfRange(row, col)
                nextHole = self.holeList[row][col]
                player.score.set(player.score.get() + nextHole.seed)
                nextHole.setSeed(0)
                player.isTurn = False
            else:
                player.isTurn = True
                for hole in player.holes:
                    if hole.seed != 0:
                        hole.config(state=tk.NORMAL)
                self.msg.config(text=player.name.get() + "'s Turn!")
                self.msg2.config(text="")

    def isEndGame(self):    #check if the game is ended
        for player in self.playerList:
            if player.isTurn:
                for hole in player.holes:
                    if hole.seed != 0:
                        return False
                self.update()
                self.after(800)
                self.msg.config(text=player.name.get() + "'s Turn. The holes of " + player.name.get() + "'s side are empty. -End Game-")
        return True

    def isBotTurn(self):    #check if it is Bot's turn
        for player in self.playerList:
            if player.isTurn and player.isBot:
                col = self.botMove()
                player.holes[col].invoke()
##                for hole in player.holes:
##                    if hole['state'] == 'normal':
##                        hole.invoke()

    def botMove(self):
        minimaxHoleList = [[None] * self.holeNum] + [[None] * self.holeNum]
        for i in range(len(self.playerList)):
            for j in range(self.holeNum):
                seed = self.holeList[i][j].seed
                minimaxHoleList[i][j] = seed
                
        newBoard = MinimaxBoard(minimaxHoleList, self.player.score.get(), self.opponent.score.get())
        return newBoard.findBestMove()
                

    def checkOutOfRange(self, row, col):
        if row == 0 and col < 0:
            row, col = 1, 0
        if row == 1 and col > self.holeNum - 1:
            row, col = 0, self.holeNum - 1
        return row, col
        
    def startBoard(self, row, col):
        
        row, col = self.distributeSeed(row, col)

        self.takeTurn(row, col)
        
        if self.isEndGame():
            self.winner = self.player if self.player.score.get() > self.opponent.score.get() else self.opponent
            self.update()
            self.after(800)
            self.msg2.config(text="Player " + self.winner.name.get() + " has more seeds! WIN!!")
        else:
            self.isBotTurn()
            
        
if __name__ == "__main__":
    app = Mancala()
    app.mainloop()