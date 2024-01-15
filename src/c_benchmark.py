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
        print("Benchmark name: ",self.name)
        Benchmark.counter += 1
        self.id = Benchmark.counter

        self.area = 0.0
        # ll and ur for the whole chip
        self.low_y = 0.0
        self.left_x = 0.0
        self.high_y = 0.0
        self.right_x = 0.0

        # width and height are for the whole chip
        self.height = 0.0
        self.width = 0.0
        self.density = 0.0

        # coreRegion: region in the chip consists of rows
        self.coreRegion_left_x=0.0
        self.coreRegion_right_x=0.0
        self.coreRegion_low_y=0.0
        self.coreRegion_high_y=0.0

        self.cells = {}# map for all cells
        self.nets = {}
        self.num_rows = 0
        self.rows = []
        self.pins = {}

        self.hpwl = 0.0

    def calculate_coreRegion_area(self):
        for row in self.rows:
            self.area += row.area

    def calculate_benchmark_coordinates(self):
        min_y = min_x = float(sys.float_info.max)
        max_y = max_x = float(sys.float_info.min)

        for row in self.rows:
            if row.corerow <= min_y:
                min_y = row.corerow
            if row.subroworigin <= min_x:
                min_x = row.subroworigin
            if row.higher_y >= max_y:
                max_y = row.higher_y
            if row.right_x >= max_x:
                max_x = row.right_x

        self.coreRegion_left_x=min_x
        self.coreRegion_right_x=max_x
        self.coreRegion_low_y=min_y
        self.coreRegion_high_y=max_y

        for cell_name in self.cells.keys():
            if self.cells[cell_name].left_x<=min_x:
                min_x=self.cells[cell_name].left_x
            if self.cells[cell_name].right_x>=max_x:
                max_x=self.cells[cell_name].right_x
            if self.cells[cell_name].low_y<=min_y:
                min_y=self.cells[cell_name].low_y
            if self.cells[cell_name].high_y>=max_y:
                max_y=self.cells[cell_name].high_y

        self.low_y = min_y
        self.left_x = min_x
        self.high_y = max_y
        self.right_x = max_x

        self.width = self.right_x - self.left_x
        self.height = self.high_y - self.low_y

    def generate_benchmark_cells(self, file_parser: FParser):
        """
        Generates Cell instances inside Benchmark
        """

        cell_list = []
        cell_info= file_parser.read_cells()
        for cell_name in cell_info.keys():
            cell = Cell()
            cell.generate_cell(cell_info[cell_name], cell_name)
            self.cells[cell_name] = cell
            cell_list.append(cell)
        return cell_list

    def generate_benchmark_nets(self, file_parser: FParser, tmp_cells_list: list):
        """
        Generates all Nets
        """

        nets, nets_index = file_parser.read_nets()
        for _ in nets.keys():
            net = Net()
            net.generate_net(nets, tmp_cells_list, nets_index)
            self.nets[net.name] = net

    def generate_cells_connections(self):
        for n in self.nets.values():
            for c_name in n.cells:
                self.cells[c_name].nets[n.name] = n

    def generate_benchmark_rows(self, file_parser: FParser):
        """
        Generate Row instances inside Benchmark
        :param file_parser:
        :return:
        """

        rows = file_parser. read_rows()
        for row_name in rows.keys():
            row = Row()
            row.generate_row(rows[row_name])
            self.rows.append(row)

    def calculate_rows_number(self):
        self.num_rows = len(self.rows)

    def calculate_hpwl(self):
        for net in self.nets.keys():
            self.hpwl += self.nets[net].hpwl

    def recalculate_hpwl(self):
        # Saves time when you need to check hpwl after cells' movement
        self.hpwl = 0.0
        for net in self.nets.values():
            net.calculate_net_corners(self.cells)
            net.calculate_hpwl()
            self.hpwl += net.hpwl

    def generate_benchmark(self):
        """
        Generates a Benchmark instance with all its cells, nets and rows
        """

        file_parser = FParser(self.file_name)

        # 1. Generate Cells
        cells_list = self.generate_benchmark_cells(file_parser)
        # 2. Generate Nets
        # self.generate_benchmark_nets(file_parser, cells_list)
        # self.generate_cells_connections()
        # 3. Generate Rows
        self.generate_benchmark_rows(file_parser)
        self.calculate_rows_number()
        # 4. Calculate remaining attributes
        self.calculate_coreRegion_area()
        self.calculate_benchmark_coordinates()
        # # 5. Calculate hpwl
        # for net in self.nets.keys():
        #     self.nets[net].calculate_net_corners(self.cells)
        #     self.nets[net].calculate_hpwl()
        # # 6. Check if all terminal added previsously are pins or macros
        # for pin in self.pins.keys():
        #     if self.pins[pin].low_y > self.low_y and self.pins[pin].high_y < self.high_y \
        #             and self.pins[pin].left_x > self.left_x and self.pins[pin].right_x < self.right_x:
        #         self.pins.pop(pin)
        #     else:
        #         self.cells[pin].is_pin = True
        # self.calculate_hpwl()
    
    def print_info(self):
        print(len(self.cells))

    def setCellLocation(self,cellName:str,left_x:float,lower_y:float):
        # print(self.cells[cellName].left_x)
        self.cells[cellName].left_x=left_x
        self.cells[cellName].low_y=lower_y
        self.cells[cellName].calculate_high_y()
        self.cells[cellName].calculate_right_x()

