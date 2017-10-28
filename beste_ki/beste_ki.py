import random


class Beste_ki(object):

    def __init__(self, player):
        self.player = player

    def predict(self, game):
        print(self.has_lost(game))
        return random.randint(0, 2)

    def has_lost(self, game):
        return game.player_lost[self.player]
