from strategy import player_game
import numpy as np

import pygame
from pygame import locals

PLAYER_KEYS = [
    [locals.K_a, locals.K_d],
    [locals.K_LEFT, locals.K_RIGHT]
]

class HumanPlayerStrategy(player_game.PlayerStrategy):

    def __init__(self, player_idx = 0):
        super(HumanPlayerStrategy, self).__init__()
        self.player_idx = player_idx
        self.keys = PLAYER_KEYS[player_idx]

    def get_action(self, game, game_state, events = None):
        left_key, right_key = self.keys
        action = game.ACTION_STRAIGHT
        for event in events:
            if event.type == locals.KEYDOWN and (event.key == left_key or event.key == right_key):
                action = game.ACTION_TURN_LEFT if event.key == left_key else game.ACTION_TURN_RIGHT
        return action
