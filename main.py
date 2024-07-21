import pygame
import random

from Game import Game
import Game as G
from HumanPlayer import HumanPlayer
from Player import Player

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS






def main():
    global grid

    game1 = Game()
    game2 = Game()
    game1.player = HumanPlayer("Dracula",game1)

    while game1.run:
        game1.update(win)
    G.draw_text_middle("You Lost", 40, (255,255,255), win)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        win.fill((0,0,0))
        G.draw_text_middle('Press any key to begin.', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


win = pygame.display.set_mode((G.s_width, G.s_height))
pygame.display.set_caption('Tetris')

main_menu()  # start game






