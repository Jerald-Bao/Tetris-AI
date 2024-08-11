import pygame.event

import Game
from AIPlayerBase import AIPlayerBase
from Piece import Piece
import random
from collections import defaultdict


class MonteCarloPlayer(AIPlayerBase):

    def __init__(self, name, game, simulations=100):
        super().__init__(name, game)
        self.simulations = simulations  # Number of simulations per move
        self.tree = defaultdict(lambda: {"score": 0, "visits": 0, "children": {}})

    def update(self, update_time):
        pygame.event.get()
        super().update(update_time)

    def generate_command(self):
        self.tree = defaultdict(lambda: {"score": 0, "visits": 0, "children": {}})
        root_state = self.get_game_state_key(self.game)
        best_move = self.mcts(root_state)
        self.placing_piece = True
        self.choice = best_move

    def mcts(self, root_state):
        self.expand(self.game, root_state)
        for _ in range(self.simulations):
            node = self.tree[root_state]
            # Selection
            state = self.select(node)
            # Expansion
            if state not in self.tree:
                self.expand(self.game, state)
            # Simulation
            score = self.simulate(self.game, state)
            # Backpropagation
            self.backpropagate(state, score)

        # Choose the best move based on the average score
        max_score = max(
            (self.tree[s]["score"] / self.tree[s]["visits"]) if self.tree[s]["visits"] > 0 else 0
            for s in self.tree[root_state]["children"]
        )
        best_states = [
        s for s in self.tree[root_state]["children"]
        if ((self.tree[s]["score"] / self.tree[s]["visits"])
            if self.tree[s]["visits"] > 0 else 0) == max_score
        ]
        return random.choice(best_states)

    def select(self, node):
        # Selection using UCT (Upper Confidence Bound for Trees)
        state = max(node["children"], key=lambda s: self.uct_value(s))
        return state

    def uct_value(self, state):
        """Compute the Upper Confidence Bound for Trees (UCT) value of a state."""
        if self.tree[state]["visits"] == 0:
            return float('inf')  # Favor unexplored states
        return (self.tree[state]["score"] / self.tree[state]["visits"]) + \
            2 * (2 * (self.tree[state]["visits"] ** 0.5) / (1 + self.tree[state]["visits"]))

    def expand(self, game, state):
        possible_states = self.get_possible_states_from_state(game, state)
        for child_state in possible_states:
            if child_state not in self.tree:
                self.tree[state]["children"][child_state] = {"score": 0, "visits": 0, "children": {}}

    def simulate(self, game: Game.Game, state):
        # Create a copy of the game to simulate
        simulated_game = game.copy()
        simulated_piece = Piece(state[0], state[1], self.game.current_piece.shape)
        simulated_piece.rotation = state[2]
        simulated_game.current_piece = simulated_piece

        # Place the piece
        while simulated_game.valid_space(simulated_piece):
            simulated_piece.y += 1
        simulated_piece.y -= 1  # Move back to the last valid position
        simulated_game.push(simulated_piece.x, simulated_piece.y, simulated_piece.rotation)

        # Run random rollouts
        score = 0
        simulation_depth = 20
        for depth in range(simulation_depth):
            possible_moves = self.get_possible_states(simulated_game)
            if not possible_moves:
                score -= 20000
                break
            x, y, rotation = random.choice(possible_moves)
            if simulated_game.push(x, y, rotation):
                score -= 20000
                break
            score += self.evaluate_state(simulated_game) + 4
        while not simulated_game.history:
            simulated_game.pop()

        return score

    def backpropagate(self, state, score):
        while state:
            self.tree[state]["visits"] += 1
            self.tree[state]["score"] += score
            state = self.get_parent_state(state)

    def get_game_state_key(self, game):
        """Generate a unique key representing the game state."""
        return game.current_piece.x, game.current_piece.y, game.current_piece.rotation

    def get_possible_states_from_state(self,game, state):
        """Generate possible states from a given state."""
        # current_piece = self.create_piece_from_state(game, state)
        return self.get_possible_states(game)
        # for rotation in range(len(current_piece.shape[1])):
        #     for x in range(-2, self.game.cols - 2):
        #         piece_copy = Piece(x, 0, current_piece.shape,rotation)
        #         if self.game.valid_space(piece_copy):
        #             possible_states.append((x, piece_copy.y, rotation))
        # return possible_states

    def create_piece_from_state(self,game, state):
        """Create a Piece object from a given state."""
        x, y, rotation = state
        piece = Piece(x, y, self.game.current_piece.shape)
        piece.rotation = rotation
        return game, piece

    def get_parent_state(self, state):
        """Determine the parent state for backpropagation."""
        # Implement based on your tree structure and state representation
        return None
