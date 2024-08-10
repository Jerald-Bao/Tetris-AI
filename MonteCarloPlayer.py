<<<<<<< Updated upstream
from Player import Player
import random

class MonteCarloPlayer(Player):
    
    def __init__(self, name, game, simulations=100):
        super().__init__(name, game)
        self.simulations = simulations

    def simulate_random_play(self, game):
        simulation_game = game.copy()
        while not simulation_game.check_lost(simulation_game.locked_positions):
            possible_states = self.get_possible_states(simulation_game)
            if not possible_states:
                break
            state, x, rotation = random.choice(possible_states)
            simulation_game = state
        return simulation_game.score

    def get_possible_states(self, game):
        possible_states = []
        original_piece = game.current_piece

        for rotation in range(len(original_piece.shape)):
            for x in range(-2, 3):
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

        return possible_states

    def generate_command(self):
        best_score = float('-inf')
        best_move = None

        for state, x, rotation in self.get_possible_states(self.game):
            total_score = 0
            for _ in range(self.simulations):
                score = self.simulate_random_play(state)
                total_score += score
            average_score = total_score / self.simulations

            if average_score > best_score:
                best_score = average_score
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
=======
from AIPlayerBase import AIPlayerBase
from Piece import Piece
import random

class MonteCarloPlayer(AIPlayerBase):

    def __init__(self, name, game, simulations=100):
        super().__init__(name, game)
        self.simulations = simulations  # Number of simulations per move

    def generate_command(self):
        possible_states = self.get_possible_states(self.game)
        best_score = -float('inf')
        best_move = None

        for state in possible_states:
            total_score = 0
            for _ in range(self.simulations):
                score = self.simulate(state)
                total_score += score

            average_score = total_score / self.simulations
            if average_score > best_score:
                best_score = average_score
                best_move = state

        self.choice = best_move

    def simulate(self, state):
        # Create a copy of the game to simulate
        simulated_game = self.game.copy()
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
        while simulated_game.run:
            possible_moves = self.get_possible_states(simulated_game)
            if not possible_moves:
                break
            x, y, rotation = random.choice(possible_moves)
            simulated_game.push(x, y, rotation)
            score += simulated_game.score
            simulated_game.pop()

        return score

    def get_possible_states(self, game):
        possible_states = []
        for rotation in range(len(game.current_piece.shape)):
            for x in range(-2, game.cols - 2):
                piece_copy = Piece(x, 0, game.current_piece.shape)
                piece_copy.rotation = rotation
                if game.valid_space(piece_copy):
                    possible_states.append((x, piece_copy.y, rotation))
        return possible_states
>>>>>>> Stashed changes
