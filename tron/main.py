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
from strategy.rl_keras_strategy import RLKerasStrategy
#from strategy.beste_ki import Beste_ki
#from strategy.neat.neat_strategy import NEATStrategy
#from strategy.neat.neat_strategy import NEATStrategy
from strategy.neat.neat_strategy import NEATStrategy
#from strategy.rl_strategy import RLStrategy
from strategy.beste_ki import Beste_ki

def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Tron game')
    parser.add_argument('--width', type=int, default = 15)
    parser.add_argument('--height', type=int, default = 15)
    parser.add_argument('--player_dim', type=int, default=5)
    parser.add_argument('--skip_frames', type=int, default=1)
    parser.add_argument('--timeout', type=int, default = 10)
    parser.add_argument('--player_1_strategy', type=str, default = 'simple')
    parser.add_argument('--player_2_strategy', type=str, default = 'simple')
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

    def init_game(random = True):
        def get_random_orientation():
            return np.random.choice([0, 90, 180, 270])
        game = tron.TronGame(width = args.width, height = args.height)
        if random:
            game.set_player_pos(game.get_random_pos(), game.get_random_pos())
            game.set_player_orientation([get_random_orientation(), get_random_orientation()])
        return game

    game = init_game(True)

    strategy_definitions = dict(
        simple = lambda p: SimpleStrategy(p),
        human = lambda p: HumanPlayerStrategy(p),
        beste_ki = lambda p: Beste_ki(p, game.width, game.height),
        rl = lambda p: RLStrategy(p),
        rl_keras = lambda p: RLKerasStrategy(p, game),
        neat = lambda p: NEATStrategy(p)
    )

    strategies = []
    for player_idx, player_strategy_str in enumerate([args.player_1_strategy, args.player_2_strategy]):
        if player_strategy_str not in strategy_definitions:
            print('Strategy for player {} is invalid: {}. Valid strategies are: {}'.format(player_idx, player_strategy_str, strategy_definitions.keys()))
            sys.exit(1)
        strategies.append(strategy_definitions[player_strategy_str](player_idx))

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

    def draw_game():
        for y, row in enumerate(game.get_game_state_as_class().game_field):
            for x, cell in enumerate(row):
                if cell != 0:
                    pygame.draw.rect(background, PLAYER_COLORS[cell - 1], (x * args.player_dim, y * args.player_dim, args.player_dim, args.player_dim))

        screen.blit(background, (0, 0))
        pygame.display.flip()


    going = True
    counter = 0
    while going:
        start_time = time()
        clock.tick(1000)

        events = pygame.event.get()
        if events is None:
            events = []

        if has_quit(events):
            pygame.quit()
            sys.exit()

        player_game.evaluate(events)


        wants_to_restart = False
        for event in events:
            if event.type == locals.KEYDOWN and event.key == locals.K_r:
                wants_to_restart = True

        # Restart game
        if game.game_over() or wants_to_restart:
            draw_game()
            game_state = game.get_game_state_as_class()
            for player_idx, strategy in enumerate(strategies):
                strategy.on_game_over(game, game_state)
            pygame.time.wait(500)
            background = get_background()
            game = init_game(True)
            player_game.game = game
            continue

        if counter % args.skip_frames == 0:
            draw_game()
            #sys.stdout.write('\r{}'.format())
        counter += 1

    pygame.quit()



if __name__ == '__main__':
    main()