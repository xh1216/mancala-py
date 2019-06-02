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
        self.frames = {}
        
        for F in (MenuPage, Board):
            setattr(Mancala, F.__name__, F(parent=container, controller=self))
            getattr(Mancala, F.__name__).grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuPage")

    def show_frame(self, page_name):
        frame = getattr(Mancala, page_name)
        frame.tkraise()


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
        self.controller = controller
        self.playerName = tk.StringVar()
        self.opponentName = tk.StringVar()
        self.vsRadioButton = tk.IntVar()
        
        tk.Label(self, text="Mancala", font=('Helvetica','18')).place(x=190, y=30)
        tk.Label(self, text="Player Name:", font=('Helvetica','12')).place(x=130, y=100)
        tk.Entry(self, font=('Helvetica','12'), textvariable=self.playerName).place(x=240, y=102, width=100)
        tk.Label(self, text="VS:", font=('Helvetica','12')).place(x=95, y=165)
        tk.Radiobutton(self, text="Computer", variable=self.vsRadioButton, value=0, font=('Helvetica','12'), command=self.radioButtonPicked).place(x=135, y=150)
        tk.Radiobutton(self, text="Player Name:", variable=self.vsRadioButton, value=1, font=('Helvetica','12'), command=self.radioButtonPicked).place(x=135, y=175)
        self.vsEntry = tk.Entry(self, font=('Helvetica','12'), textvariable=self.opponentName, state=tk.DISABLED)
        self.vsEntry.place(x=265, y=177, width=100)
        tk.Label(self, text="Number of holes:", font=('Helvetica','12')).place(x=130, y=220)
        tk.Entry(self, font=('Helvetica','12')).place(x=260, y=222, width=30)
        tk.Label(self, text="Number of seeds:", font=('Helvetica','12')).place(x=130, y=260)
        tk.Entry(self, font=('Helvetica','12')).place(x=260, y=262, width=30)
        tk.Button(self, text="Start Game", font=('Helvetica','16'), command=self.startClicked).place(x=175, y=340)
        self.msg1 = tk.Label(self, font=('Helvetica','10'), fg="red")
        self.msg1.place(x=345, y=100)
        self.msg2 = tk.Label(self, font=('Helvetica','10'), fg="red")
        self.msg2.place(x=370, y=177)

    def radioButtonPicked(self):
        if self.vsRadioButton.get() == 0:
            self.vsEntry.config(state=tk.DISABLED)
        else:
            self.vsEntry.config(state=tk.NORMAL)
            
    def startClicked(self):
        self.msg1.config(text="")
        self.msg2.config(text="")
        if not self.playerName.get():
            self.msg1.config(text="Enter player name")
        elif self.vsRadioButton.get() == 1 and not self.opponentName.get():
            self.msg2.config(text="Enter player name")
        elif self.playerName.get() == self.opponentName.get():
            self.msg2.config(text="Enter different name")
        else:
            self.controller.show_frame("Board")


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
        self.after(500)


class Board(tk.Frame):

    def __init__(self, parent, controller):
        #create Game Board Frame
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.holeList = [None] * 14
        tk.Label(self, text="Player:", font=('Helvetica','12')).grid(row=0, column=0)
        tk.Label(self, textvariable=Mancala.MenuPage.playerName, font=('Helvetica','12')).grid(row=0, column=1, columnspan=10, sticky=tk.W)
        tk.Label(self, text="Score:", font=('Helvetica','12')).grid(row=1, column=0)
        #create Hole Button
        j = 6
        for i in range(14):
            if i < 7:
                hole = Hole(self, i+j, 4)
                self.holeList[i+j] = hole
                j -= 2

            else:
                hole = Hole(self, i, 4)
                self.holeList[i] = hole
            hole.grid(padx=5, pady=5, row=(i//7) + 3, column=(i%7) + 1)
        tk.Label(self, text="Player:", font=('Helvetica','12')).grid(row=5, column=7)
        tk.Label(self, text="Score:", font=('Helvetica','12')).grid(row=6, column=7)
        
    def onClick(self, pos):
        #once a Hole button is clicked, disable button click
        for button in self.holeList:
            button.config(state=tk.DISABLED)
            
        n = self.holeList[pos].seed   #get current Hole's marble

        #while the Hole is not empty, distribute seed
        while n != 0:
            self.updateBoard(pos)
            
            endPos = pos + n
            startPos = endPos + 1
            
            if startPos >= len(self.holeList):
                startPos = startPos - len(self.holeList)

            pos = startPos
            n = self.holeList[pos].seed
            
        #until a Hole is empty, another player's turn
        tk.Label(self, text="Player ? 's turn!", font=('Helvetica','12')).grid(row=8,column=3,columnspan=3)
        for button in self.holeList:
            button.config(state=tk.NORMAL)
        
    def updateBoard(self, pos):
        n = self.holeList[pos].seed
        self.holeList[pos].setSeed(0)
        startPos = 0
        
        for i in range(1, n + 1):
            
            if pos + i < len(self.holeList):
                j = self.holeList[pos+i].seed
                self.holeList[pos+i].setSeed(j+1)
                
            else:
                j = self.holeList[startPos].seed
                self.holeList[startPos].setSeed(j+1)
                startPos += 1


if __name__ == "__main__":
    app = Mancala()
    app.mainloop()
