import random

import pygame

from AIPlayerBase import AIPlayerBase
from Piece import Piece
from Player import Player


class RandomPlayer(AIPlayerBase):

    def __init__(self, name, game):
        super().__init__(name, game)

    def generate_command(self):
        possible_states = self.get_possible_states(self.game)
        self.choice = random.choice(possible_states)
        self.placing_piece = True
        self.place_current_piece(self.choice)

    def update(self, update_time):
        # Just in case the event list blocks everything
        pygame.event.get()
        super().update(update_time)
        if self.choice is not None:
            self.highlight()


