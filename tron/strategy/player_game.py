import time
import copy

class PlayerStrategy(object):

    def __init__(self, player_idx):
        self.player_idx = player_idx

    def get_action(self, game, game_state, other=None):
        raise NotImplementedError()

    def on_game_over(self, game, game_state):
        pass

    def get_player_idx(self):
        return self.player_idx

    def get_enemy_idx(self):
        return (self.player_idx + 1) % 2

    def game_is_over(self, game):
        return game.game_over()

    def player_has_won(self, game):
        return not game.player_lost[self.get_player_idx()]

    def enemy_has_won(self, game):
        return not game.player_lost[self.get_enemy_idx()]



class PlayerGame(object):
    def __init__(self, game, strategies):
        self.game = game
        self.strategies = strategies

    def evaluate(self, events = None):
        game_state = self.game.get_game_state_as_class()
        if game_state.game_over:
            print('Warning: called PlayerGame.evaluate when the game is already over!')
            return

        for player_idx, strategy in enumerate(self.strategies):
            action = strategy.get_action(self.game, game_state, events)
            self.game.set_action(player_idx, action)

        if self.game.game_over():
            for strategy in self.strategies:
                strategy.on_game_over(self.game, game_state)