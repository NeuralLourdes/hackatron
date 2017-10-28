from strategy import player_game
import time
import numpy as np


class Beste_ki(player_game.PlayerStrategy):

    def __init__(self, player_idx):
        super(Beste_ki, self).__init__(player_idx)

    def get_action(self, game, game_state, other = None):
        timestamp = time.time()
        score, clone_game, action = self.find_best_action(game, 3)
        print("Processing step took ", time.time()-timestamp)
        return action

    def get_first_item(self, x):
        return x[0]

    def process_state(self, state):
        score, game, action = state
        return [self.replace_action(new_state, action) for new_state in self.generate_next_games(game)]

    def best(self, s1, s2):
        return min([s1, s2], key=self.get_first_item)

    def find_best_action(self, game, max_depth):
        to_be_processed = list([(state, max_depth) for state in self.generate_next_games(game)])

        candidates = []

        while len(to_be_processed) > 0:
            head, *to_be_processed = to_be_processed

            current_state, depth = head

            if depth == 0:
                candidates.append(current_state)

            else:
                new_states = [(state, depth-1) for state in self.process_state(current_state)]
                to_be_processed = to_be_processed + new_states

        print("Found candidates: ", len(candidates))

        return self.determine_winner(candidates)

    def determine_winner(self, candidates):
        result = (1, None, 0)
        for current_state in candidates:
            result = self.best(result, current_state)
        return result

    def replace_action(self, tu, action):
        score, game, _ = tu
        return score, game, action

    def generate_next_games(self, game):
        for action in game.get_available_actions():
            for opponent_action in self.predict_opponent_actions(game):
                cloned_game = game.clone()
                cloned_game.has_played = [False, False]
                cloned_game.set_action(self.get_player_idx(), action)
                cloned_game.set_action(self.get_enemy_idx(), opponent_action)
                score = self.evaluate_state(cloned_game)
                yield (score, cloned_game, action)

    def evaluate_state(self, game):
        game_state = game.get_game_state_as_class()
        if game_state.game_over:
            if self.player_has_won(game):
                return -1
            else:
                return 1
        return 0

    def predict_opponent_actions(self, game):
        return game.get_available_actions()

    def on_game_over(self, game, game_state):
        print("I won: ", self.player_has_won(game))
