import random

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
    def __init__(self, seed):
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
        self.fall_speed = 1
        self.score = 0
        self.piece_dropped = False
        self.accepted_positions = None
        # self.seed = seed  # save seed
        # random.seed(seed)  # set random seed

    def update(self, win,update_time):

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
            if not (self.valid_space(self.current_piece)) and self.current_piece.y > 0:
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
            for pos in shape_pos:
                p = (pos[0], pos[1])
                self.locked_positions[p] = self.current_piece.color
            self.current_piece = self.next_pieces.pop(
                0)  # take next from next_pieces
            self.next_pieces.append(
                self.get_shape())  # add a new piece into next_pieces
            self.change_piece = False

            # call four times to check for multiple clear rows
            if self.clear_rows(self.grid, self.locked_positions):
                self.score += 10

        self.update_valid_positions()

        self.draw_window(win)
        self.draw_next_shapes(self.next_pieces, win)  # show next 5 pieces
        pygame.display.update()

        # Check if user lost
        if self.check_lost(self.locked_positions):
            self.run = False

    def create_grid(self, locked_positions=None):
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
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions

    def update_valid_positions(self):
        self.accepted_positions = [[(j, i) for j in range(10)
                                    if self.grid[i][j] == (0, 0, 0)] for i in range(20)]
        self.accepted_positions = [j for sub in self.accepted_positions for j in sub]

    def valid_space(self, shape: Piece):
        formatted = self.convert_shape_format(shape)

        for pos in formatted:
            if pos not in self.accepted_positions:
                if pos[1] > -1 or pos[0] < 0 or pos[0] >= self.cols:
                    return False

        return True

    def check_lost(self, positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False

    def get_shape(self):
        return Piece.Piece(5, 0, self.randomizer.choice(Piece.shapes))

    def draw_grid(self, surface, row, col):
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
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Shapes', 1, (255, 255, 255))

        sx = top_left_x + play_width + 30
        sy = top_left_y + play_height / 2 - 100
        surface.blit(label, (sx + 10, sy - 30))

        small_block_size = block_size // 2  # shrink size
        offset_y = 50  # gap between pieces (in y axis)

        for index, shape in enumerate(shapes):
            format = shape.shape[shape.rotation % len(shape.shape)]
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
        surface.fill((0, 0, 0))
        # Tetris Title
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('TETRIS', 1, (255, 255, 255))

        surface.blit(label, (top_left_x + play_width / 2 -
                             (label.get_width() / 2), 30))

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pygame.draw.rect(
                    surface, self.grid[i][j],
                    (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)
                if not self.debug_grid[i][j] == (0,0,0):
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
        self.current_piece.x -= 1
        if not self.valid_space(self.current_piece):
            self.current_piece.x += 1

    def move_right(self):
        self.current_piece.x += 1
        if not self.valid_space(self.current_piece):
            self.current_piece.x -= 1

    def rotate_piece(self):
        self.current_piece.rotation = self.current_piece.rotation + 1 % len(
            self.current_piece.shape)
        if not self.valid_space(self.current_piece):
            self.current_piece.rotation = self.current_piece.rotation - 1 % len(
                self.current_piece.shape)

    def drop_piece(self):
        self.current_piece.y += 1
        if not self.valid_space(self.current_piece):
            self.current_piece.y -= 1
        else:
            self.piece_dropped = True

    def quit(self):
        self.run = False
        pygame.display.quit()

    # def copy(self):
    #     # create a new Game
    #     new_game = Game(self.seed)

    #     # copy all we need
    #     new_game.grid = [row[:] for row in self.grid]
    #     new_game.current_piece = self.current_piece.copy()
    #     new_game.next_pieces = [piece.copy() for piece in self.next_pieces]
    #     new_game.score = self.score
    #     new_game.run = self.run

    #     return new_game

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
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label,
                 (top_left_x + play_width / 2 - (label.get_width() / 2),
                  top_left_y + play_height / 2 - label.get_height() / 2))


def draw_text(text, size, color, surface, x, y):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (x, y))
