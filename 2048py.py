from tkinter import *
from tkinter import messagebox
import random

class Board():
    bg_color = {
        '2': '#eee4da', 
        '4': '#ede0c8',
        '8': '#edc850',
        '16': '#edc53f',
        '32': '#f67c5f',
        '64': '#f65e3b',
        '128': '#edcf72',
        '256': '#edcc61',
        '512': '#f2b179',
        '1024': '#f59563',
        '2048': '#edc22e',
    }
    color = {
        '2': '#776e65',
        '4': '#f9f6f2',
        '8': '#f9f6f2',
        '16': '#f9f6f2',
        '32': '#f9f6f2',
        '64': '#f9f6f2',
        '128': '#f9f6f2',
        '256': '#f9f6f2',
        '512': '#776e65',
        '1024': '#f9f6f2',
        '2048': '#f9f6f2',
    }
    
    def __init__(self):
        self.window = Tk()
        self.window.title('2048 GAME')

        # the whole board(not display frame, but internal board) to hold each cell
        # self.gridCell[i][j] values to be paint on the frame with config ltr on 
        self.board = []

        # for the value of each cell (now initialized to 0, but for eg, if self.gridCell[2][2] = 4 means
        # row 2 column 2 = 4)
        self.gridCell = [[0] * 4 for i in range(4)]

        # a container for the game to run in 
        self.gameArea = Frame(self.window, bg='azure3')

        self.compress = False
        self.merge = False
        self.moved = False

        self.score = 0 

        for i in range(4):
            rows = []
            for j in range(4):
                # setting up the frame 
                l = Label(self.gameArea, font=('arial', 20, 'bold'), width=4, height=2)
                # design the grid for the frame, one by one, for i and j loops, (padx / pady are for the borders)
                l.grid(row=i, column=j, padx=7, pady=7)
                # append l 4(j) times into rows for each i loop
                rows.append(l)
            # board will append these rows first, then later paint the numbers from self.gridCell[i][j] onto the frame 
            # with config 
            # append 4 rows into board 
            self.board.append(rows)
        # pasting the grid onto the frame 
        self.gameArea.grid()

    """
    create a newBoard (initialise to 0)
    add elements of gridCell to the newBoard
    in terms of rows, remain the same 
    but if the left most column is empty, newBoard elements will shift to the left
    when newBoard has all the values on the left, assign it back to gridCell 
    in this case it is compressing the board towards the left side 
    """
    def compressGrid(self):
        self.compress = False 
        newBoard = [[0] * 4 for i in range(4)]
        for i in range(4):
            newPos = 0 
            for j in range(4):
                if self.gridCell[i][j] != 0:
                    newBoard[i][newPos] = self.gridCell[i][j]
                    if j != newPos :
                        self.compress = True 
                    newPos +=1
        self.gridCell = newBoard

    """
    reverse the rows of the gridCell 
    row 1 swap with row 4 
    row 2 swap with row 3
    """
    def reverse(self):
        for k in range(4):
            i=0
            j=3
            while(i<j):
                self.gridCell[k][i], self.gridCell[k][j] = self.gridCell[k][j], self.gridCell[k][i]
                i+=1
                j-=1
    
    """
    * unravel the list 
    without the *, you're doing zip( [[1,2,3],[4,5,6]] ). With the *, you're doing zip([1,2,3], [4,5,6]).
    self.gridCell = [[0, 2, 0, 8], [4, 0, 16, 0], [2, 0, 0, 2], [2, 0, 2, 0]] at the sstart 
    with *, doing zip([0, 2, 0, 8], [4, 0, 16, 0], [2, 0, 0, 2], [2, 0, 2, 0])
    zip 
    (0, 4, 2, 2), (2, 0, 0, 0), (0, 16, 0, 2), (8, 0, 2, 0)
    list(t) for t in ^
    [(0, 4, 2, 2)], [(2, 0, 0, 0)], [(0, 16, 0, 2)], [(8, 0, 2, 0)]
    in this case, transpose is changing the values diagonally 
    eg self.gridCell[0][1] and self.gridCell[1][0] will swap place
    """
    def transpose(self):
        self.gridCell=[list(t) for t in zip(*self.gridCell)]

    """
    if cells that are side by side are the same and not 0, can merge them together 
    new cell merged will be an addition of the previous 2 cells, but since
    the previous 2 cells are the same, so x2 

    may not be the same as can_merge() where u need 2 sets 
    one: for i in range(4), for j in range(3)
    two: for i in range(3), for j in range(4)
    cos the second set is unnecessary when ur j+1 already fulfils the last row 
    but for can_merge ure trying to check the availability to merge in all ways, so safer to include a second set 
    """
    def mergeGrid(self):
        self.merge = False 
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j+1] and self.gridCell[i][j] !=0:
                    self.gridCell[i][j] *= 2
                    self.gridCell[i][j+1] = 0 
                    self.score +=self.gridCell[i][j]
                    self.merge=True

    """
    generating a new random cell 
    """
    def random_cell(self):
        cells = []
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] == 0:
                    cells.append((i, j))
        curr = random.choice (cells)

        i = curr[0]
        j = curr[1]
        self.gridCell[i][j] = 2

    """
    paint / update the values and the respective colors onto the grid onto the frame with config
    """
    def paintGrid(self):
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] == 0:
                    # painting the text on the grid 
                    self.board[i][j].config(text='', bg='azure4')
                else: 
                    self.board[i][j].config(text=str(self.gridCell[i][j]), 
                                            bg=self.bg_color.get(str(self.gridCell[i][j])), 
                                            fg=self.color.get(str(self.gridCell[i][j])))
                    
    """
    check if ure able to merge 2 cells together 
    """
    def can_merge(self):
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j+1]:
                    return True
        for i in range(3):
            for j in range(4):
                if self.gridCell[i+1][j] == self.gridCell[i][j]:
                    return True
        return False 
        

