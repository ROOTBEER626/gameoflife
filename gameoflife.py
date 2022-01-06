#If a cell is alive, and 2 or 3 of it's neighbours are alive, the cell reamins alive
#if a cell is alive and it has more than 3 alive neighbours, it dies of overcrowding
#i a cell is alive and it has fewer than 2 alive neighbours, it dies of loneliness
#if a cell is dead and it has exatly 3 neighbours it becomes alive again
#from tkinter import *
import tkinter as tk
import random

class Square:

    def __init__(self, coords, length, size, state=False, active_color='black', inactive_color='white'):
        self.length = length
        self.coords = coords
        self.size = size
        self.state = state
        self.active_color = active_color
        self.inactive_color = inactive_color

    def rect(self):
        return (self.coords[0]+self.size, self.coords[1]+self.size)

    def inbounds(self, coord):
        (x,y) = coord

        return (x >= 0 and x <= self.length-self.size) and (y >= 0 and y <= self.length-self.size)

    def neighbours(self):
        (x,y) = self.coords

        return list(filter(self.inbounds, [
            (x-self.size, y+self.size), (x, y+self.size), (x+self.size, y+self.size),
            (x-self.size, y),
            (x-self.size, y-self.size), (x, y-self.size), (x+self.size,y-self.size),
            ]))

    def get_color(self):
        return self.active_color if self.state else self.inactive_color


class Grid:
    def __init__(self,length, size, tolerance, active_color='black', inactive_color='white' ):

        self.length = length
        self.tolerance = tolerance
        self.active_color = active_color
        self.inactive_color = inactive_color

        self.squares = self.make_squares(size)
        

        #bind click action
        ##self.bind("<Button-1>", self.handleMouseClick)
        #bind moving whiiile clikcing
        #self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of modified cells
        #self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

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

    def get_neighbors(self, cell):
        coords = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
        if cell.abs == 49:
            for c in coords:
                if c[1] == 1:
                    coords.remove(c)
        if cell.abs == 0:
            for c in coords:
                if c[1] == -1:
                    coords.remove(c)
        if cell.ord == 49:
            for c in coords:
                if c[0] == 1:
                    coords.remove(c)
        if cell.ord == 0:
            for c in coords:
                if c[0] ==  -1:
                    coords.remove(c)
        neighbors = []
        for n in coords:
            neighbors.append(self.grid[cell.abs+n[1]][cell.ord+n[0]])
        return neighbors



    def animate(self):
        while True:
            time.sleep(.5)
            switch = []
            for line in self.grid:
                for cell in line:
                    if cell.fill == True:
                        if (self.check_fewer_than_2_alive(cell) or self.check_more_than_3_alive(cell)):
                            switch.append(cell)
                    elif cell.fill == False:
                        if self.check_exactly_3_alive(cell):
                            switch.append(cell)
            if len(switch) > 0:
                self.update(switch)

    def update(self, switches):
        print(len(switches))
        print("Updating")
        for c in switches:
            cell = self.grid[c.ord][c.abs]
            cell._switch()
            c.update()
        self.switched.clear()

    def check_2_or_3_alive(self, cell):
        neighbors = self.get_neighbors(cell)
        alive = 0
        for c in neighbors:
            if c.fill == True:
                alive += 1
        if alive == 2 or alive == 3:
            return True
        else:
            return False


    def check_more_than_3_alive(self, cell):
        neighbors = self.get_neighbors(cell)
        alive = 0
        for c in neighbors:
            if c.fill == True:
                alive += 1
        if alive >= 3:
            return True
        else:
            return False

    def check_fewer_than_2_alive(self,cell):
        neighbors = self.get_neighbors(cell)
        alive = 0
        for c in neighbors:
            if c.fill == True:
                alive += 1
        if alive <= 2: 
            return True
        else:
            return False

    def check_exactly_3_alive(self,cell):
        neighbors = self.get_neighbors(cell)
        alive = 0
        for c in neighbors:
            if c.fill == True:
                alive += 1
        if alive == 3:
            return True
        else: 
            return False


class App:
    def __init__(self, length, size, tolerance):
        self.length = length
        self.size = size
        self.tolerance = tolerance

        if not self.length % self.size == 0:
            raise Exception("The square don't fit evenly on the screen." +
                            "Box size needs to be a factor of window size.")

        self.grid = Grid(self.length, self.size, self.tolerance,  active_color='#008080', inactive_color='white')

        self.root = tk.Tk()

        self.canvas = tk.Canvas(self.root, height = self.length, width = self.length)

        self.canvas.pack()

        self.items = self.update_canvas()

        self.root.after(5, self.refresh_screen)

        self.root.mainloop()

    def refresh_screen(self):
        self.grid.rules()
        self.update_canvas(canvas_done=True, canvas_items=self.items)

        self.root.after(5, self.refresh_screen)

    def update_canvas(self, canvas_done=False, canvas_items={}):
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
