import time
import random
from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "Solving this maze, yo!"
        self.canvas = Canvas(self.__root, width=width, height=height, bg="white")
        self.canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color):
        if not isinstance(line, Line):
            raise TypeError("line must be of type Line")

        line.draw(self.canvas, fill_color)


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Line:
    def __init__(self, point1, point2):
        if not isinstance(point1, Point) or not isinstance(point2, Point):
            raise ValueError("Both point1 and point2 must be Point objects")
        self.point1 = point1
        self.point2 = point2

    def __repr__(self):
        return f"Line({self.point1}, {self.point2})"

    def draw(self, canvas, fill_color):
        if not isinstance(canvas, Canvas):
            raise ValueError("Canvas must be an instance of Canvas")
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2
        )


class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win
        self.visited = False

    def __repr__(self):
        return f"Cell(x1={self._x1}, y1={self._y1}, x2={self._x2}, y2={self._y2}, win={self._win})"

    def draw(self):
        if self._win is None:
            return

        points = [
            (Point(self._x1, self._y1), Point(self._x1, self._y2), self.has_left_wall),
            (Point(self._x2, self._y1), Point(self._x2, self._y2), self.has_right_wall),
            (Point(self._x1, self._y1), Point(self._x2, self._y1), self.has_top_wall),
            (Point(self._x1, self._y2), Point(self._x2, self._y2), self.has_bottom_wall),
        ]

        for p1, p2, has_wall in points:
            color = "black" if has_wall else "white"
            line = Line(p1, p2)
            self._win.draw_line(line, color)

    def draw_move(self, to_cell, undo=False):
        x1 = (self._x1 + self._x2) / 2
        y1 = (self._y1 + self._y2) / 2
        x2 = (to_cell._x1 + to_cell._x2) / 2
        y2 = (to_cell._y1 + to_cell._y2) / 2

        start = Point(x1, y1)
        end = Point(x2, y2)
        line = Line(start, end)

        color = 'gray85' if undo else 'red'
        self._win.draw_line(line, color)


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        if seed is not None:
            random.seed(seed)
        self._create_cells()

    def _create_cells(self):
        for i in range(self._num_cols):
            column = []
            for j in range(self._num_rows):
                column.append(None)
            self._cells.append(column)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j] = Cell(0, 0, 0, 0, self._win)
                self._draw_cell(i, j)

        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_visited(self._num_cols, self._num_rows)

    def _draw_cell(self, i, j):
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j]._x1 = x1
        self._cells[i][j]._y1 = y1
        self._cells[i][j]._x2 = x2
        self._cells[i][j]._y2 = y2
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        # entrance
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)

        # exit
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False
        self._draw_cell(self._num_cols-1, self._num_rows-1)
    
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            directions = []
            if i > 0 and not self._cells[i-1][j].visited:
                directions.append((-1, 0))  # left
            if i < self._num_cols - 1 and not self._cells[i+1][j].visited:
                directions.append((1, 0))  # right
            if j > 0 and not self._cells[i][j-1].visited:
                directions.append((0, -1))  # up
            if j < self._num_rows - 1 and not self._cells[i][j+1].visited:
                directions.append((0, 1))  # down

            if not directions:
                self._draw_cell(i, j)
                return

            di, dj = random.choice(directions)
            ni, nj = i + di, j + dj

            if di == -1:  # left
                self._cells[i][j].has_left_wall = False
                self._cells[ni][nj].has_right_wall = False
            elif di == 1:  # right
                self._cells[i][j].has_right_wall = False
                self._cells[ni][nj].has_left_wall = False
            elif dj == -1:  # up
                self._cells[i][j].has_top_wall = False
                self._cells[ni][nj].has_bottom_wall = False
            elif dj == 1:  # down
                self._cells[i][j].has_bottom_wall = False
                self._cells[ni][nj].has_top_wall = False

            self._draw_cell(i, j)
            self._draw_cell(ni, nj)
            self._animate()

            self._break_walls_r(ni, nj)

    def _reset_visited(self, i, j):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if (0 <= ni < self._num_cols and 0 <= nj < self._num_rows and
                    not self._cells[ni][nj].visited and
                    not self._has_wall(i, j, ni, nj)):
                self._cells[i][j].draw_move(self._cells[ni][nj])
                if self._solve_r(ni, nj):
                    return True
                self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)

        return False

    def _has_wall(self, i, j, ni, nj):
        if i == ni:  # vertical move
            if j < nj:  # moving down
                return self._cells[i][j].has_bottom_wall
            else:  # moving up
                return self._cells[i][j].has_top_wall
        else:  # horizontal move
            if i < ni:  # moving right
                return self._cells[i][j].has_right_wall
            else:  # moving left
                return self._cells[i][j].has_left_wall


def main():
    win = Window(800, 600)
    maze = Maze(5,5, 29, 39, 20, 20, win)
    if maze.solve():
        print("Maze solved!")
    else:
        print("No solution found.")
    win.wait_for_close()


if __name__ == '__main__':
    main()

