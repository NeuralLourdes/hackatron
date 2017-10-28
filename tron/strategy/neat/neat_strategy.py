from . import player_game
import numpy as np
import play_tron

import NN_IO

bester_boi = NN_IO.restore('beste1')

class SimpleStrategy(player_game.PlayerStrategy):

    def __init__(self, player_idx = None):
        super(SimpleStrategy, self).__init__(player_idx)


    def get_action(self, game, game_state, other=None):
        player = game.players[self.player_idx]
        action = play_tron.calc_next_action(game, player, bester_boi)

        return action
