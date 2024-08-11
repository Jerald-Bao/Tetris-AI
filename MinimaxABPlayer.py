import Game
from AIPlayerBase import AIPlayerBase


class MinimaxABPlayer(AIPlayerBase):

    def __init__(self, name, game, depth=2):
        super().__init__(name, game)
        self.depth = depth

    def evaluate_state(self, game: Game.Game):
        grid = game.grid
        score = 0

        # 1. number of cleared rows
        score += game.score * 10

        # 2. aggregate height
        heights = [0] * game.cols
        for x in range(game.cols):
            for y in range(game.rows):
                if not game.accepted_positions[x][y]:
                    heights[x] = game.rows - y
                    break
        aggregate_height = sum(heights)
        score -= aggregate_height * 1

        # 3. number of holes
        holes = 0
        for x in range(game.cols):
            block_found = False
            for y in range(game.rows):
                if not game.accepted_positions[x][y]:
                    block_found = True
                elif block_found:
                    holes += 1
        score -= holes * 5

        # 4. bumpiness
        bumpiness = 0
        for i in range(len(heights) - 1):
            bumpiness += abs(heights[i] - heights[i + 1])
        score -= bumpiness * 1

        # 5. well sums
        well_sums = 0
        for x in range(1, len(heights) - 1):
            if heights[x - 1] > heights[x] and heights[x + 1] > heights[x]:
                well_sums += min(heights[x - 1], heights[x + 1]) - heights[x]
        if len(heights) > 1:
            well_sums += heights[1] - heights[0]
            well_sums += heights[-2] - heights[-1]
        score -= well_sums * 1

        return score

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.check_lost(game.locked_positions):
            return self.evaluate_state(game)

        # if maximizing_player:
        max_eval = float('-inf')
        for x, y, rotation in self.get_possible_states(game):
            game.push(x, y, rotation)
            eval = self.minimax(game, depth - 1, alpha, beta, False)
            game.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
        # else:
        #     min_eval = float('inf')
        #     for x, y, rotation in self.get_possible_states(game):
        #         game.push(x, y, rotation)
        #         eval = self.minimax(game, depth - 1, alpha, beta, True)
        #         game.pop()
        #         min_eval = min(min_eval, eval)
        #         beta = min(beta, eval)
        #         if beta <= alpha:
        #             break
        #     return min_eval

    def generate_command(self):
        best_score = float('-inf')
        best_move = None

        possible_states = self.get_possible_states(self.game)
        mock_game = self.game.copy()
        for state in possible_states:
            mock_game.push(state[0],state[1],state[2])
            score = self.minimax(mock_game, self.depth, float('-inf'),
                                 float('inf'), False)
            mock_game.pop()

            if score > best_score:
                best_score = score
                best_move = state

        if best_move:
            self.choice = best_move
            print(best_score)
            self.place_current_piece(best_move)
            self.placing_piece = True
            
    def update(self, update_time):
        super().update(update_time)
        if self.choice is not None:
            self.highlight()
