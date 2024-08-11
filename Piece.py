# SHAPE FORMATS

S = [['.....', '.....', '..00.', '.00..', '.....'],
     ['.....', '..0..', '..00.', '...0.', '.....']]

Z = [['.....', '.....', '.00..', '..00.', '.....'],
     ['.....', '..0..', '.00..', '.0...', '.....']]

I = [['..0..', '..0..', '..0..', '..0..', '.....'],
     ['.....', '0000.', '.....', '.....', '.....']]

O = [['.....', '.....', '.00..', '.00..', '.....']]

J = [['.....', '.0...', '.000.', '.....', '.....'],
     ['.....', '..00.', '..0..', '..0..', '.....'],
     ['.....', '.....', '.000.', '...0.', '.....'],
     ['.....', '..0..', '..0..', '.00..', '.....']]

L = [['.....', '...0.', '.000.', '.....', '.....'],
     ['.....', '..0..', '..0..', '..00.', '.....'],
     ['.....', '.....', '.000.', '.0...', '.....'],
     ['.....', '.00..', '..0..', '..0..', '.....']]

T = [['.....', '..0..', '.000.', '.....', '.....'],
     ['.....', '..0..', '..00.', '..0..', '.....'],
     ['.....', '.....', '.000.', '..0..', '.....'],
     ['.....', '..0..', '.00..', '..0..', '.....']]

shapes = {'S':S, 'Z':Z, 'I':I, 'O':O, 'J':J, 'L':L,'T':T}
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0),
                (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape
formats = {}
for shape in shapes.items():
    for rotation in range(len(shape[1])):
        positions = []
        for i, line in enumerate(shape[1][rotation]):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((j, i))
        formats[(shape[0],rotation)] = positions

shape_list = list(shapes.items())
class Piece(object):
    def __init__(self, column, row, shape, rotation=0):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shape_list.index(shape)]
        self.rotation = rotation  # number from 0-3


    def copy(self):
        new_piece = Piece(self.x, self.y, self.shape,self.rotation)
        return new_piece
