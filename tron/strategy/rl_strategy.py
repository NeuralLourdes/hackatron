import numpy as np
import pickle
from . import player_game
from .reinforcement_learning.rl_strategy_train import *

class RLStrategy(player_game.PlayerStrategy):

    def __init__(self, player_idx = None, strategy_file = 'tmp/rl_strategy.npy'):
        super(RLStrategy, self).__init__(player_idx)
        self.load_strategy(strategy_file)

    def load_strategy(self, strategy_file):
        with open(strategy_file, 'rb') as f:
            self.RLS = pickle.load(f)

    def get_action(self, game, game_state, other=None):
        action = self.RLS[self.player_idx].choose_action(str(game_state))
        return action
