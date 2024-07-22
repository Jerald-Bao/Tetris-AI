import random

import pygame

from Player import Player


class RandomPlayer(Player):
    def __init__(self, name,game):
        super().__init__(name,game)

    def generate_command(self):
        ran = random.randint(0,10)
        if ran == 0:
            self.command_queue.append("left")
        elif ran == 1:
            self.command_queue.append("right")
        elif ran == 2:
            self.command_queue.append("rotate")
        if ran == 3:
            self.command_queue.append("drop")

    def update(self):
        self.generate_command()
        super().update()
