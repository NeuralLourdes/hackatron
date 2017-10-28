from strategy import player_game
import time
from strategy.searchtree.searchtree import Searchtree
from strategy.AlphaSnake.Game_State_Predictor import Game_State_Predictor


class Beste_ki(player_game.PlayerStrategy):

    def __init__(self, player_idx, width, height):
        super(Beste_ki, self).__init__(player_idx)
        self.GSP = Game_State_Predictor(player_idx, width, height)
        self.builder = Searchtree(player_idx, self.evaluate_games)

    def evaluate_games(self, games):
        matrix_list = [self.GSP.convert_to_prediction_matrix(game) for game in games]
        return [own_score for own_score, _ in self.GSP.get_game_score(matrix_list)]

    def get_action(self, game, game_state, other = None):
        timestamp = time.time()
        p1pos = game_state.player_pos[self.get_player_idx()]
        p2pos = game_state.player_pos[self.get_enemy_idx()]
        self.GSP.on_new_data(game_state.game_field, p1pos, p2pos, self.get_player_idx(), self.get_enemy_idx())
        action = self.builder.find_best_action(game, 2)
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
        self.GSP.on_game_finished(self.player_has_won(game), self.enemy_has_won(game))
        print("I won: ", self.player_has_won(game))
