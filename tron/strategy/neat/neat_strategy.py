from .. import player_game
import numpy as np
from . import play_tron
import os

from . import NN_IO


class NEATStrategy(player_game.PlayerStrategy):

    def __init__(self, player_idx = None):
        super(NEATStrategy, self).__init__(player_idx)
        filename = os.path.join(os.path.dirname(__file__), 'beste')
        self.bester_boi = NN_IO.restore(filename)


    def get_action(self, game, game_state, other=None):
        player = game.players[self.player_idx]
        play_tron.gameSize = [game.width, game.height]
        action = play_tron.calc_next_action(game, self.player_idx, self.bester_boi)

        return action
