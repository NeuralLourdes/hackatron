import numpy as np


def generate_player_mat(gamestate ,player_id):
    return gamestate == player_id


def generate_player_head_mat(gamestate ,headpos):
    result = gamestate == -1
    if np.shape(result)[0]>headpos[1] and headpos[1]>=0 and np.shape(result)[1]>headpos[0] and headpos[0]>=0:
        result[headpos[1], headpos[0] ] =1
    return result


def get_training_matrix(gamestate ,p1pos ,p2pos, player_idx, enemy_idx, player_rotation):
    rotation = player_rotation/90
    p1h = np.rot90(generate_player_head_mat(gamestate, p1pos), rotation)
    p2h = np.rot90(generate_player_head_mat(gamestate, p2pos), rotation)
    p1s = np.rot90(generate_player_mat(gamestate, player_idx), rotation)
    p2s = np.rot90(generate_player_mat(gamestate, enemy_idx), rotation)
    return np.stack([p1h, p2h, p1s, p2s], axis=2)

