class Cell:
    """
    Cell class defines a cell/node object of a benchmark according to bookeshelf format
    """

    counter = -1
# cell: std cells and macors and terminals
    def __init__(self): 
        Cell.counter += 1

        # benchmark attributes
        self.name = None
        self.low_y = None
        self.left_x = None
        self.width = None
        self.height = None
        self.movetype = None  # Terminal or non-terminal/movable cells
        self.nets = {}
        self.pins={}

        # Calculated attributes
        self.high_y = None
        self.right_x = None

        self.id = Cell.counter

    def calculate_high_y(self):
        self.high_y = self.low_y + self.height

    def calculate_right_x(self):
        self.right_x = self.left_x + self.width

    def generate_cell(self, cell_info: list, name: str):
        """
        Custom cell constructor compatible to info given by file-parsing
        """

        self.name = name
        self.left_x = cell_info[0]
        self.low_y = cell_info[1]
        self.width = cell_info[2]
        self.height = cell_info[3]
        self.movetype = cell_info[4]

        self.calculate_high_y()
        self.calculate_right_x()
