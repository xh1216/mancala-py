import tkinter as tk


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
        self.show_frame("MenuPage")

    def show_frame(self, page_name):
        getattr(Mancala, page_name).tkraise()


class Player:

    def __init__(self, name):
        self.name = name
        self.score = 0

    def setScore(self, score):
        self.score = score

        
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
        tk.Label(self, text="Number of holes\n(4-20, EVEN number):", font=('Helvetica','12'), justify=tk.LEFT).place(x=130, y=220)
        tk.Entry(self, font=('Helvetica','12'), textvariable=self.holeNum).place(x=300, y=239, width=30)
        tk.Label(self, text="Number of seeds(4-10):", font=('Helvetica','12')).place(x=130, y=280)
        tk.Entry(self, font=('Helvetica','12'), textvariable=self.seedNum).place(x=300, y=281, width=30)
        tk.Button(self, text="Start Game", font=('Helvetica','16'), command=self.startClicked).place(x=175, y=350)
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
        elif self.holeNum.get() < 4 or self.holeNum.get() > 20 or self.holeNum.get()%2 != 0:
            self.msg.config(text="Enter even number 4-20")
            self.msg.place(x=338, y=239)
        elif self.seedNum.get() < 4 or self.seedNum.get() > 10:
            self.msg.config(text="Enter number 4-10")
            self.msg.place(x=338, y=281)
        else:
            frame = Board(self.parent, self.controller)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()


class Hole(tk.Button):

    def __init__(self, board, pos, seed):
        self.board = board
        self.pos = pos
        self.seed = seed
        self.btn_text = tk.StringVar()

        tk.Button.__init__(self, board, textvariable=self.btn_text, font=('Helvetica','12'), height=2, width=4, command=lambda:self.board.onClick(self.pos))
        self.btn_text.set(self.seed)

    def setSeed(self, i):
        self.seed = i
        self.btn_text.set(self.seed)
        self.update()
        self.after(800)

        
class Board(tk.Frame):

    def __init__(self, parent, controller):
        #create Game Board Frame
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.holeNum = Mancala.MenuPage.holeNum.get()
        self.seedNum = Mancala.MenuPage.seedNum.get()
        self.holeList = [None] * self.holeNum
        tk.Label(self, text="Player:", font=('Helvetica','12')).grid(row=0, column=0)
        tk.Label(self, textvariable=Mancala.MenuPage.playerName, font=('Helvetica','12')).grid(row=0, column=1, columnspan=10, sticky=tk.W)
        tk.Label(self, text="Score:", font=('Helvetica','12')).grid(row=1, column=0)
        tk.Label(self, text="Player:", font=('Helvetica','12')).grid(row=5, column=self.holeNum//2)
        tk.Label(self, text="Score:", font=('Helvetica','12')).grid(row=6, column=self.holeNum//2)

        #create Hole Button
        j = (self.holeNum // 2) - 1
        for i in range(self.holeNum):
            if i < self.holeNum // 2:
                hole = Hole(self, i+j, self.seedNum)
                self.holeList[i+j] = hole
                j -= 2
            else:
                hole = Hole(self, i, self.seedNum)
                self.holeList[i] = hole
            hole.grid(padx=5, pady=5, row=(i//(self.holeNum//2)) + 3, column=(i%(self.holeNum//2)) + 1)

    def onClick(self, pos):
        for button in self.holeList:
            button.config(state=tk.DISABLED)
            
        n = self.holeList[pos].seed   #get current Hole's marble

        #while the Hole is not empty, distribute seed
        while n != 0:
            endPos = self.updateBoard(pos)
            pos = (endPos + 1) % len(self.holeList)
            n = self.holeList[pos].seed
            
        #until a Hole is empty, another player's turn
        tk.Label(self, text="Player ? 's turn!", font=('Helvetica','12')).grid(row=8,column=3,columnspan=3)
        for button in self.holeList:
            button.config(state=tk.NORMAL)
        
    def updateBoard(self, pos):
        n = self.holeList[pos].seed
        self.holeList[pos].setSeed(0)
        
        for i in range(1, n + 1):
            j = (pos + i) % len(self.holeList)
            s = self.holeList[j].seed
            self.holeList[j].setSeed(s+1)
        return j


if __name__ == "__main__":
    app = Mancala()
    app.mainloop()
