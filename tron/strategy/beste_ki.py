from strategy import player_game
import numpy as np


class Beste_ki(player_game.PlayerStrategy):

    def __init__(self, player_idx):
        super(Beste_ki, self).__init__(player_idx)
        self.game_state_history = []

    def get_action(self, game, game_state, other = None):
        self.game_state_history.append(game_state)

        score, clone_game, action = self.find_best_action(game, 0)
        return action



    def find_best_action(self, game, max_depth):
        states = self.generate_next_games(game)

        def get_first_item(x):
            return x[0]

        if max_depth > 0:
            states = [self.replace_action(self.find_best_action(new_game, max_depth-1), action) for score, new_game, action in states]
            return min(states, key=get_first_item)
        else:
            return min(states, key=get_first_item)

    def replace_action(self, tu, action):
        score, game, _ = tu
        return score, game, action

    def generate_next_games(self, game):
        for action in game.get_available_actions():
            for opponent_action in self.predict_opponent_actions(game):
                cloned_game = game.clone()
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
