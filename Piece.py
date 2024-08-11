"""
Defines Tetris shapes, their color codes, and their positional formats.

SHAPE FORMATS:
Each Tetris shape is represented as a list of string patterns for different rotations.
The shapes include:
- 'S': The S-shape piece.
- 'Z': The Z-shape piece.
- 'I': The I-shape piece.
- 'O': The O-shape piece.
- 'J': The J-shape piece.
- 'L': The L-shape piece.
- 'T': The T-shape piece.

SHAPES:
- `S`: List of rotations for the S-shaped piece.
- `Z`: List of rotations for the Z-shaped piece.
- `I`: List of rotations for the I-shaped piece.
- `O`: List of rotations for the O-shaped piece.
- `J`: List of rotations for the J-shaped piece.
- `L`: List of rotations for the L-shaped piece.
- `T`: List of rotations for the T-shaped piece.

SHAPE COLORS:
- A list of RGB color tuples representing colors for each shape.

FORMATS:
- A dictionary that maps each shape and rotation to a list of positions
  where the blocks are located in the grid. This is used for rendering the shapes.

Piece Class:
- The `Piece` class represents a single Tetris piece.
- `__init__(self, column, row, shape, rotation=0)`: Initializes a piece with a position, shape, and rotation.
- `copy(self)`: Creates and returns a copy of the current piece.

Attributes:
- `x`: The column position of the piece.
- `y`: The row position of the piece.
- `shape`: The shape of the piece (a list of string patterns).
- `color`: The color of the piece, determined by its shape.
- `rotation`: The rotation index of the piece (0-3).
"""

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
