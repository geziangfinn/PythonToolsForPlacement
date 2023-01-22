from c_benchmark import *
from c_row import *


class Grid:
    """
    Class used to divide any design into a grid of even dimensions.
    Creates a list of Benchmark class instances with the same properties as the original design.
    """

    def __init__(self, bench: Benchmark, dim: int):
        self.bench = bench
        self.dim = dim  # cutsize i.e. 2x2, 3x3
        self.grid = []

        self.ver_cut = bench.width // dim
        self.rows_num = len(bench.rows) // dim

    def grid_generation(self):
        # Create bins | benchmark class instances
        y = 0.0
        for i in range(self.dim):
            x = 0.0
            for j in range(self.dim):

                b = Benchmark(None)  # empty object
                b.low_y = y
                b.left_x = x

                if i == self.dim-1 and j == self.dim-1:
                    b.high_y = self.bench.high_y
                    b.height = b.high_y - b.low_y
                    b.num_rows = b.height / self.bench.rows[0].height
                    b.right_x = self.bench.right_x
                    b.width = b.right_x - b.left_x
                elif j == self.dim-1:
                    b.num_rows = self.rows_num
                    b.height = b.num_rows * self.bench.rows[0].height
                    b.high_y = b.low_y + b.height
                    b.right_x = self.bench.right_x
                    b.width = b.right_x - b.left_x
                else:
                    b.num_rows = self.rows_num
                    b.height = b.num_rows * self.bench.rows[0].height
                    b.high_y = b.low_y + b.height
                    b.width = self.ver_cut
                    b.right_x = b.left_x + b.width
                self.grid.append(b)

                x += self.ver_cut
            y += self.rows_num * self.bench.rows[0].height

        # Add cells accordingly 
        for cell in self.bench.cells.values():
            for bench in self.grid:
                if cell.low_y >= bench.low_y and cell.high_y <= bench.high_y and \
                        cell.left_x >= bench.left_x and cell.right_x <= bench.right_x:
                    bench.cells[cell.name] = cell
                    break
        
         # Add rows and make their dims match | add cells in their lists
        for row in self.bench.rows:
            for bench in self.grid:
                if bench.low_y <= row.corerow <= bench.high_y:
                    r = Row()
                    r.corerow = row.corerow
                    r.subroworigin = bench.left_x
                    r.higher_y = row.higher_y
                    r.right_x = bench.right_x
                    r.width = r.right_x - r.subroworigin
                    r.left_avail = r.subroworigin
                    r.right_avail = r.right_x
                    r.calculate_area()
                    r.calculate_density()
                    for cell in bench.cells.values():
                        if cell.low_y == r.corerow:
                            r.cells.append(cell)
                    bench.rows.append(r)

        return self.grid