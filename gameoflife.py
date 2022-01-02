#If a cell is alive, and 2 or 3 of it's neighbours are alive, the cell reamins alive
#if a cell is alive and it has more than 3 alive neighbours, it dies of overcrowding
#i a cell is alive and it has fewer than 2 alive neighbours, it dies of loneliness
#if a cell is dead and it has exatly 3 neighbours it becomes alive again
from tkinter import *
import time

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


            #This returns an int not a rectangle object
            self.master.create_rectangle(xmin,ymin, xmax, ymax, fill = fill, outline = outline)



    def update(self):

        #if this doesn't work we are gonna have to update it the same way we do it on the mouse click event
        fill = Cell.FILLED_COLOR_BG
        outline = Cell.FILLED_COLOR_BORDER

        if not self.fill:
            fill = Cell.EMPTY_COLOR_BG
            outline = Cell.EMPTY_COLOR_BORDER

        xmin = self.abs * self.size
        xmax = xmin + self.size
        ymin = self.ord * self.size
        ymax = ymin + self.size
        
        self.master.create_rectangle(xmin,ymin, xmax, ymax, fill = 'black', outline = outline)


class CellGrid(Canvas):
    def __init__(self, master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber, height = cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize
        
        self.grid = []
        for row in range(rowNumber):
            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)
        
        #memorize the cells that have been modified to avoid many switching of state during mouse motion
        self.switched = []

        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)
        #bind moving whiiile clikcing
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of modified cells
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())


        self.draw()

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



if __name__ == "__main__":
    app = Tk()
    app.geometry('1000x1000')

    grid = CellGrid(app, 50, 50, 10)
    grid.pack()
    btn = Button(app, text = 'Start', bd = '5',
                              command = grid.animate)
 
    btn.pack(side = 'left')   



    app.mainloop()
