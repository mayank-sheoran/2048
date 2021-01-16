# Made by Mayank Sheoran
# BITS PILANI GOA CAMPUS

import random
import sys 
sys.setrecursionlimit(10**6)
from collections import defaultdict
# import tkinter as tk
# from tkinter import *
# from tkinter import ttk
# from tkinter import messagebox 

   

# class GUI_WINDOW:
#     tile_color = {
#         2: '#e4e8f7',
#         4: '#efddb5',
#         8: '#fcd368',
#         16: '#ffb366',
#         32: '#f66',
#         64: '#ff4242',
#         128: '#fbe18d',
#         256: '#f9ce48',
#         512: '#ffb2a4',
#         1024: '#ff8fbb',
#         2048: '#c9ff97',
#     }
#     def __init__(self,gridOBJ):
#         self.grid = gridOBJ
#         self.root = tk.Tk()
#         self.root.title('2048')
#         self.storeLabels = []
#         self.frame = Frame(self.root , bg = "#92877d")
#         # self.frame.pack()
#         for i in range(self.grid.size):
#             rowLabels = []
#             for j in range(self.grid.size):
#                 label = Label(self.frame, text='' , bg = '#9e948a' , width = 6  , height = 3, font = ('Times', 34, 'bold'))
#                 label.grid(row = i , column = j, padx = 10 , pady = 10)
#                 rowLabels.append(label)
#             self.storeLabels.append(rowLabels)
#         self.frame.grid()
#     def modify_gui(self):
#         for row in range(self.grid.size):
#             for col in range(self.grid.size):
#                 if(self.grid.CurrentGrid[row][col]!=0):
#                     bgColor = GUI_WINDOW.tile_color[self.grid.CurrentGrid[row][col]]
#                     self.storeLabels[row][col].configure(text = str(self.grid.CurrentGrid[row][col]) , bg = bgColor , fg = 'black')
#                 else:
#                     self.storeLabels[row][col].configure(text = '' , bg = '#9e948a')
    
