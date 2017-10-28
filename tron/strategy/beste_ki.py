from strategy import player_game
import time
from strategy.searchtree.searchtree import Searchtree


class Beste_ki(player_game.PlayerStrategy):

    def __init__(self, player_idx):
        super(Beste_ki, self).__init__(player_idx)
        self.builder = Searchtree(player_idx, self.evaluate_state)

    def get_action(self, game, game_state, other = None):
        timestamp = time.time()
        action = self.builder.find_best_action(game, 3)
        print("Processing step took ", time.time()-timestamp)
        return action

    def evaluate_state(self, game):
        game_state = game.get_game_state_as_class()
        if game_state.game_over:
            if not game.player_lost[self.get_player_idx()]:
                return -1
            else:
                return 1
        return 0

    def on_game_over(self, game, game_state):
        print("I won: ", self.player_has_won(game))
