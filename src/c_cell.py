class Cell:
    """
    Cell class defines a cell/node object of a benchmark according to bookeshelf format
    """

    counter = -1

    def __init__(self):
        Cell.counter += 1

        # benchmark attributes
        self.name = None
        self.low_y = None
        self.left_x = None
        self.width = None
        self.height = None
        self.movetype = None  # Terminal or non-terminal/movable cells
        self.is_pin = False
        self.nets = {}

        # Calculated attributes
        self.high_y = None
        self.right_x = None

        self.id = Cell.counter

    def calculate_high_y(self):
        self.high_y = self.low_y + self.height

    def calculate_right_x(self):
        self.right_x = self.left_x + self.width

    def generate_cell(self, tmp: list, name: str):
        """
        Custom cell constructor compatible to info given by file-parsing
        """

        self.name = name
        self.low_y = tmp[1]
        self.left_x = tmp[0]
        self.width = tmp[2]
        self.height = tmp[3]
        self.movetype = tmp[4]

        self.calculate_high_y()
        self.calculate_right_x()
