"""
This module defines the Game class and related functions for a Tetris game
implementation using Pygame. The game involves a grid where pieces fall from
the top, and the player can move, rotate, and drop these pieces to fill rows.
Completed rows are cleared from the grid, and the player's score increases
accordingly.

The game mechanics include:
- A grid of 10 columns and 20 rows.
- Falling pieces represented by the Piece class.
- A random piece generator with a configurable seed for reproducibility.
- Game controls for moving, rotating, and dropping pieces.
- Checking for valid positions, row clearing, and game over conditions.
- Drawing the game window, grid, and next pieces using Pygame.

Classes:
    - Game: The main game class handling the game state, piece movement, and
      rendering.
      
Functions:
    - draw_text_middle(text, size, color, surface): Draws text centered in
      the game window.
    - draw_text(text, size, color, surface, x, y): Draws text at a specified
      position in the game window.
"""
import random

import numpy as np
import pygame
import Piece

s_width = 600
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per blo ck
play_offset = 120  # meaning 600 // 20 = 20 height per blo ck

block_size = 30

top_left_x = (s_width - play_width - play_offset) // 2
top_left_y = s_height - play_height


class Game:
    """
    A class to represent the Tetris game.

    Attributes:
        grid (list): A 2D list representing the current state of the game grid.
        debug_grid (list): A 2D list used for debugging the game grid.
        randomizer (random.Random): A random number generator with a set seed.
        cols (int): The number of columns in the game grid (default is 10).
        rows (int): The number of rows in the game grid (default is 20).
        locked_positions (dict): A dictionary storing the locked positions on
            the grid and their corresponding colors.
        change_piece (bool): A flag indicating whether to change the current piece.
        run (bool): A flag indicating whether the game is running.
        current_piece (Piece): The current piece that the player is controlling.
        next_pieces (list): A list of the next 5 pieces that will be played.
        player (AIPlayerBase): The player controlling the game.
        fall_time (int): A counter for the time since the last piece drop.
        level_time (int): A counter for the time since the level started.
        fall_speed (float): The speed at which the current piece falls.
        score (int): The player's current score.
        piece_dropped (bool): A flag indicating whether the current piece has been dropped.
        accepted_positions (np.ndarray): A 2D numpy array indicating valid positions on the grid.
        history (list): A list storing the game history for undo functionality.
    """
    def __init__(self, seed):
        """
        Initializes the Game object with a given seed for randomization.

        Args:
            seed (int): The seed for the random number generator.
        """
        self.grid = None
        self.debug_grid = None
        self.randomizer = random.Random(seed)
        self.cols = 10
        self.rows = 20
        self.locked_positions = {}
        self.create_grid(self.locked_positions)
        self.change_piece = False
        self.run = True
        self.current_piece = self.get_shape()
        self.next_pieces = [self.get_shape()
                            for _ in range(5)]  # next 5 pieces
        self.player = None
        self.fall_time = 0
        self.level_time = 0
        self.fall_speed = 0.27
        self.score = 0
        self.piece_dropped = False
        self.accepted_positions = None
        # self.seed = seed  # save seed
        # random.seed(seed)  # set random seed
        self.history = []  # keep track of the history

    def update(self, win, update_time):
        """
        Updates the game state, including the piece position, grid, and display.

        Args:
            win (pygame.Surface): The surface on which the game is drawn.
            update_time (int): The time elapsed since the last update.
        """
        self.grid = self.create_grid(self.locked_positions)
        self.debug_grid = self.create_grid()
        self.fall_time += update_time
        self.level_time += update_time

        # if self.level_time / 1000 > 4:
        #     level_time = 0
        #     if self.fall_speed > 0.15:
        #         self.fall_speed -= 0.005

        self.update_valid_positions()
        self.player.update(update_time)

        if self.piece_dropped:
            self.fall_time = 0
            self.piece_dropped = False

        # PIECE FALLING CODE
        if self.fall_time / 1000 >= self.fall_speed:
            self.fall_time = 0
            self.current_piece.y += 1
            if not (self.valid_space(
                    self.current_piece)) and self.current_piece.y > 0:
                self.current_piece.y -= 1
                self.change_piece = True

        shape_pos = self.convert_shape_format(self.current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                self.grid[y][x] = self.current_piece.color

        # IF PIECE HIT GROUND
        if self.change_piece:
            self.update_piece(shape_pos, True)
            self.change_piece = False


        self.update_valid_positions()

        self.draw_window(win)
        self.draw_next_shapes(self.next_pieces, win)  # show next 5 pieces
        pygame.display.update()

        # Check if user lost
        if self.check_lost(self.locked_positions):
            self.run = False

    def update_piece(self,shape_pos, generate_new_piece = False):
        """
        Locks the current piece's position on the grid and optionally generates a new piece.

        Args:
            shape_pos (list): The positions of the piece to lock on the grid.
            generate_new_piece (bool): Whether to generate a new piece after locking the current one.
        """
        for pos in shape_pos:
            p = (pos[0], pos[1])
            self.locked_positions[p] = self.current_piece.color
        self.current_piece = self.next_pieces.pop(
            0)  # take next from next_pieces
        if generate_new_piece:
            self.next_pieces.append(
                self.get_shape())  # add a new piece into next_pieces

        # call four times to check for multiple clear rows
        if self.clear_rows(self.grid, self.locked_positions):
            self.score += 10

    def create_grid(self, locked_positions=None):
        """
        Creates a grid based on the current locked positions.

        Args:
            locked_positions (dict): A dictionary of positions and colors representing locked pieces.

        Returns:
            list: A 2D list representing the grid with locked positions.
        """
        if locked_positions is None:
            locked_positions = {}
        grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j, i) in locked_positions:
                    c = locked_positions[(j, i)]
                    grid[i][j] = c
        return grid

    def convert_shape_format(self, shape: Piece):
        """
        Converts the shape's format to a list of grid positions.

        Args:
            shape (Piece): The piece to convert.

        Returns:
            list: A list of tuples representing the positions of the shape on the grid.
        """
        positions = Piece.formats[(shape.shape[0],shape.rotation)].copy()
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] + shape.x - 2, pos[1] + shape.y - 4)

        # print(f"Converted shape positions: {positions}")  # debug print
        return positions

    def update_valid_positions(self):
        """
        Updates the accepted positions on the grid based on locked positions.
        """
        self.accepted_positions = np.ones((self.cols,self.rows), dtype=bool)
        for i in self.locked_positions:
            self.accepted_positions[i[0],i[1]] = False

    def valid_space(self, shape: Piece):
        """
        Checks if the current piece is in a valid position on the grid.

        Args:
            shape (Piece): The piece to check.

        Returns:
            bool: True if the piece is in a valid position, False otherwise.
        """
        formatted = self.convert_shape_format(shape)
        # print(f"Formatted positions: {formatted}")
        # print(f"Accepted positions: {self.accepted_positions}")

        for pos in formatted:
            if pos[0] < 0 or pos[0] >= self.cols or pos[1] >= self.rows:
                return False
            elif pos[1] > 0 and not self.accepted_positions[pos[0],pos[1]]:
                return False

        return True

    def check_lost(self, positions):
        """
        Checks if the player has lost the game.

        Args:
            positions (dict): The locked positions on the grid.

        Returns:
            bool: True if the game is lost, False otherwise.
        """
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False

    def get_shape(self):
        """
        Returns a new random piece.

        Returns:
            Piece: A new randomly generated piece.
        """
        return Piece.Piece(5, 0, Piece.shape_list[self.randomizer.randint(0,len(Piece.shapes)-1)])

    def draw_grid(self, surface, row, col):
        """
        Draws the grid lines on the game surface.

        Args:
            surface (pygame.Surface): The surface on which to draw the grid.
            row (int): The number of rows in the grid.
            col (int): The number of columns in the grid.
        """
        sx = top_left_x
        sy = top_left_y
        for i in range(row):
            pygame.draw.line(
                surface, (128, 128, 128), (sx, sy + i * 30),
                (sx + play_width, sy + i * 30))  # horizontal lines
            for j in range(col):
                pygame.draw.line(
                    surface, (128, 128, 128), (sx + j * 30, sy),
                    (sx + j * 30, sy + play_height))  # vertical lines

    def clear_rows(self, grid, locked):
        """
        Clears any full rows from the grid and shifts down the rows above.

        Args:
            grid (list): The current game grid.
            locked (dict): The locked positions on the grid.

        Returns:
            int: The number of rows cleared.
        """
        # need to see if row is clear the shift every other row above down one

        inc = 0
        ind = 0
        for i in range(len(grid) - 1, -1, -1):
            row = grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                # add positions to remove from locked
                ind = i
                for j in range(len(row)):
                    try:
                        del locked[(j, i)]
                    except:
                        continue
        if inc > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)
            if inc == 1:
                self.score += 10
            elif inc == 2:
                self.score += 25
            elif inc == 3:
                self.score += 45
            elif inc == 4:
                self.score += 70

    def draw_next_shapes(self, shapes, surface):
        """
        Draws the next shapes to be played on the side of the game window.

        Args:
            shapes (list): A list of the next pieces to be played.
            surface (pygame.Surface): The surface on which to draw the shapes.
        """
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Shapes', 1, (255, 255, 255))

        sx = top_left_x + play_width + 30
        sy = top_left_y + play_height / 2 - 100
        surface.blit(label, (sx + 10, sy - 30))

        small_block_size = block_size // 2  # shrink size
        offset_y = 50  # gap between pieces (in y axis)

        for index, shape in enumerate(shapes):
            format = shape.shape[1][shape.rotation % len(shape.shape[1])]
            shape_sy = sy + index * offset_y  # adjust each shape's y position according to index

            for i, line in enumerate(format):
                row = list(line)
                for j, column in enumerate(row):
                    if column == '0':
                        pygame.draw.rect(surface, shape.color,
                                         (sx + j * small_block_size,
                                          shape_sy + i * small_block_size,
                                          small_block_size, small_block_size),
                                         0)

    def draw_window(self, surface):
        """
        Draws the main game window, including the grid and current piece.

        Args:
            surface (pygame.Surface): The surface on which to draw the game.
        """
        surface.fill((0, 0, 0))
        # Tetris Title
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render(self.player.name, 1, (255, 255, 255))

        surface.blit(label, (top_left_x + play_width / 2 -
                             (label.get_width() / 2), 30))

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pygame.draw.rect(
                    surface, self.grid[i][j],
                    (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)

                if not self.debug_grid[i][j] == (0, 0, 0):
                    pygame.draw.rect(
                        surface, self.debug_grid[i][j],
                        (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)

        # draw grid and border
        self.draw_grid(surface, 20, 10)
        pygame.draw.rect(surface, (255, 0, 0),
                         (top_left_x, top_left_y, play_width, play_height), 5)
        # pygame.display.update()
        draw_text(f"score: {self.score}", 20, (255, 255, 255), surface, 20, 20)

    def move_left(self):
        """
        Moves the current piece one position to the left if possible.
        """
        self.current_piece.x -= 1
        if not self.valid_space(self.current_piece):
            self.current_piece.x += 1

    def move_right(self):
        """
        Moves the current piece one position to the right if possible.
        """
        self.current_piece.x += 1
        if not self.valid_space(self.current_piece):
            self.current_piece.x -= 1

    def rotate_piece(self):
        """
        Rotates the current piece clockwise if the new position is valid.
        """
        self.current_piece.rotation = (self.current_piece.rotation + 1) % len(
            self.current_piece.shape[1])
        if not self.valid_space(self.current_piece):
            self.current_piece.rotation = self.current_piece.rotation - 1 % len(
                self.current_piece.shape[1])

    def drop_piece(self):
        """
        Drops the current piece by one position if possible.
        """
        self.current_piece.y += 1
        if not self.valid_space(self.current_piece):
            self.current_piece.y -= 1
        else:
            self.piece_dropped = True

    def push(self, x, y, rotation):
        """
        Places the current piece on the grid and updates the game state.

        Args:
            x (int): The x-coordinate of the piece.
            y (int): The y-coordinate of the piece.
            rotation (int): The rotation state of the piece.

        Returns:
            bool: True if the player has lost after the move, False otherwise.
        """
        self.history.append({
            'locked_positions':
            self.locked_positions.copy(),
            'current_piece': (self.current_piece.x, self.current_piece.y, self.current_piece.shape,
                              self.current_piece.rotation)
        })
        shape_pos = self.convert_shape_format(Piece.Piece(x,y,self.current_piece.shape,rotation))

        # Add the piece to the grid
        self.update_piece(shape_pos)
        if not self.next_pieces:
            self.next_pieces.append(self.get_shape())
        self.update_valid_positions()
        # self.create_grid(self.locked_positions)
        return self.check_lost(self.locked_positions)

    def pop(self):
        """
        Reverts the game state to the previous move.

        Returns:
            Game: The game instance after undoing the last move.
        """
        if not self.history:
            return self  # no action to undo

        # restore the previous state
        last_state = self.history.pop()
        self.locked_positions = last_state['locked_positions']

        self.next_pieces.insert(0,self.current_piece.copy())

        self.current_piece.x, self.current_piece.y,self.current_piece.shape, self.current_piece.rotation = last_state[
            'current_piece']
        # self.grid = self.create_grid(self.locked_positions)
        self.update_valid_positions()

        return self

    def quit(self):
        """
        Stops the game and quits the Pygame display.
        """
        self.run = False
        pygame.display.quit()

    def copy(self):
        """
        Creates a copy of the current game state.

        Returns:
            Game: A new Game instance with the same state as the current game.
        """
        # create a new Game
        new_game = Game(0)

        # copy all we need
        new_game.grid = [row[:] for row in self.grid]
        new_game.current_piece = self.current_piece.copy()
        new_game.next_pieces = [piece.copy() for piece in self.next_pieces]
        new_game.score = self.score
        new_game.run = self.run
        new_game.locked_positions = self.locked_positions.copy()
        new_game.create_grid(new_game.locked_positions)
        new_game.update_valid_positions()

        return new_game

    # def lock_piece(self):
    #     shape_pos = self.convert_shape_format(self.current_piece)
    #     # lock current piece's position to locked_positions
    #     for pos in shape_pos:
    #         p = (pos[0], pos[1])
    #         self.locked_positions[p] = self.current_piece.color

    #     # add points if rows cleared
    #     rows_cleared = self.clear_rows(self.grid, self.locked_positions)
    #     if rows_cleared:
    #         self.score += 10 * rows_cleared  # according to evaluate_state()

    #     # get next piece
    #     self.current_piece = self.next_pieces.pop(0)
    #     self.next_pieces.append(self.get_shape())

    #     if self.check_lost(self.locked_positions):
    #         self.run = False


def draw_text_middle(text, size, color, surface):
    """
    Draws the given text centered in the middle of the game window.

    Args:
        text (str): The text to display.
        size (int): The font size of the text.
        color (tuple): The color of the text in RGB format.
        surface (pygame.Surface): The surface on which to draw the text.
    """
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label,
                 (top_left_x + play_width / 2 - (label.get_width() / 2),
                  top_left_y + play_height / 2 - label.get_height() / 2))


def draw_text(text, size, color, surface, x, y):
    """
    Draws the given text at the specified position on the surface.

    Args:
        text (str): The text to display.
        size (int): The font size of the text.
        color (tuple): The color of the text in RGB format.
        surface (pygame.Surface): The surface on which to draw the text.
        x (int): The x-coordinate of the position where the text will be drawn.
        y (int): The y-coordinate of the position where the text will be drawn.
    """
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (x, y))
