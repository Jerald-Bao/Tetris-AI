from Player import Player


class MinimaxABPlayer(Player):

    def __init__(self, name, game, depth=3):
        super().__init__(name, game)
        self.depth = depth

    def evaluate_state(self, game):
        # heuristic function
        grid = game.grid
        score = 0

        # 1. number of cleared rows
        score += game.score * 10

        # 2. height
        max_height = 0
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if grid[x][y] != (0, 0, 0):
                    max_height = max(max_height, y)
        score -= max_height * 5

        return score

    def get_possible_states(self, game):
        possible_states = []
        original_piece = game.current_piece

        for rotation in range(len(original_piece.shape)
                              ):  # every shape has different ratation states
            for x in range(
                    -2, 3
            ):  # limit the horizontal movement range, could be changed
                piece_copy = original_piece.copy()
                piece_copy.rotation = rotation
                piece_copy.x += x

                if game.valid_space(piece_copy, game.grid):
                    piece_copy.y += 1
                    while game.valid_space(piece_copy, game.grid):
                        piece_copy.y += 1
                    piece_copy.y -= 1

                    new_game_state = game.copy()
                    new_game_state.current_piece = piece_copy
                    new_game_state.lock_piece()
                    possible_states.append((new_game_state, x, rotation))

        # print(f"Possible states: {len(possible_states)}")
        return possible_states

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.check_lost(game.locked_positions):
            return self.evaluate_state(game)

        if maximizing_player:
            max_eval = float('-inf')
            for state, x, rotation in self.get_possible_states(game):
                eval = self.minimax(state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for state, x, rotation in self.get_possible_states(game):
                eval = self.minimax(state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def generate_command(self):
        best_score = float('-inf')
        best_move = None

        for state, x, rotation in self.get_possible_states(self.game):
            score = self.minimax(state, self.depth, float('-inf'),
                                 float('inf'), False)
            if score > best_score:
                best_score = score
                best_move = (x, rotation)

        if best_move:
            x, rotation = best_move
            self.command_queue = []

            if rotation > 0:
                self.command_queue.extend(["rotate"] * rotation)

            if x < 0:
                self.command_queue.append("left")
            elif x > 0:
                self.command_queue.append("right")

            self.command_queue.append("drop")

    def update(self):
        self.generate_command()
        super().update()
