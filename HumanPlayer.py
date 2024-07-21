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
                if event.key == pygame.K_DOWN:
                    self.command_queue.append("drop")

    def update(self):
        self.handle_input()
        super().update()
