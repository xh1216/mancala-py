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
        self.player1_name = tk.StringVar()
        self.player2_name = tk.StringVar()
        self.vs_radio_button = tk.IntVar()
        self.hole_num = tk.IntVar()
        self.seed_num = tk.IntVar()
        
        tk.Label(self, text="Mancala", font=('Helvetica','18')).place(x=190, y=30)
        tk.Label(self, text="Player Name:", font=('Helvetica','12')).place(x=130, y=100)
        tk.Entry(self, font=('Helvetica','12'), textvariable=self.player1_name).place(x=240, y=102, width=100)
        tk.Label(self, text="VS:", font=('Helvetica','12')).place(x=95, y=165)
        tk.Radiobutton(self, text="Computer", variable=self.vs_radio_button, value=0, font=('Helvetica','12'), command=lambda:self.vs_entry.config(state=tk.DISABLED)).place(x=135, y=150)
        tk.Radiobutton(self, text="Player Name:", variable=self.vs_radio_button, value=1, font=('Helvetica','12'), command=lambda:self.vs_entry.config(state=tk.NORMAL)).place(x=135, y=175)
        self.vs_entry = tk.Entry(self, font=('Helvetica','12'), textvariable=self.player2_name, state=tk.DISABLED)
        self.vs_entry.place(x=265, y=177, width=100)
        tk.Label(self, text="Number of holes\n(4-8 per row):", font=('Helvetica','12'), justify=tk.RIGHT).place(x=130, y=220)
        tk.Entry(self, font=('Helvetica','12'), textvariable=self.hole_num).place(x=260, y=239, width=30)
        tk.Label(self, text="Number of seeds\n(4-10 per hole):", font=('Helvetica','12'), justify=tk.RIGHT).place(x=130, y=280)
        tk.Entry(self, font=('Helvetica','12'), textvariable=self.seed_num).place(x=260, y=299, width=30)
        tk.Button(self, text="Start Game", font=('Helvetica','16'), command=self.start_clicked).place(x=175, y=360)
        self.msg = tk.Label(self, font=('Helvetica','10'), fg="red")
        self.msg.place(x=345, y=101)
            
    def start_clicked(self):
        
        self.msg.config(text="")
        if not self.player1_name.get():
            self.msg.config(text="Enter player name")
        elif self.vs_radio_button.get() == 1 and not self.player2_name.get():
            self.msg.config(text="Enter player name")
            self.msg.place(x=370, y=177)
        elif self.player1_name.get() == self.player2_name.get():
            self.msg.config(text="Enter different name")
            self.msg.place(x=370, y=177)
        elif self.hole_num.get() < 4 or self.hole_num.get() > 8:
            self.msg.config(text="Enter number 4-8")
            self.msg.place(x=302, y=239)
        elif self.seed_num.get() < 4 or self.seed_num.get() > 10:
            self.msg.config(text="Enter number 4-10")
            self.msg.place(x=302, y=299)
        else:
            frame = Board(self.parent, self.controller)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()


class Player:

    def __init__(self, name, is_bot, is_turn, side_of_board):
        
        self.name = name
        self.opponent = None
        self.side_of_board = side_of_board
        self.is_bot = is_bot
        self.is_turn = is_turn
        self.holes = [None] * (Mancala.MenuPage.hole_num.get())
        self.score = tk.IntVar()

    def move(self, hole_list, row, col):
        
        s = hole_list[row][col].seed    #get current Hole's seed
        
        while s != 0:           #while the Hole is not empty, distribute seed; stop when Hole is empty
            hole_list[row][col].set_seed(0)
            for i in range(s):
                col = col - 1 if row == 0 else col + 1
                row, col = self.is_out_of_range(row, col)
                hole_list[row][col].set_seed(hole_list[row][col].seed + 1)
            col = col - 1 if row == 0 else col + 1
            row, col = self.is_out_of_range(row, col)
            s = hole_list[row][col].seed

        col = col - 1 if row == 0 else col + 1      #capture next hole's seed to own store
        row, col = self.is_out_of_range(row, col)
        next_hole = hole_list[row][col]
        self.score.set(self.score.get() + next_hole.seed)
        next_hole.set_seed(0)

    def AI_move(self, board):
        
        copy_board = copy.copy(board)
        minimax_hole_list = [[None] * Mancala.MenuPage.hole_num.get()] + [[None] * Mancala.MenuPage.hole_num.get()]

        for i in range(len(board.hole_list)):
            for j in range(len(board.hole_list[i])):
                minimax_hole_list[i][j] = board.hole_list[i][j].seed
        copy_board.hole_list = minimax_hole_list
        new_board = MinimaxBoard(copy_board, self.score.get(), self.opponent.score.get(), True)
        col = new_board.find_best_move()
        self.holes[col].invoke()

    def is_out_of_range(self, row, col):
        
        if row == 0 and col < 0:
            row, col = 1, 0
        if row == 1 and col > Mancala.MenuPage.hole_num.get() - 1:
            row, col = 0, Mancala.MenuPage.hole_num.get() - 1
        return row, col     


