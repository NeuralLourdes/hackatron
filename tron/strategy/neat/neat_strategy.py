from .. import player_game
import numpy as np
from . import play_tron
import os

from . import NN_IO

filename = os.path.join(os.path.dirname(__file__), 'beste')
bester_boi = NN_IO.restore(filename)

class NEATStrategy(player_game.PlayerStrategy):

    def __init__(self, player_idx = None):
        super(NEATStrategy, self).__init__(player_idx)


    def get_action(self, game, game_state, other=None):
        player = game.players[self.player_idx]
        action = play_tron.calc_next_action(game, self.player_idx, bester_boi)

        return action
