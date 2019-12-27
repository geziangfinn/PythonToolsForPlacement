from c_row import *
from c_net import *
from c_cell import *
from c_file_parser import *
import sys


class Benchmark:
    """
    Defines a full Map/Benchmark object with rows, cells, nets
    """

    counter = -1

    def __init__(self, file_name: str):
        self.file_name = file_name  # for FParser, give path/name without extension
        self.name = str(self.file_name).split('/')[-1]

        Benchmark.counter += 1
        self.id = Benchmark.counter

        self.area = 0.0
        self.low_y = 0.0
        self.left_x = 0.0
        self.high_y = 0.0
        self.right_x = 0.0
        self.height = 0.0
        self.width = 0.0

        self.cells = {}
        self.nets = {}
        self.rows = []
        self.pins = {}  # terminal-cells of 1/1 size

        self.hpwl = 0.0

    def calculate_benchmark_area(self):
        for row in self.rows:
            self.area += row.area

    def calculate_benchmark_coordinates(self):
        min_y = left_x = float(sys.float_info.max)
        max_y = right_x = float(sys.float_info.min)

        for cell in self.cells.keys():
            if self.cells[cell].low_y <= min_y:
                min_y = self.cells[cell].low_y
            if self.cells[cell].left_x <= left_x:
                left_x = self.cells[cell].left_x
            if self.cells[cell].high_y >= max_y:
                max_y = self.cells[cell].high_y
            if self.cells[cell].right_x >= right_x:
                right_x = self.cells[cell].right_x

        self.low_y = min_y
        self.left_x = left_x
        self.high_y = max_y
        self.right_x = right_x

        self.width = self.right_x - self.left_x
        self.height = self.high_y - self.low_y

    def generate_benchmark_cells(self, file_parser: FParser):
        """
        Generates Cell instances inside Benchmark
        :param file_parser:
        :return:
        """

        tmp = []
        cell_coordinates = file_parser.read_cells()
        for cell_name in cell_coordinates.keys():
            cell = Cell()
            cell.generate_cell(cell_coordinates[cell_name], cell_name)
            self.cells[cell_name] = cell
            tmp.append(cell)
        return tmp

    def generate_benchmark_nets(self, file_parser: FParser, tmp_cells_list: list):
        """
        Generates all Nets
        :param tmp_cells_list:
        :param file_parser:
        :return:
        """

        nets, nets_index = file_parser.read_nets()
        for _ in nets.keys():
            net = Net()
            net.generate_net(nets, tmp_cells_list, nets_index)
            self.nets[net.name] = net

    def generate_benchmark_rows(self, file_parser: FParser):
        """
        Generate Row instances inside Benchmark
        :param file_parser:
        :return:
        """

        rows = file_parser.read_rows()
        for row_name in rows.keys():
            row = Row()
            row.generate_row(rows[row_name])
            self.rows.append(row)

    def return_rows_number(self):
        return len(self.rows)

    def calculate_hpwl(self):
        for net in self.nets.keys():
            self.hpwl += self.nets[net].hpwl

    def generate_benchmark(self):
        """
        Generates a Benchmark instance with all its cells, nets and rows
        :return:
        """

        file_parser = FParser(self.file_name)

        # 1. Generate Cells
        tmp_cells_list = self.generate_benchmark_cells(file_parser)
        # 2. Generate Nets
        self.generate_benchmark_nets(file_parser, tmp_cells_list)
        # 3. Generate Rows
        self.generate_benchmark_rows(file_parser)
        # 4. Calculate remaining attributes
        self.calculate_benchmark_area()
        self.calculate_benchmark_coordinates()
        # 5. Calculate hpwl
        for net in self.nets.keys():
            self.nets[net].calculate_net_corners(self.cells)
            self.nets[net].calculate_hpwl()
        self.calculate_hpwl()