class Hole(tk.Button):

    def __init__(self, board, row, col, seed):
        
        self.board = board
        self.row = row
        self.col = col
        self.seed = seed
        self.seed_text = tk.StringVar()
        tk.Button.__init__(self, board, textvariable=self.seed_text, font=('Helvetica','12'), height=2, width=4, command=lambda:self.board.hole_clicked(self.row, self.col))
        self.seed_text.set(self.seed)

    def set_seed(self, i):
        
        self.seed = i
        self.seed_text.set(self.seed)
        self.update()
        self.after(100)


class Board(tk.Frame):
    
    #create Game Board Frame
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.hole_num = Mancala.MenuPage.hole_num.get()
        self.seed_num = Mancala.MenuPage.seed_num.get()
        self.player1 = Player(Mancala.MenuPage.player1_name, False, True, 0)
        self.AI_name = tk.StringVar()
        self.AI_name.set("AI Bot")
        self.player2 = Player(self.AI_name, True, False, 1) if Mancala.MenuPage.vs_radio_button.get() == 0 else Player(Mancala.MenuPage.player2_name, False, False, 1)
        self.player1.opponent = self.player2
        self.player2.opponent = self.player1
        self.player_list = [self.player1, self.player2]
        self.hole_list = [[None] * self.hole_num] + [[None] * self.hole_num]

        tk.Label(self, text="Player:", font=('Helvetica','12')).grid(row=0, column=0)
        tk.Label(self, textvariable=self.player1.name, font=('Helvetica','12')).grid(row=0, column=1, columnspan=10, sticky=tk.W)
        tk.Label(self, text="Score:", font=('Helvetica','12')).grid(row=1, column=0)
        tk.Label(self, textvariable=self.player1.score, font=('Helvetica','12')).grid(row=1, column=1, columnspan=5, sticky=tk.W)
        tk.Label(self, text="Player:", font=('Helvetica','12')).grid(row=5, column=0)
        tk.Label(self, textvariable=self.player2.name, font=('Helvetica','12')).grid(row=5, column=1, sticky=tk.W)
        tk.Label(self, text="Score:", font=('Helvetica','12')).grid(row=6, column=0)
        tk.Label(self, textvariable=self.player2.score, font=('Helvetica','12')).grid(row=6, column=1, sticky=tk.W)
        self.msg = tk.Label(self, text=self.player1.name.get() + "'s Turn.", font=('Helvetica','12'), fg="blue")
        self.msg.grid(row=10, column=0, columnspan=15, sticky=tk.W)
        self.msg2 = tk.Label(self, font=('Helvetica','12'), fg="blue")
        self.msg2.grid(row=11, column=0, columnspan=15, sticky=tk.W)

        #create Hole Button
        for i in range(len(self.player_list)):
            for j in range(self.hole_num):
                hole = Hole(self, i, j, self.seed_num)
                self.hole_list[i][j] = hole
                if i == 0:
                    self.player1.holes[j] = hole
                else:
                    self.player2.holes[j] = hole
                hole.grid(padx=5, pady=5, row=i+3, column=j)
        
        for player in self.player_list:
            if not player.is_turn:
                for hole in player.holes:
                    hole.config(state=tk.DISABLED)

        self.is_bot_turn()
        
    def hole_clicked(self, row, col):
        
        for holes in self.hole_list:
            for hole in holes:
                hole.config(state=tk.DISABLED)  #once a Hole is clicked, disable all button click

        for player in self.player_list:
            if player.is_turn:
                self.msg.config(text=player.name.get() + "'s Turn.")
                if player.is_bot:
                    self.update()
                    self.after(800)
                    self.msg2.config(text="Bot pick Hole col " + str(col+1))
                    print("Bot pick Hole col " + str(col+1))
                player.move(self.hole_list, row, col)

        self.take_turn()

        if not self.is_end_game():
            self.is_bot_turn()
        else:
            self.winner = self.player1 if self.player1.score.get() > self.player2.score.get() else self.player2         #draw
            self.update()
            self.after(800)
            self.msg2.config(text="Player " + self.winner.name.get() + " has more seeds! WIN!!")

    def take_turn(self):
        
        #self.player_list.sort(key=lambda player: player.is_turn, reverse=True)    #sort player's index to the first if it is the player's turn 
        for player in self.player_list:
            if player.is_turn:
                player.is_turn = False
            else:
                player.is_turn = True
                for hole in player.holes:
                    if hole.seed != 0:
                        hole.config(state=tk.NORMAL)
                self.msg.config(text=player.name.get() + "'s Turn!")
                self.msg2.config(text="")

    def is_bot_turn(self):    #check if it is Bot's turn
        
        for player in self.player_list:
            if player.is_turn and player.is_bot:
                player.AI_move(self)

    def is_end_game(self):    #check if the game is ended

        for player in self.player_list:
            if player.is_turn:
                for hole in player.holes:
                    if hole.seed != 0:
                        return False
                self.update()
                self.after(800)
                self.msg.config(text=player.name.get() + "'s Turn. The holes of " + player.name.get() + "'s side are empty. -End Game-")
        return True


