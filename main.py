import random
from enum import Enum
from tkinter import *

import numpy as np

COLOR_END = '#D6000A'
COLOR_START = '#0ED100'
COLOR_WALL = 'black'
COLOR_PATH = 'white'
DIRECTIONS = Enum("DIR", ("U", "D", "L", "R"))


class Maze(object):
    def __init__(self, width=35, height=21, recursion_limit=2000):
        assert width % 2 == 1 and height % 2 == 1, "width and height must be odd"
        self.width = width
        self.height = height
        self.maze = np.ones((self.width, self.height), bool)
        try:
            sys.setrecursionlimit(recursion_limit)
        except RecursionError as e:
            print(e)

    def carve_maze(self, x, y):
        dir = random.randint(0, 3)

        for _ in range(4):
            if dir == 0:
                dx = 1
                dy = 0
            elif dir == 1:
                dx = 0
                dy = 1
            elif dir == 2:
                dx = -1
                dy = 0
            else:
                dx = 0
                dy = -1

            x1 = x + dx
            y1 = y + dy
            x2 = x1 + dx
            y2 = y1 + dy

            if 0 < x2 < self.width and 0 < y2 < self.height:
                if self.maze[x1, y1] and self.maze[x2, y2]:
                    self.maze[x1, y1] = False
                    self.maze[x2, y2] = False
                    self.carve_maze(x2, y2)

            dir = (dir + 1) % 4

    def generate_maze(self):
        random.seed()
        self.maze[1, 1] = False
        try:
            self.carve_maze(1, 1)
        except RecursionError:
            print('Size of maze is too big!')
            sys.exit(1)
        self.maze[1, 0] = False
        self.maze[self.width - 2, self.height - 1] = False

    def gui_maze(self, wall_size=10):
        tk = Tk()

        tk_width = self.width * wall_size + 1
        tk_height = self.height * wall_size + 1
        tk.title(u'Maze generator')
        tk.geometry(f"{tk_width}x{tk_height}+100+100")
        tk.resizable(False, False)
        c = Canvas(tk, width=tk_width, height=tk_height)
        c.pack()

        def rebuild_maze(event):
            tk.destroy()
            self.gui_maze()

        tk.bind("<Button-1>", rebuild_maze)

        self.generate_maze()
        x0, y0, x1, y1 = 0, 0, wall_size, wall_size

        for y in range(self.height - 1, -1, -1):
            for x in range(self.width - 1, -1, -1):
                if not self.maze[x, y]:
                    c.create_rectangle(x0, y0, x1, y1, fill=COLOR_PATH, width=0)
                else:
                    c.create_rectangle(x0, y0, x1, y1, fill=COLOR_WALL, width=0)
                x0 += wall_size
                x1 += wall_size
            x0 = 0
            y0 += wall_size
            x1 = wall_size
            y1 += wall_size
        c.create_rectangle(wall_size + 1, wall_size + 1, 2 * wall_size - 1, 2 * wall_size - 1, fill=COLOR_START,
                           width=0)
        c.create_rectangle(tk_width - 2 * wall_size, tk_height - 2 * wall_size, tk_width - wall_size - 1,
                           tk_height - wall_size - 1,
                           fill=COLOR_END, width=0)
        tk.mainloop()


if __name__ == '__main__':
    game = Maze(101, 101)
    game.gui_maze(10)
