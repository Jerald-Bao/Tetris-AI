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
