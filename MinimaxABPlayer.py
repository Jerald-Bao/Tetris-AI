import Game
from AIPlayerBase import AIPlayerBase


class MinimaxABPlayer(AIPlayerBase):

    def __init__(self, name, game, depth=2):
        super().__init__(name, game)
        self.depth = depth



    def minimax(self, game, depth, alpha, beta, maximizing_player, state):
        if depth == 0 or game.check_lost(game.locked_positions):
            return self.evaluate_state(game),[state]

        # if maximizing_player:
        max_eval = float('-inf')
        best_move = []
        for x, y, rotation in self.get_possible_states(game):
            game.push(x, y, rotation)
            eval, sequence = self.minimax(game, depth - 1, alpha, beta, False,(x,y,rotation))
            game.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = sequence
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, [state] + best_move
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
        best_sequence = []
        for state in possible_states:
            mock_game.push(state[0],state[1],state[2])
            score, sequence = self.minimax(mock_game, self.depth, float('-inf'),
                                 float('inf'), False, state)
            mock_game.pop()

            if score > best_score:
                best_score = score
                best_move = state
                best_sequence = sequence

        if best_move:
            self.choice = best_move
            # print(best_sequence)
            # print(best_move)
            # print(best_score)
            self.place_current_piece(best_move)
            self.placing_piece = True

        #self.debug_heuristic(best_sequence)
            
    def update(self, update_time):
        super().update(update_time)
        # if self.choice is not None:
        #     self.highlight()

    def debug_heuristic(self, sequence):
        mock_game = self.game.copy()
        eval = 0
        for state in sequence:
            mock_game.push(state[0],state[1],state[2])
            eval = self.evaluate_state(mock_game)
        print(eval)


