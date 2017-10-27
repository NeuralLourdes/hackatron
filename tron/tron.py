import numpy as np
import collections

GameState = collections.namedtuple('GameState', ['game_over', 'game_field', 'player_pos', 'player_orientation', 'player_lost'])

class Player(object):
    def __init__(self, name='default', x=0, y=0, orientation=90, body=None):
        self.name = name
        self.x = x
        self.y = y
        self.orientation = orientation
        self.body = body if body is not None else []
        self.add_to_body()

    def get_position(self):
        return self.x, self.y

    def add_to_body(self, x = None, y = None):
        if x is None or y is None:
            x, y = self.get_position()

        self.body.append((x, y))

    def do_action(self, action):
        factor = 0

        if action == ACTION_TURN_LEFT:
            factor = -90
        elif action == ACTION_TURN_RIGHT:
            factor = 90

        self.orientation = (self.orientation + factor) % 360

        self.add_to_body()

        if self.orientation == 0:
            self.x += 1
        elif self.orientation == 90:
            self.y += 1
        elif self.orientation == 180:
            self.x -= 1
        else:
            self.y -= 1

        self.add_to_body()


PLAYER_1 = 0
PLAYER_2 = 1

ACTION_TURN_LEFT = 0
ACTION_TURN_RIGHT = 1
ACTION_STRAIGHT = 2

class TronGame(object):

    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.game_field = np.zeros((width, height), dtype=np.int8)
        # Start positions
        self.players = [Player('P1', x = 0, y = 0), Player('P2', x = self.width - 1, y = 0)]
        self.tick = 0
        self.has_played = [False, False]
        self.player_lost = [False, False]

    def set_action(self, player, action):
        if self.game_over():
            print('Warning: tried to do action, but the game is already over! Aborting')
            return

        if self.has_played[player]:
            print('Warning: player {} already did an action this tick. Ignoring'.format(player))
            return

        player_ = self.players[player]
        player_.do_action(action)

        self.has_played[player] = True
        self.check_state()

        if np.all(self.has_played):
            self.has_played = [False, False]
            self.check_for_collision()
            self.tick += 1


    def check_for_collision(self):
        collision_found = False
        for player_idx, player in enumerate(self.players):
            other_player = self.players[(player_idx + 1) % 2]
            collision_found_ = False
            for x, y in other_player.body + player.body[:-1]:
                if player.x == x and player.y == y:
                    collision_found_ = True
                    break
            if collision_found_:
                collision_found = True
                self.player_lost[player_idx] = True

        return collision_found


    def get_player_pos(self):
        return [player.get_position() for player in self.players]

    def get_player_orientation(self):
        return [player.orientation for player in self.players]

    def get_game_state(self):
        return self.game_over(), self.get_game_field(), self.get_player_pos(), self.get_player_orientation(), self.player_lost

    def check_state(self):
        for player_idx, player in enumerate(self.players):
            for x, y in player.body:
                if self.check_field_bounds(x, y):
                    self.player_lost[player_idx] = True

    def check_field_bounds(self, x, y):
        return y < 0 or y >= self.height or x >= self.width or x < 0

    def get_available_actions(self):
        return [ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_STRAIGHT]

    def get_game_field(self):
        self.game_field = np.zeros((self.height, self.width), dtype=np.int8)
        for player_idx, player in enumerate(self.players):
            for x, y in player.body:
                if self.check_field_bounds(x, y):
                    print("Warning: this should not happen, x or y is greater than field dimension")
                    break
                self.game_field[y][x] = player_idx + 1
        return self.game_field

    def get_game_state_flattened(self):
        return np.array(self.get_game_state()).flatten()

    def get_game_state_as_class(self):
        return GameState(*self.get_game_state())

    def game_over(self):
        self.check_state()
        player_has_lost = np.any(self.player_lost)
        has_collision = self.check_for_collision()
        return player_has_lost or has_collision


    def __str__(self):
        out = ''

        game_field = self.get_game_field()

        field_width_padded =(self.width * 2 + 2)
        out += '_' * field_width_padded
        out += '\n'
        for y, row in enumerate(game_field):
            out += '|'
            for x, cell in enumerate(row):
                if cell == -1:
                    out += ' '
                else:
                    out += str(cell)
                out += ' '
            out += '|'
            out += '\n'
        out += '-' * field_width_padded
        return out