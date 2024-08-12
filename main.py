import pygame
import random

from Game import Game
import Game as G
from HumanPlayer import HumanPlayer
from MonteCarloPlayer import MonteCarloPlayer
from RandomPlayer import RandomPlayer
from Player import Player
from GreedyDFSPlayer import GreedyDFSPlayer
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


def main(difficulty):
    """
    Runs the main game loop for Tetris, initializing two game instances with 
    the same seed and different difficulty levels.

    Args:
        difficulty (int): The difficulty level selected by the player.

    Initializes:
        game1: HumanPlayer vs. AI Player with selected difficulty.
        game2: AI Player with the selected difficulty level.

    The function updates both games and displays them side by side on the screen.
    If either player loses, it displays "You Lost" on their respective screen.
    The game continues to run until both players lose.
    """
    global grid
    seed = random.randint(1, 1000)
    game1 = Game(seed)
    game2 = Game(seed)
    game1.player = HumanPlayer("Player", game1)
    if difficulty == 0:
        game2.player = GreedyDFSPlayer("Easy", game2, 0)
        game2.player.command_interval = 350
    elif difficulty == 1:
        game2.player = GreedyDFSPlayer("Advanced", game2, 1)
        game2.player.command_interval = 150
    elif difficulty == 2:
        game2.player = GreedyDFSPlayer("Nightmare", game2, 1)
        game2.player.command_interval = 100
    else:
        game2.player = MonteCarloPlayer("MCST", game2, 50)
        game2.player.command_interval = 150

    rect = pygame.Rect(0, 0, G.s_width, G.s_height)
    game1_surface = pygame.Surface(rect.size)
    game2_surface = pygame.Surface(rect.size)

    clock = pygame.time.Clock()
    while game1.run or game2.run:
        clock.tick()
        if not game1.run:
            game1_surface.fill((0, 0, 0))
            G.draw_text_middle("You Lost", 40, (255, 255, 255), game1_surface)
        else:
            game1.update(game1_surface, clock.get_rawtime())
        if not game2.run:
            game2_surface.fill((0, 0, 0))
            G.draw_text_middle("You Lost", 40, (255, 255, 255), game2_surface)
        else:
            game2.update(game2_surface, clock.get_rawtime())
        win.blit(game1_surface, (left_margin, top_margin))
        win.blit(game2_surface, (left_margin * 2 + G.s_width, top_margin))
        pygame.display.flip()

    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    """
    Displays the main menu for Tetris, allowing the player to select a difficulty level.

    The function renders a list of difficulty levels:
        0 - Easy
        1 - Advanced
        2 - Nightmare
        3 - Monte Carlo

    The player can navigate the menu using the up and down arrow keys, 
    and select a difficulty by pressing the Enter key.

    The selected difficulty level is then passed to the main game loop.
    """
    run = True
    selected_diff = 0
    difficulty_text = ["Easy", "Advanced", "Nightmare", "Monte Carlo"]
    while run:
        win.fill((0, 0, 0))

        for i in range(4):
            G.draw_text(difficulty_text[i], 60, (255, 255, 255), win,
                        G.s_width + left_margin - 200,
                        G.s_height / 2 - 100 + i * 80)
            if selected_diff == i:
                G.draw_text('·', 60, (255, 255, 255), win,
                            G.s_width + left_margin - 200 - 50,
                            G.s_height / 2 - 100 + i * 80)

        # G.draw_text_middle('Press any key to begin.', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_diff = (selected_diff - 1) % 4
                elif event.key == pygame.K_DOWN:
                    selected_diff = (selected_diff + 1) % 4
                elif event.key == pygame.K_RETURN:
                    win.fill((0, 0, 0))
                    main(selected_diff)

    pygame.quit()


win = pygame.display.set_mode((G.s_width * 2 + 2 * left_margin + middle_margin,
                               G.s_height + 2 * top_margin))
pygame.display.set_caption('Tetris')

main_menu()  # start game
