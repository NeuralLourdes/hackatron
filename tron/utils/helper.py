import numpy as np

def get_rotation_matrix(rotation_in_deg):
    theta = np.deg2rad(rotation_in_deg)
    c, s = np.cos(theta), np.sin(theta)
    R = np.matrix('{} {}; {} {}'.format(c, -s, s, c))
    return R