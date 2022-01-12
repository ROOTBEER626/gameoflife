#if a cell is alive, and 2 or 3 of it's neighbours are alive, the cell reamins alive
#if a cell is alive and it has more than 3 alive neighbours, it dies of overcrowding
#i a cell is alive and it has fewer than 2 alive neighbours, it dies of loneliness
#if a cell is dead and it has exatly 3 neighbours it becomes alive again
#from tkinter import *
import tkinter as tk
import random
import time


class Square:

    def __init__(self, coords, length, size, state=False, active_color='black', inactive_color='white'):
        self.length = length
        self.coords = coords
        self.size = size
        self.state = state
        self.active_color = active_color
        self.inactive_color = inactive_color
    
    """Gives the bottom right values of square"""
    def rect(self):
        return (self.coords[0]+self.size, self.coords[1]+self.size)
    
    """Returns whether a coordinate is inbounds in the grid"""
    def inbounds(self, coord):
        (x,y) = coord

        return (x >= 0 and x <= self.length-self.size) and (y >= 0 and y <= self.length-self.size)

    """Returns all neighbours to the object"""
    def neighbours(self):
        (x,y) = self.coords

        return list(filter(self.inbounds, [
            (x-self.size, y+self.size), (x, y+self.size), (x+self.size, y+self.size),
            (x-self.size, y),
            (x-self.size, y-self.size), (x, y-self.size), (x+self.size,y-self.size),
            ]))

    """Returns a color whether the object is alive or dead"""
    def get_color(self):
        return self.active_color if self.state else self.inactive_color


class Grid:
    def __init__(self,length, size, tolerance, active_color='black', inactive_color='white' ):

        self.length = length
        self.tolerance = tolerance
        self.active_color = active_color
        self.inactive_color = inactive_color

        self.squares = self.make_squares(size)
        
    """Creates a dictionary of square objects"""
    def make_squares(self, size):
        squares = {}
        for y in range(0, self.length, size):
            for x in range(0, self.length, size):
                if random.random() < self.tolerance:
                    squares[(x,y)] = Square((x,y),
                                            self.length,
                                            size,
                                            active_color=self.active_color,
                                            inactive_color=self.inactive_color)
                else:
                    squares[(x,y)] = Square((x,y),
                                            self.length,
                                            size,
                                            state = True,
                                            active_color=self.active_color,
                                            inactive_color=self.inactive_color)
        return squares

    """Take a list of coordinates and make them alive cells
    Not used but can be used to set alive squares"""
    def set_squares(self, on_coordinates):
        for coord, square in self.squares:
            if coord in on_coordinates:
                square.state=True

    def rules(self):
        for coord, square in self.squares.items():
            alive_neighbours = 0

            neighbours = square.neighbours()

            for neighbour in neighbours:
                if self.squares[neighbour].state:
                    alive_neighbours += 1

            if square.state:
                #Rule 1
                if alive_neighbours < 2:
                    square.state=False
                #Rule 3
                elif alive_neighbours > 3:
                    square.state = False
                #Rule 2
                else:
                    continue
            else:
                #Rule 4
                if alive_neighbours == 3:
                    square.state = True

class App:
    def __init__(self, length, size, tolerance):
        self.length = length
        self.size = size
        self.tolerance = tolerance
        self.go = False

        if not self.length % self.size == 0:
            raise Exception("The square don't fit evenly on the screen." +
                            "Box size needs to be a factor of window size.")

        self.grid = Grid(self.length, self.size, self.tolerance,  active_color='#008080', inactive_color='white')

        self.root = tk.Tk()

       #Increase the size of the canvas so that I will be able to insert the buttons 
        self.canvas = tk.Canvas(self.root, height = self.length, width = self.length+100)

        self.canvas.pack()
        
        self.items = self.update_canvas()

        #start button
        start_button = tk.Button(self.root, text = "Start", command = self.start)
        start_button.configure(width = 10, activebackground = "#33B5E5")
        start_button_window = self.canvas.create_window(1065,150, window=start_button)


        #pause button
        pause_button = tk.Button(self.root, text = "Pause", command = self.pause)
        pause_button.configure(width = 10, activebackground = "#33B5E5")
        pause_button_window = self.canvas.create_window(1065,175, window=pause_button)


        #step button
        step_button = tk.Button(self.root, text = "Step", command = self.step)
        step_button.configure(width = 10, activebackground = "#33B5E5")
        step_button_window = self.canvas.create_window(1065,200, window=step_button)

        #reset button
        reset_button = tk.Button(self.root, text='Reset', command=self.reset)
        reset_button.configure(width=10,activebackground="#33B5E5")
        reset_button.window = self.canvas.create_window(1065, 225,window=reset_button)

        #clear button
        clear_button = tk.Button(self.root, text="clear", command=self.clear)
        clear_button.configure(width=10,activebackground="#33B5E5")
        clear_button_window = self.canvas.create_window(1065,250, window = clear_button)

        #blocks the program here
        self.root.mainloop()

        #Old code just here for the time being 
        #bind click action
        ##self.bind("<Button-1>", self.handleMouseClick)
        #bind moving whiiile clikcing
        #self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of modified cells
        #self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

    def start(self):
        self.go = True
        self.root.after(5, self.refresh_screen)

    def pause(self):
        self.go = False

    def step(self):
        self.go = True
        self.root.after(5, self.refresh_screen(step=True))

    def reset(self):
        #reset the board
        return
    
    def clear(self):
        #clear the board
        return

    def __eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleMouseClick(self, event):
        row, column = self.__eventCoords(event)
        cell = self.grid[row][column]
        cell._switch()
        cell.draw()
        #add the cell to the list of cell switched during the click
        self.switched.append(cell)

    def handleMouseMotion(self, event):
        row, column = self.__eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            cell._switch()
            cell.draw()
            self.switched.append(cell)  

    def refresh_screen(self, step = False):
        if self.go == False:
            return
        self.grid.rules()
        self.update_canvas(canvas_done=True, canvas_items=self.items)
        if step == True:
            return
        self.root.after(5, self.refresh_screen)

    def update_canvas(self, canvas_done=False, canvas_items={}):
        #time.sleep(.1)
        square_items = self.grid.squares

        if not canvas_done:
            for coords, square in square_items.items():
                (b_r_x, b_r_y) = square.rect()
                (t_l_x, t_l_y) = coords

                canvas_items[coords] = self.canvas.create_rectangle(t_l_x, t_l_y, b_r_x, b_r_y, fill=square.get_color())

            return canvas_items

        else:

            if canvas_items:
                for coords, item in canvas_items.items():

                    self.canvas.itemconfig(item, fill=square_items[coords].get_color())

            else:
                raise ValueError("No canvas_item given for re-iterating over grid.")


if __name__ == "__main__":
    app = App(1000, 25, tolerance=0.7)
