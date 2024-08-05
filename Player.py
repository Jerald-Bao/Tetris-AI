import pygame

import HumanPlayer
from Game import Game
import numpy as np

from Piece import Piece


class Player:
    def __init__(self, name,game):
        self.name = name
        self.game = game
        self.commands = {
            "left": game.move_left,
            "right": game.move_right,
            "rotate": game.rotate_piece,
            "drop": game.drop_piece,
            "quit": game.quit
        }
        self.states_path_map = {}
        self.command_queue = []

    def update(self):
        if len(self.command_queue) != 0:
            queued_commands = self.command_queue.pop()
            if queued_commands in self.commands:
                self.commands[queued_commands]()

    # use grass-fire algorithm to find all possible final position of a pieces.
    def get_possible_states(self, game):
        piece = Piece(self.game.current_piece.x,self.game.current_piece.y,self.game.current_piece.shape)
        piece.rotation = self.game.current_piece.rotation

        accessible = np.zeros((game.cols + 5,game.rows + 5, 4), dtype=bool)
        # set the spawning point of the 'fire' to the piece's current location
        accessible[piece.x,piece.y,piece.rotation] = True
        validity = np.ones((game.cols + 5,game.rows + 5, 4), dtype=bool)
        for piece.x in range(-2, game.cols + 3):
            for piece.y in range(0, game.rows+5):
                for piece.rotation in range(4):
                    if not game.valid_space(piece):
                        validity[piece.x, piece.y, piece.rotation] = False

        hasChange = True
        while hasChange:
            hasChange = False
            for i in range(-2,game.cols + 3):
                for j in range(0, game.rows + 5):
                    for rotation in range(4):
                        if not accessible[i, j, rotation] and validity[i, j, rotation]:
                            # Spread fire to adjacent grass cells
                            if i > -2 and accessible[i - 1, j, rotation]:
                                accessible[i, j, rotation] = True
                                hasChange = True
                            elif i < game.cols + 2 and accessible[i + 1, j,rotation]:
                                accessible[i, j, rotation] = True
                                hasChange = True
                            elif j < game.rows + 4 and accessible[i, j - 1, rotation]:
                                accessible[i, j, rotation] = True
                                hasChange = True
                            elif accessible[i, j, (rotation + 1)//4] or accessible[i, j, rotation - 1]:
                                accessible[i, j, rotation] = True
                                hasChange = True

        # next, select out possible final positions that has a ground support the piece
        possible_states = []
        for i in range(-2, game.cols + 3):
            for j in range(game.rows+5):
                for rotation in range(4):
                    if accessible[i, j, rotation] and (j == game.rows +4 or not validity[i, j+1,rotation]):
                        possible_states.append((i,j,rotation))

        # print(f"Possible states: {len(possible_states)}")
        return possible_states



