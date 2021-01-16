# Made by Mayank Sheoran
# BITS PILANI GOA CAMPUS

import random
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox 

   

class GUI_WINDOW:
    tile_color = {
        2: '#e4e8f7',
        4: '#efddb5',
        8: '#fcd368',
        16: '#ffb366',
        32: '#f66',
        64: '#ff4242',
        128: '#fbe18d',
        256: '#f9ce48',
        512: '#ffb2a4',
        1024: '#ff8fbb',
        2048: '#c9ff97',
    }
    def __init__(self,gridOBJ):
        self.grid = gridOBJ
        self.root = tk.Tk()
        self.root.title('2048')
        self.storeLabels = []
        self.frame = Frame(self.root , bg = "#92877d")
        # self.frame.pack()
        for i in range(self.grid.size):
            rowLabels = []
            for j in range(self.grid.size):
                label = Label(self.frame, text='' , bg = '#9e948a' , width = 6  , height = 3, font = ('Times', 34, 'bold'))
                label.grid(row = i , column = j, padx = 10 , pady = 10)
                rowLabels.append(label)
            self.storeLabels.append(rowLabels)
        self.frame.grid()
    def modify_gui(self):
        for row in range(self.grid.size):
            for col in range(self.grid.size):
                if(self.grid.CurrentGrid[row][col]!=0):
                    bgColor = GUI_WINDOW.tile_color[self.grid.CurrentGrid[row][col]]
                    self.storeLabels[row][col].configure(text = str(self.grid.CurrentGrid[row][col]) , bg = bgColor , fg = 'black')
                else:
                    self.storeLabels[row][col].configure(text = '' , bg = '#9e948a')
    
class GAME:
    def __init__(self,gridOBJ,guiOBJ):
        self.grid = gridOBJ
        self.gui = guiOBJ
        self.startingCellsCNT = 2
        self.Highest_Tile = 0
        self.gameOver = False
        self.filled_grid = False
        self.start_game()
        self.valid_move = True

    def keyboard_reader(self,event):
        key_pressed = event.keysym
        before_move_grid = self.grid.CurrentGrid[::]
        move_made = False
        if(key_pressed=='Left' or key_pressed=='a' or key_pressed=='A'):
            self.grid.left_move()
            move_made = True
        if(key_pressed=='Right' or key_pressed=='d' or key_pressed=='D'):
            self.grid.right_move()
            move_made = True
        if(key_pressed=='Up' or key_pressed=='w' or key_pressed=='W'):
            self.grid.up_move()
            move_made = True
        if(key_pressed=='Down' or key_pressed=='s' or key_pressed=='S'):
            self.grid.down_move()
            move_made = True
        else:
            pass
        after_move_grid = self.grid.CurrentGrid[::]
        if(before_move_grid!=after_move_grid and move_made==True):
            self.grid.generate_random_cell()
            self.gui.modify_gui()
        
        currentGrid_copy = self.grid.CurrentGrid[::]
        self.grid.up_move()
        self.grid.right_move()
        self.grid.left_move()
        self.grid.down_move()
        if(self.grid.CurrentGrid == currentGrid_copy):
            self.gameOver = True
        self.grid.CurrentGrid = currentGrid_copy[::]
        self.check_filled_grid()
        if(self.filled_grid==True and self.gameOver==True):
            messagebox.showinfo("Oops!!", "No Moves Left!")
            self.grid.CurrentGrid = self.grid.empty_grid()
            self.Highest_Tile = 0
            self.gameOver = False
            self.start_game()


    def start_game(self):
        for i in range(self.startingCellsCNT):                                                  # Adding Starting CELLS
            self.grid.generate_random_cell()
        self.valid_move = False
        self.set_highest_tile()
        # self.grid.print_grid()
        self.gui.modify_gui()
        self.gui.root.bind('<Key>',self.keyboard_reader)
        self.gui.root.mainloop()

    def check_filled_grid(self):
        self.filled_grid = True
        for row in range(self.grid.size):
            for col in range(self.grid.size):
                if(self.grid.CurrentGrid[row][col]==0):
                    self.filled_grid = False
                    break
    
    def set_highest_tile(self):
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                if(self.grid.CurrentGrid[i][j]!=0):
                    self.Highest_Tile = max(self.Highest_Tile,self.grid.CurrentGrid[i][j])

    def win(self):
        print("Congrats !! You completed the 2048 Game :)")
        return 
        

