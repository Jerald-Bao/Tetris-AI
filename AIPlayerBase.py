import numpy as np

from Piece import Piece
from Player import Player


class AIPlayerBase(Player):
    def __init__(self, name, game):
        super().__init__(name, game)
        self.placing_piece = False
        self.current_piece = None
        self.command_interval = 100
        self.command_time = 0
        self.moving_piece = False
        self.choice = None

    def update(self, update_time):
        if self.placing_piece:
            if self.current_piece != self.game.current_piece:
                self.placing_piece = False

        if not self.placing_piece:
            self.generate_command()

        if self.placing_piece and self.moving_piece:
            self.command_time += update_time
            if self.command_time > self.command_interval:
                self.command_time -= self.command_interval
                command = self.path_map[self.current_piece.x, self.current_piece.y, self.current_piece.rotation]
                if not command == '':
                    self.command_queue.append(command)
                    #print(f"add command {command}")
                else:
                    self.moving_piece = False
                    #print("recalculate path")

        if not self.moving_piece and self.placing_piece:
            self.place_current_piece(self.choice)

        super().update(update_time)

    def generate_command(self):
        pass

    # use grass-fire algorithm to find all possible final position of a pieces.
    def get_possible_states(self, game):
        piece = Piece(game.current_piece.x, game.current_piece.y, game.current_piece.shape)
        piece.rotation = game.current_piece.rotation

        accessible = np.zeros((game.cols + 5, game.rows + 5, len(piece.shape)), dtype=bool)
        # set the spawning point of the 'fire' to the piece's current location
        accessible[piece.x, piece.y, piece.rotation] = True
        validity = self.get_position_validity(piece)

        hasChange = True
        while hasChange:
            hasChange = False
            for i in range(-2, game.cols + 3):
                for j in range(0, game.rows + 5):
                    for rotation in range(len(piece.shape)):
                        if not accessible[i, j, rotation] and validity[i, j, rotation]:
                            # Spread fire to adjacent grass cells
                            if i > -2 and accessible[i - 1, j, rotation]:
                                accessible[i, j, rotation] = True
                                hasChange = True
                            elif i < game.cols + 2 and accessible[i + 1, j, rotation]:
                                accessible[i, j, rotation] = True
                                hasChange = True
                            elif j < game.rows + 4 and accessible[i, j - 1, rotation]:
                                accessible[i, j, rotation] = True
                                hasChange = True
                            elif accessible[i, j, (rotation + 1) % len(piece.shape)] or accessible[i, j, rotation - 1]:
                                accessible[i, j, rotation] = True
                                hasChange = True

        # next, select out possible final positions that has a ground support the piece
        possible_states = []
        for i in range(-2, game.cols + 3):
            for j in range(game.rows + 5):
                for rotation in range(len(piece.shape)):
                    if accessible[i, j, rotation] and (j == game.rows + 4 or not validity[i, j + 1, rotation]):
                        possible_states.append((i, j, rotation))

        # print(f"Possible states: {len(possible_states)}")
        return possible_states

    def get_position_validity(self, piece):
        validity = np.zeros((self.game.cols + 5, self.game.rows + 5, len(piece.shape)), dtype=bool)
        for piece.x in range(-2, self.game.cols + 3):
            for piece.y in range(0, self.game.rows + 5):
                for piece.rotation in range(len(piece.shape)):
                    if self.game.valid_space(piece):
                        validity[piece.x, piece.y, piece.rotation] = True
        return validity

    def place_current_piece(self, position):
        piece = Piece(self.game.current_piece.x, self.game.current_piece.y, self.game.current_piece.shape)
        piece.rotation = self.game.current_piece.rotation
        dtype = np.dtype([('direction', 'S10'), ('distance', 'i4')])
        default_value = np.array([('unknown', 999)], dtype=dtype)
        directions = np.full((self.game.cols + 5, self.game.rows + 5, len(piece.shape)), default_value, dtype=dtype)
        # set the spawning point of the 'fire' to the piece's current location
        directions[piece.x, piece.y, piece.rotation] = np.array([('none', 0)], dtype=dtype)

        validity = self.get_position_validity(piece)

        # use grassfire to calculate directions
        hasChange = True
        while hasChange:
            hasChange = False
            for i in range(-2, self.game.cols + 3):
                for j in range(0, self.game.rows + 5):
                    for rotation in range(len(piece.shape)):
                        if validity[i, j, rotation]:
                            # Spread fire to adjacent grass cells
                            if i > -2 and directions[i - 1, j, rotation]["distance"] + 1 < directions[i, j, rotation][
                                "distance"]:
                                directions[i, j, rotation]["distance"] = directions[i - 1, j, rotation]["distance"] + 1
                                directions[i, j, rotation]["direction"] = "left"
                                hasChange = True
                            elif i < self.game.cols + 2 and directions[i + 1, j, rotation]["distance"] + 1 < \
                                    directions[i, j, rotation]["distance"]:
                                directions[i, j, rotation]["distance"] = directions[i + 1, j, rotation]["distance"] + 1
                                directions[i, j, rotation]["direction"] = "right"
                                hasChange = True
                            elif directions[i, j, (rotation - 1) % len(piece.shape)]["distance"] + 1 < \
                                    directions[i, j, rotation]["distance"]:
                                directions[i, j, rotation]["distance"] = directions[i, j, (rotation - 1) % len(piece.shape)][
                                                                             "distance"] + 1
                                directions[i, j, rotation]["direction"] = "clockwise"
                                hasChange = True
                            elif (j < self.game.rows + 4 and not directions[i, j, rotation]["direction"] == b"up"
                                  and directions[i, j - 1, rotation]["distance"] < \
                                    directions[i, j, rotation]["distance"]):
                                directions[i, j, rotation]["distance"] = directions[i, j - 1, rotation]["distance"] + 1
                                directions[i, j, rotation]["direction"] = "up"
                                hasChange = True

        # backtrace to find path
        i = position[0]
        j = position[1]
        rotation = position[2]
        self.path_map = np.zeros((self.game.cols + 5, self.game.rows + 5, len(piece.shape)), dtype='U10')
        distance = directions[i, j, rotation]["distance"]
        last_distance = distance
        while not directions[i, j, rotation]["direction"] == b"none":
            # Spread fire to adjacent grass cells
            if directions[i, j, rotation]["direction"] == b"left":
                i -= 1
                distance -= 1
                self.path_map[i, j, rotation] = "right"
            elif directions[i, j, rotation]["direction"] == b"right":
                i += 1
                distance -= 1
                self.path_map[i, j, rotation] = 'left'
            elif directions[i, j, rotation]["direction"] == b"up":
                j -= 1
                distance -= 1
                self.path_map[i, j, rotation] = 'drop'
            elif directions[i, j, rotation]["direction"] == b"clockwise":
                rotation = (rotation + 3) % len(piece.shape)
                distance -= 1
                self.path_map[i, j, rotation] = 'rotate'
            if last_distance == distance:
                print("we lost")
                break
        self.placing_piece = True
        self.moving_piece = True
        self.current_piece = self.game.current_piece