class MinimaxBoard:

    def __init__(self, board, AI_seed, opponent_seed, is_bot_turn):
        
        self.hole_list = list(list(x) for x in board.hole_list)
        self.AI_seed = AI_seed
        self.opponent_seed = opponent_seed
        self.is_bot_turn = is_bot_turn

    def find_best_move(self):
        
        best_val = -1000
        best_col = -1
        move_val = 0
        row = 1
        for col in range(len(self.hole_list[row])):
            if self.hole_list[row][col] != 0:                                    # correct
                new_board = MinimaxBoard(self, self.AI_seed, self.opponent_seed, self.is_bot_turn)
                new_board.bot_move(row, col)
                move_val = self.minimax(new_board, 0, new_board.is_bot_turn)
                if move_val > best_val:
                    best_val = move_val
                    best_col = col
##                print("best val ", best_val)
##        print("pick col ", best_col)
        return best_col

    def bot_move(self, row, col):
        
        seed = self.hole_list[row][col]
        while seed != 0:
            self.hole_list[row][col] = 0
            for i in range(seed):
                col = col - 1 if row == 0 else col + 1
                row, col = self.is_out_of_range(row, col)
                self.hole_list[row][col] += 1
            col = col - 1 if row == 0 else col + 1
            row, col = self.is_out_of_range(row, col)
            seed = self.hole_list[row][col]

        col = col - 1 if row == 0 else col + 1
        row, col = self.is_out_of_range(row, col)
        next_hole_seed = self.hole_list[row][col]
        self.hole_list[row][col] = 0
        
        if self.is_bot_turn:
            self.AI_seed += next_hole_seed
        else:
            self.opponent_seed += next_hole_seed
            
        self.is_bot_turn = not self.is_bot_turn
                                                                        #correct, seed is increasing 
    def is_out_of_range(self, row, col):
        
        if row == 0 and col < 0:
            row, col = 1, 0
        if row == 1 and col > len(self.hole_list[row]) - 1:
            row, col = 0, len(self.hole_list[row]) - 1
        return row, col

    def evaluate(self):
        
        return self.AI_seed - self.opponent_seed

    #buggg
    def is_end_game(self):
        
        row = 1 if self.is_bot_turn else 0
        for hole in self.hole_list[row]:
                if hole != 0:
                    return False
        return True

    def minimax(self, board, depth, is_max):
        
        if board.is_end_game() or depth == 5:
            minimax_score = board.evaluate()
            return minimax_score

        if is_max:
            best = -1000
            for col in range(len(board.hole_list[1])):
                if board.hole_list[1][col] != 0:
                    new_board = MinimaxBoard(board, board.AI_seed, board.opponent_seed, board.is_bot_turn)
                    new_board.bot_move(1, col)
                    
##                    print("MAX    ", new_board.hole_list)
                    
                    a = board.minimax(new_board, depth+1, False)
                    best = max(best, a)
##                    print("MAX RETURN      ", a)
##            print("MAX BEST RETURN     ", best)
            return best
        else:
            best = 1000
            for col in range(len(board.hole_list[0])):
                if board.hole_list[0][col] != 0:
                    new_board = MinimaxBoard(board, board.AI_seed, board.opponent_seed, board.is_bot_turn)
                    new_board.bot_move(0, col)
                    
##                    print("MIN     ", new_board.hole_list)
                    
                    r = board.minimax(new_board, depth+1, True)
                    best = min(best, r)
##                    print("MIN RETURN      ", r)

                    
##            print("MIN BEST RETURN     ", best)
            return best

        
if __name__ == "__main__":
    app = Mancala()
    app.mainloop()