class GRID:
    def __init__(self,size):
        self.size = size
        self.CurrentGrid = self.empty_grid()
        
    def empty_grid(self):
        return [[0 for i in range(size)] for j in range(self.size)]
    def generate_random_cell(self):
        empty_cells = self.get_empty_cells()
        random_cell = random.choice(empty_cells)
        if(random.random()<0.85):
            self.CurrentGrid[random_cell[0]][random_cell[1]] = 2
        else:
            self.CurrentGrid[random_cell[0]][random_cell[1]] = 4

    def get_empty_cells(self):
        empty_cells=[]
        for i in range(self.size):
            for j in range(self.size):
                if(self.CurrentGrid[i][j]==0):                                                  # Checking Empty Cells
                    empty_cells.append([i,j])
        return empty_cells

    def generate_compressed_grid_up(self,modify_grid):
        newGrid = self.empty_grid()
        for col in range(self.size):
            shiftUP = 0
            for row in range(self.size):
                if(modify_grid[row][col]!=0):
                    newGrid[shiftUP][col] = modify_grid[row][col]
                    shiftUP+=1
        return newGrid
    
    def generate_compressed_grid_down(self,modify_grid):
        newGrid = self.empty_grid()
        for col in range(self.size):
            shiftUP = self.size-1
            for row in range(self.size):
                if(modify_grid[row][col]!=0):
                    newGrid[shiftUP][col] = modify_grid[row][col]
                    shiftUP-=1
        return newGrid

    def generate_compressed_grid_left(self,modify_grid):
        newGrid = self.empty_grid()
        for row in range(self.size):
            shiftUP = 0
            for col in range(self.size):
                if(modify_grid[row][col]!=0):
                    newGrid[row][shiftUP] = modify_grid[row][col]
                    shiftUP+=1
        return newGrid

    def generate_compressed_grid_right(self,modify_grid):
        newGrid = self.empty_grid()
        for row in range(self.size):
            shiftUP = self.size-1
            for col in range(self.size):
                if(modify_grid[row][col]!=0):
                    newGrid[row][shiftUP] = modify_grid[row][col]
                    shiftUP-=1
        return newGrid

    def generate_merge_grid_vertical(self,modify_grid):
        for col in range(self.size):
            for row in range(self.size-1):
                if(modify_grid[row][col]==modify_grid[row+1][col]):
                    modify_grid[row][col]*=2
                    modify_grid[row+1][col] = 0
        return modify_grid
    
    def generate_merge_grid_horizontal(self,modify_grid):
        for row in range(self.size):
            for col in range(self.size-1):
                if(modify_grid[row][col]==modify_grid[row][col+1]):
                    modify_grid[row][col+1]*=2
                    modify_grid[row][col] = 0
        return modify_grid

    def up_move(self):
        newGrid = self.generate_compressed_grid_up(self.CurrentGrid)
        newGrid = self.generate_merge_grid_vertical(newGrid)
        finalGrid = self.generate_compressed_grid_up(newGrid)
        self.CurrentGrid = finalGrid
        
    
    def down_move(self):
        newGrid = self.generate_compressed_grid_down(self.CurrentGrid)
        newGrid = self.generate_merge_grid_vertical(newGrid)
        finalGrid = self.generate_compressed_grid_down(newGrid)
        self.CurrentGrid = finalGrid
        

    def left_move(self):
        newGrid = self.generate_compressed_grid_left(self.CurrentGrid)
        newGrid = self.generate_merge_grid_horizontal(newGrid)
        finalGrid = self.generate_compressed_grid_left(newGrid)
        self.CurrentGrid = finalGrid
        

    def right_move(self):
        newGrid = self.generate_compressed_grid_right(self.CurrentGrid)
        newGrid = self.generate_merge_grid_horizontal(newGrid)
        finalGrid = self.generate_compressed_grid_right(newGrid)
        self.CurrentGrid = finalGrid
        

    def print_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.CurrentGrid[i][j],"  ",end="")
            print("")


if __name__ == '__main__':
    size = 4                                                                                    # Default SIZE 
    grid = GRID(size)
    gui = GUI_WINDOW(grid)
    game = GAME(grid,gui)
    