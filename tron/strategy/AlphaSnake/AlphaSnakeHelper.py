import numpy as np


def generate_player_mat(gamestate ,player_id):
    return gamestate == player_id


def generate_player_head_mat(gamestate ,headpos):
    result = gamestate == -1
    if np.shape(result)[0]>headpos[1] and headpos[1]>=0 and np.shape(result)[1]>headpos[0] and headpos[0]>=0:
        result[headpos[1], headpos[0] ] =1
    return result


def get_training_matrix(gamestate ,p1pos ,p2pos, player_idx, enemy_idx, player_rotation):
    p1h = np.rot(generate_player_head_mat(gamestate, p1pos), player_rotation)
    p2h = np.rot(generate_player_head_mat(gamestate, p2pos), player_rotation)
    p1s = np.rot(generate_player_mat(gamestate, player_idx), player_rotation)
    p2s = np.rot(generate_player_mat(gamestate, enemy_idx), player_rotation)
    return np.stack([p1h, p2h, p1s, p2s], axis=2)