class GAME:
    def __init__(self,gridOBJ):
        self.grid = gridOBJ
        # self.gui = guiOBJ
        self.startingCellsCNT = 2
        self.filled_grid = False
        self.task_completed = False
        self.storage_list = []
        self.Highest_Tile = 0
        self.required_sum = 8
        self.storage = defaultdict(list)
        self.parent = {}
        self.skip_states = {}
        self.start_game()

    def all_possible_move_without_random_insertion(self):
        store = []
        before_any_move = self.grid.CurrentGrid[::]
        # 0th Element -> UP
        # 1th Element -> Down
        # 2nd Element -> Left
        # 3rd Element -> Right
        self.grid.up_move()
        store.append(self.grid.CurrentGrid[::])
        self.grid.down_move()
        store.append(self.grid.CurrentGrid[::])
        self.grid.left_move()
        store.append(self.grid.CurrentGrid[::])
        self.grid.right_move()
        store.append(self.grid.CurrentGrid[::])
        return store
    

    def start_game(self):

        # Adding Random Cells

        for i in range(self.startingCellsCNT):                                 
            self.grid.generate_random_cell()

        # Printing Initial Grid

        print("\n\nINITIAL GRID :-\n\n")
        self.grid.print_grid()

        # Implementation  1   -> DFS

        self.dfs(self.grid.CurrentGrid)

        # Implementation  2   -> Random Var

        # while(True):
        #     before_move_grid = self.grid.CurrentGrid[::]
        #     move = random.choice(['Left' , 'Right' , 'Left' , 'Down'])
        #     if(move=='Left'):
        #         self.grid.left_move()
        #     if(move=='Right'):
        #         self.grid.right_move()
        #     if(move=='Up'):
        #         self.grid.up_move()
        #     if(move=='Down'):
        #         self.grid.down_move()
            
        #     after_move_grid = self.grid.CurrentGrid[::]
        #     if(before_move_grid==after_move_grid):
        #         continue
        #     self.grid.generate_random_cell()
        #     print("Move :- {}\n\n".format(move))
        #     self.grid.print_grid()
        #     if(self.grid.get_sum_of_grid(self.grid.CurrentGrid)==self.required_sum):
        #         break
        #     if(self.grid.get_sum_of_grid(self.grid.CurrentGrid)<self.required_sum):
        #         continue
        #     if(self.grid.get_sum_of_grid(self.grid.CurrentGrid)>self.required_sum):
        #         print("BackTracking ...\n\n")
        #         self.grid.CurrentGrid = before_move_grid[::]
        #         self.grid.print_grid()
        #         continue


    def dfs(self,matrix):
        # Checks if the Condition is Satisfied in the Start itself
        if(self.grid.get_sum_of_grid(self.grid.CurrentGrid)==self.required_sum):
            self.task_completed = True
            return
        
        # Checks if Our Task is Completed -> Then we can simply return it to main function
        if(self.task_completed==True):
            return

        # Checking For Already Existing State
        try:
            if(self.skip_states[self.matrix_to_string(matrix)] == True):
                return
        except:
            pass
        
        # Iterating Over All Moves and BackTracking On OverShoot Sum 
        count = 0
        for move in ['Left','Right','Up','Down']:
            count+=1
            if(self.task_completed==True):
                return

            # Saving Parent Matrix So that We Can Restore it Back from Child Matrix Which Overshooted 
            save_Matrix = self.grid.CurrentGrid[::]
            if(move=='Left'):
                self.grid.left_move()
            if(move=='Right'):
                self.grid.right_move()
            if(move=='Up'):
                self.grid.up_move()
            if(move=='Down'):
                self.grid.down_move()
            after_move = self.grid.CurrentGrid[::]

            #Checking if Game Over
            if(after_move==save_Matrix and count==4):
                print("Game Over Now BackTracking\n\n")
                self.skip_states[self.matrix_to_string(self.grid.CurrentGrid)] = True
                self.grid.CurrentGrid = self.parent[self.matrix_to_string(self.grid.CurrentGrid)][::]
            # Checking If Current Move Changed the Matrix Else We Can Continue
            if(after_move==save_Matrix):
                print("!!!! Again {} is not Possible -> Trying Different Move !!!!\n\n".format(move))
                continue
            self.grid.generate_random_cell()

            # Storing Child in Parent Graph/Tree
            self.parent[self.matrix_to_string(self.grid.CurrentGrid)] = save_Matrix[::]

            #Setting Highest Tile
            self.set_highest_tile()
            print("\n\nMove = {}              Highest Tile/Score:- {}\n".format(move,self.Highest_Tile))
            self.grid.print_grid()

            # We Found the Required Sum
            if(self.grid.get_sum_of_grid(self.grid.CurrentGrid)==self.required_sum):
                self.task_completed = True
                return
            
            # Sum is still less than Required Sum So we Continue with the child itself
            if(self.grid.get_sum_of_grid(self.grid.CurrentGrid)<self.required_sum):
                self.dfs(self.grid.CurrentGrid)
                if(self.task_completed==True):
                    return

                #Saving State In Storage Map To Reduce Computation Power
                childState = self.matrix_to_string(self.grid.CurrentGrid)
                ParentState = self.matrix_to_string(save_Matrix)
                if(childState not in self.storage[ParentState]):
                    self.storage[ParentState].append(childState)
                if(len(ParentState) == self.grid.maximum_random_states()):
                    self.skip_states[self.matrix_to_string(save_Matrix)] = True

                self.grid.CurrentGrid = self.parent[self.matrix_to_string(self.grid.CurrentGrid)]
            
            # Sum Overshoots the Required Sum so we Need to BackTrack to its Parent Matrix 
            if(self.grid.get_sum_of_grid(self.grid.CurrentGrid)>self.required_sum):
                self.grid.CurrentGrid = self.parent[self.matrix_to_string(self.grid.CurrentGrid)]
                self.set_highest_tile()
                print("\n\nSUM OverShoot -> BACK TRACK Done           Highest Tile/Score:- {}\n".format(self.Highest_Tile))
                self.grid.print_grid()

    # def keyboard_reader(self,event):
    #     key_pressed = event.keysym
    #     before_move_grid = self.grid.CurrentGrid[::]
    #     move_made = False
    #     if(key_pressed=='Left' or key_pressed=='a' or key_pressed=='A'):
    #         self.grid.left_move()
    #         move_made = True
    #     if(key_pressed=='Right' or key_pressed=='d' or key_pressed=='D'):
    #         self.grid.right_move()
    #         move_made = True
    #     if(key_pressed=='Up' or key_pressed=='w' or key_pressed=='W'):
    #         self.grid.up_move()
    #         move_made = True
    #     if(key_pressed=='Down' or key_pressed=='s' or key_pressed=='S'):
    #         self.grid.down_move()
    #         move_made = True
    #     else:
    #         pass
    #     after_move_grid = self.grid.CurrentGrid[::]
    #     if(before_move_grid!=after_move_grid and move_made==True):
    #         self.grid.generate_random_cell()
    #         self.gui.modify_gui()
        
    #     currentGrid_copy = self.grid.CurrentGrid[::]
    #     self.grid.up_move()
    #     self.grid.right_move()
    #     self.grid.left_move()
    #     self.grid.down_move()
    #     if(self.grid.CurrentGrid == currentGrid_copy):
    #         self.gameOver = True
    #     self.grid.CurrentGrid = currentGrid_copy[::]
    #     self.check_filled_grid()
    #     if(self.filled_grid==True and self.gameOver==True):
    #         messagebox.showinfo("Oops!!", "No Moves Left!")
    #         self.grid.CurrentGrid = self.grid.empty_grid()
    #         self.Highest_Tile = 0
    #         self.gameOver = False
    #         self.start_game()

    def matrix_to_string(self,matrix):
        s=""
        for i in range(len(matrix)):
            rowS = ""
            for j in range(len(matrix[0])):
                rowS+=str(matrix[i][j])
            s+=rowS
        return s

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

    

        

