#!/usr/bin/env python3

import os, pygame
from pygame import locals
import tron
import time

from strategy.human_player_strategy import HumanPlayerStrategy
from strategy.random_strategy import RandomStrategy

def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Tron game')
    parser.add_argument('--width', type=int, default = 100)
    parser.add_argument('--height', type=int, default = 100)
    parser.add_argument('--player_dim', type=float, default=4)
    parser.add_argument('--timeout', type=int, default = 50)
    args = parser.parse_args()
    return args

def main():
    args = get_args()

    game = tron.TronGame(width = args.width, height = args.height)

    strategy_1 = HumanPlayerStrategy(player_idx=0)
    strategy_2 = HumanPlayerStrategy(player_idx=1)
    strategy_2 = RandomStrategy()
    strategies = [strategy_1, strategy_2]

    # GUI

    pygame.init()
    screen = pygame.display.set_mode((int(args.width * args.player_dim), int(args.height * args.player_dim)))
    pygame.display.set_caption('Tron')
    pygame.mouse.set_visible(1)
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
        clock.tick(60)

        events = pygame.event.get()
        game_state = game.get_game_state_as_class()
        for player_idx, strategy in enumerate(strategies):
            action = strategy.get_action(game, game_state, events)
            game.set_action(player_idx, action)


        for y, row in enumerate(game.get_game_state_as_class().game_field):
            for x, cell in enumerate(row):
                if cell != 0:
                    pygame.draw.rect(background, PLAYER_COLORS[cell - 1], (x * args.player_dim, y * args.player_dim, args.player_dim, args.player_dim))

        # Restart game
        if game.game_over():
            pygame.time.wait(500)
            background = get_background()
            game.reset()
            continue

        screen.blit(background, (0, 0))
        pygame.display.flip()

    pygame.quit()



if __name__ == '__main__':
    main()