import Game
from AIPlayerBase import AIPlayerBase


class GreedyDFSPlayer(AIPlayerBase):

    def __init__(self, name, game, depth=2):
        """
        Initializes a GreedyDFSPlayer with the given name, game, and search depth.

        Args:
            name (str): The name of the player.
            game (Game): The game instance that the player is interacting with.
            depth (int): The depth of the search tree. Defaults to 2.
        """
        super().__init__(name, game)
        self.depth = depth

    def greedy_dfs(self, game, depth, state):
        """
        Executes the Greedy DFS algorithm to determine the best move.

        Args:
            game (Game): The game instance being evaluated.
            depth (int): The current depth in the search tree.
            state (tuple): The current state of the game (x, y, rotation).

        Returns:
            tuple: A tuple containing the evaluation score and the sequence of moves leading to that score.
        """
        if depth == 0 or game.check_lost(game.locked_positions):
            return self.evaluate_state(game), [state]

        max_eval = float('-inf')
        best_move = []
        for x, y, rotation in self.get_possible_states(game):
            game.push(x, y, rotation)
            eval, sequence = self.greedy_dfs(game, depth - 1, (x, y, rotation))
            game.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = sequence
        return max_eval, [state] + best_move

    def generate_command(self):
        """
        Generates the best move for the AI player using the Greedy DFS algorithm.

        Determines the optimal move based on the current state of the game and the predefined depth.
        Updates the player's choice with the best move and places the current piece accordingly.
        """
        best_score = float('-inf')
        best_move = None

        possible_states = self.get_possible_states(self.game)
        mock_game = self.game.copy()
        best_sequence = []
        for state in possible_states:
            mock_game.push(state[0], state[1], state[2])
            score, sequence = self.greedy_dfs(mock_game, self.depth, state)
            mock_game.pop()

            if score > best_score:
                best_score = score
                best_move = state
                best_sequence = sequence

        if best_move:
            self.choice = best_move
            self.place_current_piece(best_move)
            self.placing_piece = True

    def update(self, update_time):
        """
        Updates the AI player by processing game state changes and making decisions.

        Calls the base class's update method and processes the chosen move if available.

        Args:
            update_time (int): The time elapsed since the last update, used for timing control.
        """
        super().update(update_time)

    def debug_heuristic(self, sequence):
        """
        Debugs the heuristic evaluation by applying the given sequence of moves and printing the resulting score.

        Args:
            sequence (list): A list of states representing the sequence of moves to apply.
        """
        mock_game = self.game.copy()
        eval = 0
        for state in sequence:
            mock_game.push(state[0], state[1], state[2])
            eval = self.evaluate_state(mock_game)
        print(eval)
