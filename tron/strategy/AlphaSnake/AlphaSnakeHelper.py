
import numpy as np

def generate_player_mat(base ,player_id):
    return base == player_id

def generate_player_head_mat(base ,headpos):
    result = base == -1
    result[headpos[1], headpos[0] ] =1
    return result


def get_training_matrix(base ,p1pos ,p2pos, player_idx,):
    p1h = generate_player_head_mat(base, p1pos)
    p2h = generate_player_head_mat(base, p2pos)
    p1s = generate_player_mat(base, player_idx)
    p2s = generate_player_mat(base, )
    return np.stack([p1h, p2h, p1s, p2s], axis=2)

