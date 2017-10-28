from . import player_game
from .rl_keras_model import rl_keras_train

class RLKerasStrategy(player_game.PlayerStrategy):

    def __init__(self, player_idx = None, game = None):
        super(RLKerasStrategy, self).__init__(player_idx)
        self.game = game
        self.load_model()

    def load_model(self):
        self.model = rl_keras_train.get_model(self.game)
        rl_keras_train.load_progress(self.model)

    def get_action(self, game, game_state, other=None):
        action = self.model.forward(game.get_decomposed_game_field())
        return action
