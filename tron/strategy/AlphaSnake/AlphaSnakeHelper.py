
import numpy as np

def generate_player_mat(gamestate ,player_id):
    return gamestate == player_id

def generate_player_head_mat(gamestate ,headpos):
    result = gamestate == -1
    result[headpos[1], headpos[0] ] =1
    return result


def get_training_matrix(gamestate ,p1pos ,p2pos, player_idx, enemy_idx):
    p1h = generate_player_head_mat(gamestate, p1pos)
    p2h = generate_player_head_mat(gamestate, p2pos)
    p1s = generate_player_mat(gamestate, player_idx)
    p2s = generate_player_mat(gamestate, enemy_idx)
    return np.stack([p1h, p2h, p1s, p2s], axis=2)

