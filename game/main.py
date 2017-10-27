#!/usr/bin/env python3

import tron

def main():
    args = get_args()
    game = tron.TronGame(width = 20, height = 20)
    print(game)
    game.set_action(0, tron.ACTION_TURN_LEFT)
    game.set_action(1, tron.ACTION_TURN_RIGHT)
    for i in range(30):
        if game.game_over():
            break
        for player in range(0, 2):
            if game.game_over():
                break
            game.set_action(player, tron.ACTION_STRAIGHT)
        print(game)
    game_state = game.get_game_state()


def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='desc')
    parser.add_argument('--arg', type=str, help="help", default='default')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()