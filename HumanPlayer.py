import random

import pygame

from Player import Player


class HumanPlayer(Player):
    def __init__(self, name,game):
        super().__init__(name,game)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.command_queue.append("left")
                elif event.key == pygame.K_RIGHT:
                    self.command_queue.append("right")
                elif event.key == pygame.K_UP:
                    self.command_queue.append("rotate")
                elif event.key == pygame.K_DOWN:
                    self.command_queue.append("drop")
                elif event.key == pygame.K_f:
                    possible_states = self.get_possible_states(self.game)
                    pick = random.choice(possible_states)
                    self.game.current_piece.x = pick[0]
                    self.game.current_piece.y = pick[1]
                    self.game.current_piece.rotation = pick[2]

    def update(self, update_time):
        self.handle_input()
        super().update(update_time)

