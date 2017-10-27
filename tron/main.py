#!/usr/bin/env python3

import tron

def main():
    args = get_args()
    game = tron.TronGame(width = 20, height = 20)
    print(game)
    for i in range(30):
        for player in range(0, 2):
            if game.game_over():
                break
            game.set_action(player, tron.ACTION_STRAIGHT)
        if game.game_over():
            break
        print(game)
    game_state = game.get_game_state()
    player_have_lost = game.player_lost


def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='desc')
    parser.add_argument('--arg', type=str, help="help", default='default')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()