class Game():
    def __init__(self, gamepanel):
        self.gamepanel = gamepanel
        self.won = False 
        self.end = False

    # starting scenario for the game 
    # 2 random cells 
    # painted onto the grid 
    # bind the up down left right key to the game 
    # runs the game 
    def start(self) :
        self.gamepanel.random_cell()
        self.gamepanel.random_cell()
        self.gamepanel.paintGrid()
        self.gamepanel.window.bind('<Key>', self.link_keys)
        self.gamepanel.window.mainloop()

    # functions for the shifting of the cells 
    def link_keys(self, event):
        # if game won or ended, return, no more shifting 
        if self.won or self.end:
            return 
        
        self.gamepanel.moved = False 
        self.gamepanel.compress = False
        self.gamepanel.merge =False

        pressed_key = event.keysym

        """
        Left 
        compress them to the left, merge them
        compress again for any empty spaces created from merging 
        """
        """
        Right 
        reverse the rows, compress to the left, merge, compress to the left and reverse the rows back
        if u reverse the rows and shift left and reverse it back it is actually the same as shifting it right 
        """
        """
        Up 
        This move requires the elements to change diagonally first. Then we move them to the left, 
        merge the values, move to the left again to eliminate any empty spaces created from merging, 
        and transpose the values back
        """
        """
        Down 
        transpose(change diagonally), reverse, compress to the left, merge, compress again, reverse, transpose back
        """

        if pressed_key == "Left":
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()

        if pressed_key == "Right":
            self.gamepanel.reverse()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()

        if pressed_key == "Up":
            self.gamepanel.transpose()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.transpose()

        if pressed_key == "Down":
            self.gamepanel.transpose()
            self.gamepanel.reverse()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()
            self.gamepanel.transpose()

        else:
            pass 

        self.gamepanel.paintGrid()
        print(self.gamepanel.score)
        flag = 0 

        for i in range(4):
            for j in range(4):
                if self.gamepanel.gridCell[i][j] == 2048:
                    flag = 1
                    break
                    
        if flag == 1:
            self.won = True 
            messagebox.showinfo('2048', message='won')
            print('won')
        
        if flag==0 and self.gamepanel.can_merge() == False:
            self.end = True 
            messagebox.showinfo('2048', 'gameover')
            print('over')

        if self.gamepanel.moved:
            self.gamepanel.random_cell()

        self.gamepanel.paintGrid()

gamepanel = Board()
Game2048 = Game(gamepanel)
Game2048.start()
                    
                    
        
