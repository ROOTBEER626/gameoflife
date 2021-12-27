#If a cell is alive, and 2 or 3 of it's neighbours are alive, the cell reamins alive
#if a cell is alive and it has more than 3 alive neighbours, it dies of overcrowding
#i a cell is alive and it has fewer than 2 alive neighbours, it dies of loneliness
#if a cell is dead and it has exatly 3 neighbours it becomes alive again
from tkinter import *

dead_color = 'white'
alive_color = 'blue'

class Cell():
    FILLED_COLOR_BG = 'green'
    EMPTY_COLOR_BG = 'white'
    FILLED_COLOR_BORDER = 'green'
    EMPTY_COLOR_BORDER = 'black'

    def __init__(self, master, x, y, size):
        """Constructor of the object caled by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.fill = False

    def _switch(self):
        self.fill = not self.fill

    def draw(self):
        if self.master != None:
            fill = Cell.FILLED_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER

            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin,ymin, xmax, ymax, fill = fill, outline = outline)

class CellGrid(Canvas):
    def __init__(self, master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber, height = cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize
        self.alive = []
        self.dead = []
        
        self.grid = []
        for row in range(rowNumber):
            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)

        self.initilize_dead()
        #memorize the cells that have been modified to avoid many switching of state during mouse motion
        self.switched = []

        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)
        #bind moving whiiile clikcing
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of modified cells
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

        self.draw()
        #self.animate()

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

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
        self.update_dead_or_alive(cell)

    def handleMouseMotion(self, event):
        row, column = self.__eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            cell._switch()
            cell.draw()
            self.switched.append(cell)

    def initilize_dead(self):
        #50 by 50 grid
        for line in self.grid:
            for cell in line:
                self.dead.append(cell)
        

    def update_dead_or_alive(self, cell):
        if cell in self.dead:
            self.dead.remove(cell)
            self.alive.append(cell)
        elif cell in self.alive:
            self.alive.remove(cell)
            self.dead.append(cell)
        print(self.alive)

    def animate(self):
        while True:
            for line in self.grid:
                for cell in line:
                    if cell.fill == True:
                        #check that 2 or 3 neighbors are alive
                        cell.fill == True
                    if cell.fill == True:
                        #check if it has more than 3 alive neighbors
                        cell.fill == False
                    if cell.fill == True:
                        #check if it has fewer than 2 alive neighbords
                        cell.fill == False
                    if cell.fill == False:
                        #check if it has exactly 3 alive neightbors
                        cell.fill == True

if __name__ == "__main__":
    app = Tk()

    grid = CellGrid(app, 50, 50, 10)
    grid.pack()

    app.mainloop()
