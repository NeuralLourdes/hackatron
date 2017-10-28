from . import player_game
import numpy as np

class SimpleStrategy(player_game.PlayerStrategy):

    def __init__(self, player_idx = None, default_action = None):
        super(SimpleStrategy, self).__init__(player_idx)
        if not default_action:
            default_action = 0
        self.default_action = default_action


    def get_action(self, game, game_state, other=None):
        #game.ACTION_TURN_LEFT
        #game.ACTION_TURN_RIGHT
        #game.ACTION_STRAIGHT
        player = game.players[self.player_idx]
        pos = player.pos

        return self.default_action
