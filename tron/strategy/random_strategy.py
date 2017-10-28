from . import player_game
import numpy as np

class RandomStrategy(player_game.PlayerStrategy):

    def __init__(self, player_idx = None):
        super(RandomStrategy, self).__init__(player_idx)
        self.last_action= -1

    def get_random_choice(self, game):
        return np.random.choice(game.get_available_actions())

    def get_action(self, game, game_state, other = None):
        choice = self.get_random_choice(game)
        while choice == self.last_action:
            choice = self.get_random_choice(game)
        self.last_action = choice
        print('Random', choice)
        return choice
