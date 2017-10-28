# !/usr/bin/env python3

import numpy as np
import tron
from strategy.rl_keras_model import rl_keras_train


def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Train a keras DQN agend')
    parser.add_argument('--steps', type=int, default=100000)
    parser.add_argument('--width', type=int, default=100)
    parser.add_argument('--height', type=int, default=100)
    parser.add_argument('--disable_loading', action='store_true')
    parser.add_argument('--save_period', type=int, default=100)
    parser.add_argument('--verbose', type=int, default=2)
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    np.random.seed(123)
    try:
        env = tron.TronGame(width=args.width, height=args.width)
        dqn = rl_keras_train.get_model(env)
        if not args.disable_loading:
            rl_keras_train.load_progress(dqn)
        dqn.fit(env, nb_steps=args.steps, visualize=False, verbose=args.verbose, callbacks=rl_keras_train.get_callbacks(period=args.save_period))
    except Exception as e:
        print('Warning: {}'.format(e))
    print('Saving')
    rl_keras_train.save_progress(dqn)


if __name__ == '__main__':
    main()