class GRID:
    def __init__(self,size):
        self.size = size
        self.CurrentGrid = self.empty_grid()
        
    def empty_grid(self):
        return [[0 for i in range(size)] for j in range(self.size)]

    def generate_random_cell(self):
        empty_cells = self.get_empty_cells()
        random_cell = random.choice(empty_cells)
        if(random.random()<0.5):
            self.CurrentGrid[random_cell[0]][random_cell[1]] = 2
        else:
            self.CurrentGrid[random_cell[0]][random_cell[1]] = 4
    
    def get_count_of_different_values(self):
        result=dict()
        for i in range(self.size):
            for j in range(self.size):
                if(self.CurrentGrid[i][j] in result):
                    result[self.CurrentGrid[i][j]]+=1
                else:
                    result[self.CurrentGrid[i][j]]=1
        return result
        
    def maximum_random_states(self):
        result = 0
        for i in range(self.size):
            for j in range(self.size):
                if(self.CurrentGrid[i][j]==0):                                              
                    result+=1
        return 2**result

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

    def generate_random_move(self):
        possibleMoves = ['Up','Down','Left','Right']
        move = random.choice(possibleMoves)
        return move

    def get_sum_of_grid(self,matrix):
        sum=0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                sum+=matrix[i][j]
        return sum

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
                # print(self.CurrentGrid[i][j],end="       ")
                print("{:<4}".format(self.CurrentGrid[i][j]),end="     ")
            print("")
        print("\n\n----------------------------------------------\n\n")


if __name__ == '__main__':
    size = 4         

    # Creates an Empty Grid of required Size
    grid = GRID(size)

    # Gui Class Implementation Which is now Commented as per Question Demands
    # gui = GUI_WINDOW(grid)

    # Game Class 
    """
    Constructor is like this :- 
        self.grid = gridOBJ             #import Empty Grid
        self.gui = guiOBJ               #Import Gui Window
        self.startingCellsCNT = 2       #Number of starting random cells we should have
        self.task_completed = False     #We Found the Required Sum (may be 8,10,12... anything)
        self.required_sum = 2044        #This is the Requred Sum (We can set it to any even number less than MAX possible)
        self.storage = {}               #Stores All the Visited States Where it BackTracked
        self.start_game()               #Function Which starts the Game is executed in the constructor      
    """
    game = GAME(grid)
    