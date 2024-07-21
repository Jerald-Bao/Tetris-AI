import pygame

import HumanPlayer
from Game import Game


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
        self.command_queue = []

    def update(self):
        if len(self.command_queue) != 0:
            queued_commands = self.command_queue.pop()
            if queued_commands in self.commands:
                self.commands[queued_commands]()

