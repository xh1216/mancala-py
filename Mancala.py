import tkinter as tk


class Mancala(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
##        container.grid_rowconfigure(0, weight=1)
##        container.grid_columnconfigure(0, weight=1)
        self.title("Mancala")
        self.geometry("400x400")
        self.frames = {}
        
        for F in (MenuPage, Board):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class MenuPage(tk.Frame):
    #create MenuPage Frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Button(self, text="Start", command=lambda: controller.show_frame("Board")).pack()

        
class Hole(tk.Button):

    def __init__(self, board, pos, marble):
        self.board = board
        self.pos = pos
        self.marble = marble
        self.btn_text = tk.StringVar()

        tk.Button.__init__(self, board, textvariable=self.btn_text, font=('Helvetica','12'), height=2, width=4, command=lambda:self.board.onClick(self.pos))
        self.btn_text.set(self.marble)

    def updateMarble(self, i):
        self.marble = i
        self.btn_text.set(self.marble)
        self.update()
        self.after(500)


class Board(tk.Frame):

    def __init__(self, parent, controller):
        #create Game Board Frame
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.holeList = [None] * 14

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

            hole.grid(padx=2, pady=2, row=i//7, column=i%7)

    def onClick(self, pos):
        #disable button click
        for button in self.holeList:
            button.config(state=tk.DISABLED)
            
        n = self.holeList[pos].marble   #get current Hole's marble

        #while the Hole is not empty
        while n != 0:
            self.updateBoard(pos)
            
            endPos = pos + n
            startPos = endPos + 1
            
            if startPos >= len(self.holeList):
                startPos = startPos - len(self.holeList)

            pos = startPos
            n = self.holeList[pos].marble
            
        #until a Hole is empty, another player's turn
        tk.Label(self, text="change player").grid(row=4,column=0,columnspan=2)
        for button in self.holeList:
            button.config(state=tk.NORMAL)
        
    def updateBoard(self, pos):
        n = self.holeList[pos].marble
        self.holeList[pos].updateMarble(0)
        startPos = 0
        
        for i in range(1, n + 1):
            
            if pos + i < len(self.holeList):
                j = self.holeList[pos+i].marble
                self.holeList[pos+i].updateMarble(j+1)
                
            else:
                j = self.holeList[startPos].marble
                self.holeList[startPos].updateMarble(j+1)
                startPos += 1


if __name__ == "__main__":
    app = Mancala()
    app.mainloop()
