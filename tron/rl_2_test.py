# !/usr/bin/env python3

import numpy as np
import tron
import traceback
import sys
from strategy.rl_keras_model import rl_keras_train


def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Train a keras DQN agend')
    parser.add_argument('--steps', type=int, default=100000)
    parser.add_argument('--width', type=int, default=50)
    parser.add_argument('--height', type=int, default=50)
    parser.add_argument('--disable_loading', action='store_true')
    parser.add_argument('--save_period', type=int, default=100)
    parser.add_argument('--verbose', type=int, default=2)
    args = parser.parse_args()
    return args


def init_game(args):
    env = tron.TronGame(width=args.width, height=args.width)
    env.set_player_pos(env.get_random_pos(), env.get_random_pos())
    env.set_player_orientation([get_random_orientation(), get_random_orientation()])
    return env

def get_random_orientation():
    return np.random.choice([0, 90, 180, 270])

def main():
    args = get_args()
    np.random.seed(123)
    try:
        env = init_game(args)

        dqn = rl_keras_train.get_model(env)
        if not args.disable_loading:
            rl_keras_train.load_progress(dqn)
        dqn.fit(env, nb_steps=args.steps, visualize=False, verbose=args.verbose, callbacks=rl_keras_train.get_callbacks(period=args.save_period))
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print('Warning: {}, {}'.format(e, e.message))
    print('Saving')
    rl_keras_train.save_progress(dqn)


if __name__ == '__main__':
    main()