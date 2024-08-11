import numpy as np
import pygame

from Game import Game
from Piece import Piece
from Player import Player


class AIPlayerBase(Player):
    """
    Base class for AI players in Tetris.

    Inherits from:
        Player: Base player class.

    Attributes:
        placing_piece (bool): Indicates whether the AI is currently placing a piece.
        current_piece (Piece): The piece currently being handled by the AI.
        command_interval (int): Interval for command updates (in milliseconds).
        command_time (int): Time elapsed since the last command was issued.
        moving_piece (bool): Indicates whether the AI is moving the piece.
        choice (tuple): The chosen position for placing the piece.
    """

    def __init__(self, name, game):
        """
        Initializes an AIPlayerBase instance.

        Args:
            name (str): Name of the player.
            game (Game): The game instance to control.
        """
        super().__init__(name, game)
        self.placing_piece = False
        self.current_piece = None
        self.command_interval = 100
        self.command_time = 0
        self.moving_piece = False
        self.choice = None

    def evaluate_state(self, game: Game):
        """
        Evaluates the state of the game and assigns a score based on various factors.

        Args:
            game (Game): The current game instance.

        Returns:
            int: The score representing the desirability of the game state.
        """
        score = 0

        # 1. number of cleared rows
        score += game.score * 6

        # 2. aggregate height
        heights = [0] * game.cols
        for x in range(game.cols):
            for y in range(game.rows):
                if not game.accepted_positions[x][y]:
                    heights[x] = game.rows - y
                    break
        aggregate_height = sum(heights)
        score -= aggregate_height * 1

        # 3. number of holes
        holes = 0
        for x in range(game.cols):
            for y in range(1,game.rows):
                if game.accepted_positions[x][y] and not game.accepted_positions[x][y-1]:
                    holes += 1
        score -= holes * 25

        # 4. bumpiness
        bumpiness = 0
        for i in range(len(heights) - 1):
            bumpiness += abs(heights[i] - heights[i + 1])
        score -= bumpiness * 2

        # 5. well sums
        well_sums = 0
        for x in range(1, len(heights) - 1):
            if heights[x - 1] > heights[x] and heights[x + 1] > heights[x]:
                well_sums += min(heights[x - 1], heights[x + 1]) - heights[x]
        if len(heights) > 1:
            well_sums += heights[1] - heights[0]
            well_sums += heights[-2] - heights[-1]
        score -= well_sums * 1

        return score
    
    def update(self, update_time):
        """
        Updates the AI player's state and handles piece placement and movement.

        Args:
            update_time (int): Time elapsed since the last update (in milliseconds).
        """
        if self.placing_piece:
            if self.current_piece != self.game.current_piece:
                self.placing_piece = False

        if not self.placing_piece:
            self.generate_command()

        if self.placing_piece and self.moving_piece:
            self.command_time += update_time
            if self.command_time > self.command_interval:
                self.command_time -= self.command_interval
                command = self.path_map[self.current_piece.x,
                                        self.current_piece.y,
                                        self.current_piece.rotation]
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
        """
        Generates the next command for the AI player.

        This method should be implemented by subclasses.
        """
        pass

    # use grass-fire algorithm to find all possible final position of a pieces.
    def get_possible_states(self, game):
        """
        Uses a grass-fire algorithm to find all possible final positions for the current piece.

        Args:
            game (Game): The current game instance.

        Returns:
            list of tuples: Each tuple represents a possible state (x, y, rotation) for the piece.
        """
        piece = Piece(game.current_piece.x, game.current_piece.y,
                      game.current_piece.shape)
        piece.rotation = game.current_piece.rotation
        orientation = len(piece.shape[1])

        accessible = np.zeros((game.cols + 5, game.rows + 5, orientation),
                              dtype=bool)
        # set the spawning point of the 'fire' to the piece's current location
        accessible[piece.x, piece.y, piece.rotation] = True
        validity = self.get_position_validity(game, piece)

        hasChange = True
        while hasChange:
            hasChange = False
            for i in range(-2, game.cols + 3):
                for j in range(0, game.rows + 5):
                    for rotation in range(orientation):
                        if not accessible[i, j,
                                          rotation] and validity[i, j,
                                                                 rotation]:
                            # Spread fire to adjacent grass cells
                            if i > -2 and accessible[i - 1, j, rotation]:
                                accessible[i, j, rotation] = True
                                hasChange = True
                            elif i < game.cols + 2 and accessible[i + 1, j,
                                                                  rotation]:
                                accessible[i, j, rotation] = True
                                hasChange = True
                            elif j < game.rows + 4 and accessible[i, j - 1,
                                                                  rotation]:
                                accessible[i, j, rotation] = True
                                hasChange = True
                            elif accessible[i, j, (rotation + 1) %
                                            orientation] or accessible[
                                                i, j, rotation - 1]:
                                accessible[i, j, rotation] = True
                                hasChange = True

        # next, select out possible final positions that has a ground support the piece
        possible_states = []
        for i in range(-2, game.cols + 3):
            for j in range(game.rows + 5):
                for rotation in range(orientation):
                    if accessible[i, j, rotation] and (
                            j == game.rows + 4
                            or not validity[i, j + 1, rotation]):
                        possible_states.append((i, j, rotation))

        # print(f"Possible states: {possible_states}")
        # print(f"Possible states: {len(possible_states)}")
        return possible_states

    def get_position_validity(self, game, piece):
        """
        Determines the validity of positions for a given piece.

        Args:
            game (Game): The current game instance.
            piece (Piece): The piece to check.

        Returns:
            np.ndarray: A boolean array indicating the validity of positions for the piece.
        """
        orientation = len(piece.shape[1])
        validity = np.zeros(
            (game.cols + 5, game.rows + 5, orientation),
            dtype=bool)
        for piece.x in range(-2, game.cols + 3):
            for piece.y in range(0, game.rows + 5):
                for piece.rotation in range(orientation):
                    if game.valid_space(piece):
                        validity[piece.x, piece.y, piece.rotation] = True
        return validity

    def place_current_piece(self, position):
        """
        Places the current piece at the given position and calculates the path for placement.

        Args:
            position (tuple): The target position (x, y, rotation) for placing the piece.
        """
        piece = Piece(self.game.current_piece.x, self.game.current_piece.y,
                      self.game.current_piece.shape)
        piece.rotation = self.game.current_piece.rotation
        orientation = len(piece.shape[1])
        dtype = np.dtype([('direction', 'S10'), ('distance', 'i4')])
        default_value = np.array([('unknown', 999)], dtype=dtype)
        directions = np.full(
            (self.game.cols + 5, self.game.rows + 5, orientation),
            default_value,
            dtype=dtype)
        # set the spawning point of the 'fire' to the piece's current location
        directions[piece.x, piece.y, piece.rotation] = np.array([('none', 0)],
                                                                dtype=dtype)

        validity = self.get_position_validity(self.game, piece)

        # use grassfire to calculate directions
        hasChange = True
        while hasChange:
            hasChange = False
            for i in range(-2, self.game.cols + 3):
                for j in range(0, self.game.rows + 5):
                    for rotation in range(orientation):
                        if validity[i, j, rotation]:
                            # Spread fire to adjacent grass cells
                            if i > -2 and directions[i - 1, j, rotation][
                                    "distance"] + 1 < directions[
                                        i, j, rotation]["distance"]:
                                directions[i, j,
                                           rotation]["distance"] = directions[
                                               i - 1, j,
                                               rotation]["distance"] + 1
                                directions[i, j,
                                           rotation]["direction"] = "left"
                                hasChange = True
                            elif i < self.game.cols + 2 and directions[i + 1, j, rotation]["distance"] + 1 < \
                                    directions[i, j, rotation]["distance"]:
                                directions[i, j,
                                           rotation]["distance"] = directions[
                                               i + 1, j,
                                               rotation]["distance"] + 1
                                directions[i, j,
                                           rotation]["direction"] = "right"
                                hasChange = True
                            elif directions[i, j, (rotation - 1) % orientation]["distance"] + 1 < \
                                    directions[i, j, rotation]["distance"]:
                                directions[
                                    i, j, rotation]["distance"] = directions[
                                        i, j, (rotation - 1) %
                                        orientation]["distance"] + 1
                                directions[i, j,
                                           rotation]["direction"] = "clockwise"
                                hasChange = True
                            elif (j < self.game.rows + 4 and not directions[i, j, rotation]["direction"] == b"up"
                                  and directions[i, j - 1, rotation]["distance"] < \
                                    directions[i, j, rotation]["distance"]):
                                directions[i, j,
                                           rotation]["distance"] = directions[
                                               i, j - 1,
                                               rotation]["distance"] + 1
                                directions[i, j, rotation]["direction"] = "up"
                                hasChange = True

        # backtrace to find path
        i = position[0]
        j = position[1]
        rotation = position[2]
        self.path_map = np.zeros(
            (self.game.cols + 5, self.game.rows + 5, orientation),
            dtype='U10')
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
                rotation = (rotation + 3) % orientation
                distance -= 1
                self.path_map[i, j, rotation] = 'rotate'
            if last_distance == distance:
                print("we lost")
                break
        self.placing_piece = True
        self.moving_piece = True
        self.current_piece = self.game.current_piece
        self.command_time = self.command_interval + 1

    def highlight(self):
        """
        Highlights the position on the game grid where the AI has chosen to place the current piece.

        If a choice has been made, this method creates a `Piece` object based on the choice and
        updates the `debug_grid` of the game to visually represent the piece's placement.

        The piece is colored with a distinct color (RGB: 200, 10, 200) to indicate the placement.

        The piece is highlighted only if its position is within the bounds of the grid (0 ≤ x < 10 and 0 ≤ y < 20).
        """
        if self.choice is not None:
            piece = Piece(self.choice[0], self.choice[1], self.game.current_piece.shape)
            piece.rotation = self.choice[2]
            for position in self.game.convert_shape_format(piece):
                if 0 <= position[1] < 20 and 0 <= position[0] < 10:
                    self.game.debug_grid[position[1]][position[0]] = (200, 10, 200)