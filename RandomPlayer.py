import random

import pygame

from AIPlayerBase import AIPlayerBase
from Piece import Piece
from Player import Player


class RandomPlayer(AIPlayerBase):

    def __init__(self, name, game):
        super().__init__(name, game)
        self.choice = None

    def generate_command(self):
        possible_states = self.get_possible_states(self.game)
        self.choice = random.choice(possible_states)
        self.placing_piece = True
        self.current_piece = self.game.current_piece
        self.place_current_piece(self.choice)
        print(self.choice)

    def update(self, update_time):
        if self.choice is not None:
            self.highlight()

        if not self.moving_piece and self.placing_piece:
            self.place_current_piece(self.choice)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    print("P")

        super().update(update_time)

    def highlight(self):
        if self.choice is not None:
            piece = Piece(self.choice[0], self.choice[1], self.game.current_piece.shape)
            piece.rotation = self.choice[2]
            for position in self.game.convert_shape_format(piece):
                if 0 <= position[1] < 20 and 0 <= position[0] < 10:
                    self.game.debug_grid[position[1]][position[0]] = (200, 10, 200)
