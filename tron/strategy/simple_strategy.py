from . import player_game
import numpy as np

class SimpleStrategy(player_game.PlayerStrategy):

    def __init__(self, player_idx = None):
        super(SimpleStrategy, self).__init__(player_idx)


    def get_action(self, game, game_state, other=None):
        player = game.players[self.player_idx]
        used_action = -1
        actions = [game.ACTION_TURN_LEFT, game.ACTION_TURN_RIGHT]
        np.random.shuffle(actions)
        for action in [game.ACTION_STRAIGHT] + actions:
            orientation, next_position = player.get_next_position_after_action(action)
            if not game.check_pos_is_invalid(*next_position) and game_state.game_field[next_position.y][next_position.x] == 0:
                used_action = action
                break
        if used_action == -1:
            used_action = 0
        return action
