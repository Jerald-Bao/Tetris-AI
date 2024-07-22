import pygame
import random

from Game import Game
import Game as G
from HumanPlayer import HumanPlayer
from RandomPlayer import RandomPlayer
from Player import Player

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS

middle_margin = 20
top_margin = 20
left_margin = 20


def main():
    global grid
    seed = random.randint(0,100000)
    game1 = Game(seed)
    game2 = Game(seed)
    game1.player = HumanPlayer("Dracula",game1)
    game2.player = RandomPlayer("Random",game2)
    rect = pygame.Rect(0, 0, G.s_width, G.s_height)
    game1_surface = pygame.Surface(rect.size)
    game2_surface = pygame.Surface(rect.size)

#game2_surface = pygame.Surface(rect.size)
#    game2_surface.blit(win, (left_margin * 2 + G.s_width, top_margin), rect)

    while game1.run or game2.run:
        if not game1.run:
            game1_surface.fill((0,0,0))
            G.draw_text_middle("You Lost", 40, (255,255,255), game1_surface)
        else:
            game1.update(game1_surface)
        if not game2.run:
            game2_surface.fill((0,0,0))
            G.draw_text_middle("You Lost", 40, (255,255,255), game2_surface)
        else:
            game2.update(game2_surface)
        win.blit(game1_surface, (left_margin, top_margin))
        win.blit(game2_surface, (left_margin * 2 + G.s_width, top_margin))
        pygame.display.flip()

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


win = pygame.display.set_mode((G.s_width * 2 + 2 * left_margin + middle_margin, G.s_height + 2 * top_margin))
pygame.display.set_caption('Tetris')

main_menu()  # start game






