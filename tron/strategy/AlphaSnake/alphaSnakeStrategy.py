from strategy import player_game
import numpy as np

class alphaSnakeStrategy(player_game.PlayerStrategy):

    def __init__(self):
        super(alphaSnakeStrategy, self).__init__()
        self.last_action = -1

    def get_action(self, game, game_state, other = None):
        #print(game.get_available_actions())
        return 2