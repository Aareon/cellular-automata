import random
import numpy as np
from engine import Engine
from engine.locals import COLORS, QUIT, rect


class Game(Engine):
    def __init__(self, height, width, **kwargs):
        self.height = height
        self.width = width
        Engine.__init__(self, height, width, **kwargs)

        self.cell_size = kwargs.get('cell_size', 10)
        self.rows = int(width/self.cell_size)
        self.columns = int((height/self.cell_size)+self.cell_size*2)

        self.grid = np.zeros((self.columns, self.rows))

        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                self.grid[x][y] = np.random.choice((True, False), 1, p=(0.1, 0.9))[0]

        self.colors = kwargs.get('colors', False)

    def event(self, event):
        if event.type == QUIT:
            Engine.quit()

    def get_neighbors(self, coords):
        x, y = coords

        # possible neighbors at coordinates
        neighbors = (
            (x-1, y), (x+1, y),
            (x, y-1), (x, y+1),
            (x-1, y-1), (x+1, y+1),
            (x-1, y+1), (x+1, y-1)
        )

        num_neighbors = 0
        for i, j in neighbors:
            try:
                num_neighbors += self.grid[i][j]
            except IndexError:
                pass

        return num_neighbors

    def do_rules(self, coords, num_neighbors):
        x, y = coords
        cell = self.grid[x][y]

        if cell == 1:
            # 1. Any live cell with fewer than two live neighbors dies, as if by under population.
            if num_neighbors < 2:
                return 0

            # 2. Any live cell with two or three live neighbors lives on to the next generation.
            elif num_neighbors in (2, 3):
                return 1

            # 3. Any live cell with more than three live neighbors dies, as if by overpopulation.
            elif num_neighbors > 3:
                return 0

        else:
            # Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
            if num_neighbors == 3:
                return 1

        return 0

    def update(self):
        # modified grid. used so that the state of one cell is not affected by the change in state of another
        mod_grid = self.grid.copy()

        for x, column in enumerate(self.grid):
            for y, cell in enumerate(column):
                num_neighbors = self.get_neighbors((x, y))
                mod_grid[x][y] = self.do_rules((x, y), num_neighbors)

        self.grid = mod_grid

    def get_color(self, coords):
        x, y = coords
        if self.grid[x][y] == 1:
            return random.choice(COLORS) if self.colors else tuple((255, 255, 255))
        else:
            return tuple((0, 0, 0))

    def draw(self):
        for x, column in enumerate(self.grid):
            for y, cell in enumerate(column):
                rect(
                    self.screen,
                    self.get_color((x, y)),
                    (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                )


if __name__ == '__main__':
    game = Game(600, 800, fps=10, colors=True)
    game.run()
