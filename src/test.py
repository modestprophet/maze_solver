import unittest
from maze_solver import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_another_maze(self):
        num_cols = 24
        num_rows = 20
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows
        )

    def test_entrance_exit_exist(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertFalse(m1._cells[0][0].has_top_wall)
        self.assertFalse(m1._cells[num_cols-1][num_rows-1].has_bottom_wall)
    
    def test_reset_visited(self):
        solver = Maze(0, 0, 3, 3, 10, 10)

        for i in range(3):
            for j in range(3):
                solver._cells[i][j].visited = True

        solver._reset_visited(0, 0)

        for i in range(3):
            for j in range(3):
                self.assertFalse(solver._cells[i][j].visited)


if __name__ == "__main__":
    unittest.main()

