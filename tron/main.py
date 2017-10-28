#!/usr/bin/env python3

import os, pygame
from pygame import locals
import tron
from time import time
import sys
import numpy as np

from strategy.human_player_strategy import HumanPlayerStrategy
from strategy.random_strategy import RandomStrategy
from strategy.simple_strategy import SimpleStrategy
from strategy.player_game import PlayerGame
from strategy.rl_strategy import RLStrategy
#from strategy.beste_ki import Beste_ki

def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Tron game')
    parser.add_argument('--width', type=int, default = 30)
    parser.add_argument('--height', type=int, default = 30)
    parser.add_argument('--player_dim', type=float, default=4)
    parser.add_argument('--timeout', type=int, default = 50)
    args = parser.parse_args()
    return args

def has_quit(events):
    for event in events:
        if event.type == pygame.QUIT:
            return True
        if event.type == locals.KEYDOWN and event.key == locals.K_ESCAPE:
            return True
    return False

def main():
    args = get_args()

    def init_game(random = False):
        def get_random_orientation():
            return np.random.choice([0, 90, 180, 270])
        game = tron.TronGame(width = args.width, height = args.height)
        if random:
            game.set_player_pos(game.get_random_pos(), game.get_random_pos())
            game.set_player_orientation([get_random_orientation(), get_random_orientation()])
        return game

    game = init_game()

    strategy_1 = HumanPlayerStrategy(player_idx=0)
    strategy_2 = HumanPlayerStrategy(player_idx=1)

    #strategy_1 = SimpleStrategy(0)
    #strategy_2 = SimpleStrategy(1)

    strategy_1 = RLStrategy(0)
    strategy_2 = RLStrategy(1)
    #strategy_1 = SimpleStrategy(0)
    #strategy_2 = SimpleStrategy(1)
    #strategy_1 = Beste_ki(0)
    #strategy_2 = Beste_ki(1)
    strategies = [strategy_1, strategy_2]

    player_game = PlayerGame(game, strategies)
    # GUI

    pygame.init()
    screen = pygame.display.set_mode((int(args.width * args.player_dim), int(args.height * args.player_dim)))
    pygame.display.set_caption('Tron')
    pygame.mouse.set_visible(0)
    clock = pygame.time.Clock()

    def get_background():
        background = pygame.Surface(screen.get_size())
        background.fill((255, 255, 255))  # fill the background white
        background = background.convert()  # prepare for faster blitting
        return background

    background = get_background()

    PLAYER_COLORS = [(255, 0, 0), (0, 0, 255)]

    going = True
    while going:
        clock.tick(1000)

        events = pygame.event.get()
        if events is None:
            events = []

        if has_quit(events):
            pygame.quit()
            sys.exit()


        player_game.evaluate(events)

        for y, row in enumerate(game.get_game_state_as_class().game_field):
            for x, cell in enumerate(row):
                if cell != 0:
                    pygame.draw.rect(background, PLAYER_COLORS[cell - 1], (x * args.player_dim, y * args.player_dim, args.player_dim, args.player_dim))

        wants_to_restart = False
        for event in events:
            if event.type == locals.KEYDOWN and event.key == locals.K_r:
                wants_to_restart = True

        # Restart game
        if game.game_over() or wants_to_restart:
            game_state = game.get_game_state_as_class()
            for player_idx, strategy in enumerate(strategies):
                strategy.on_game_over(game, game_state)
            pygame.time.wait(500)
            background = get_background()
            game = init_game()
            player_game.game = game
            continue

        screen.blit(background, (0, 0))
        pygame.display.flip()

    pygame.quit()



if __name__ == '__main__':
    main()