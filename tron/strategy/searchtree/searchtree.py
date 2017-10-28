from multiprocessing import Pool
import time
import numpy as np

#pool = Pool()

class Searchtree:

    def __init__(self, own_index, evaluate_games):
        self.own_index = own_index
        self.enemy_index = 1-own_index
        self.evaluate_games = evaluate_games

    def get_first_item(self, x):
        return x[0]

    def process_state(self, state):
        game, action = state
        return [self.replace_action(new_state, action) for new_state in self.generate_next_games(game)]

    def best(self, s1, s2):
        return max([s1, s2], key=self.get_first_item)

    def find_best_action(self, game, max_depth):
        timestamp = time.time()
        to_be_processed = list([(state, max_depth) for state in self.generate_next_games(game)])

        candidates = []
        counter = 0

        while len(to_be_processed) > 0:
            head, *to_be_processed = to_be_processed

            current_state, depth = head

            if depth == 0:
                candidates.append(current_state)
            else:
                counter+=1
                new_states = [(state, depth-1) for state in self.process_state(current_state)]
                to_be_processed = to_be_processed + new_states

        #print("Found candidates: ", len(candidates), " counter ", counter, " took ", time.time()-timestamp)
        timestamp = time.time()
        action = self.determine_winner(candidates)
        #print("Evaluating took ",time.time()-timestamp)
        return action

    def determine_winner(self, candidates):

        games = [candidate[0] for candidate in candidates]
        actions = [candidate[1] for candidate in candidates]
        scores = self.evaluate_games(games)
        #candidates = [self.evaluate_candidate(candidate) for candidate in candidates]
        best_score_index = np.argmax(scores)
        print("Score ",scores[best_score_index])
        return actions[best_score_index]

    def evaluate_candidate(self, candidate):
        cloned_game, action = candidate
        score = self.evaluate_state(cloned_game)
        return (score, cloned_game, action)

    def replace_action(self, tu, action):
        game, _ = tu
        return game, action

    def generate_next_games(self, game):
        for action in game.get_available_actions():
            for opponent_action in self.predict_opponent_actions(game):
                cloned_game = game.clone()
                cloned_game.has_played = [False, False]
                cloned_game.set_action(self.own_index, action)
                cloned_game.set_action(self.enemy_index, opponent_action)
                yield (cloned_game, action)

    def predict_opponent_actions(self, game):
        return game.get_available_actions()

