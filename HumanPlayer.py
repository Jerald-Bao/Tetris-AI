import random

import pygame

from Player import Player


class HumanPlayer(Player):
    
    def __init__(self, name, game):
        """
        Initializes a HumanPlayer with the given name and game.

        Args:
            name (str): The name of the player.
            game (Game): The game instance that the player is interacting with.
        """
        super().__init__(name,game)

    def handle_input(self):
        """
        Handles user input from the keyboard to control the game.

        Processes events from `pygame` to detect user actions, such as moving left, right,
        rotating the piece, or dropping the piece. It also handles quitting the game if
        the quit event is triggered.

        If the 'f' key is pressed, it randomly places the current piece to a new valid position.
        """
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
                elif event.key == pygame.K_f:
                    possible_states = self.get_possible_states(self.game)
                    pick = random.choice(possible_states)
                    self.game.current_piece.x = pick[0]
                    self.game.current_piece.y = pick[1]
                    self.game.current_piece.rotation = pick[2]

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.command_queue.append("drop")

    def update(self, update_time):
        """
        Updates the player's state by handling input and processing commands.

        Calls `handle_input` to process user input and then updates the player state
        using the base class's `update` method.

        Args:
            update_time (int): The time elapsed since the last update, used for timing control.
        """
        self.handle_input()
        super().update(update_time)

