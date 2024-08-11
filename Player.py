import pygame

from Game import Game
import numpy as np

from Piece import Piece


class Player:
    """
    Represents a player in the Tetris game. Handles player actions such as moving, rotating, dropping pieces, and quitting the game.

    Attributes:
        name (str): The name of the player.
        game (Game): The current game instance associated with the player.
        commands (dict): A dictionary mapping command strings to game methods.
        states_path_map (dict): A dictionary to store state paths, primarily for AI or advanced gameplay.
        command_queue (list): A queue of commands to be executed in the game.
    """
    def __init__(self, name,game):
        """
        Initializes the Player with a name and a game instance.

        Args:
            name (str): The name of the player.
            game (Game): The game instance that the player is controlling.
        """
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

    def update(self, update_time):
        """
        Processes the next command in the command queue and executes it in the game.

        Args:
            update_time (int): The time passed since the last update, typically used for time-based actions.
        """
        if len(self.command_queue) != 0:
            queued_commands = self.command_queue.pop()
            if queued_commands in self.commands:
                self.commands[queued_commands]()


