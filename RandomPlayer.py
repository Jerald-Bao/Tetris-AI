import random

import pygame

from AIPlayerBase import AIPlayerBase
from Piece import Piece
from Player import Player


class RandomPlayer(AIPlayerBase):

    def __init__(self, name, game):
        """
        Initializes a RandomPlayer with the given name and game instance.

        Args:
            name (str): The name of the player.
            game (Game): The game instance that the player is interacting with.
        """
        super().__init__(name, game)

    def generate_command(self):
        """
        Randomly selects a possible move from the available states and places the current piece accordingly.

        Chooses a random state from the list of possible states and updates the player's choice.
        Sets the flag for placing the piece and calls the method to place the piece in the game.
        """
        possible_states = self.get_possible_states(self.game)
        self.choice = random.choice(possible_states)
        self.placing_piece = True
        self.place_current_piece(self.choice)

    def update(self, update_time):
        """
        Updates the state of the RandomPlayer, processes events, and highlights the current piece if chosen.

        Args:
            update_time (int): The time elapsed since the last update, used for timing control.
        """
        # Just in case the event list blocks everything
        pygame.event.get()
        super().update(update_time)
        if self.choice is not None:
            self.highlight()


