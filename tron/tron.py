import numpy as np
import collections
import copy

GameState = collections.namedtuple('GameState', ['game_over', 'game_field', 'player_pos', 'player_orientation', 'player_lost'])
Point = collections.namedtuple('Point', ['x', 'y'])

PLAYER_1 = 0
PLAYER_2 = 1

ACTION_TURN_LEFT = 0
ACTION_TURN_RIGHT = 1
ACTION_STRAIGHT = 2


class Player(object):
    def __init__(self, name='default', pos=Point(0, 0), orientation=180, body=None):
        self.name = name
        self.x, self.y = pos
        self.orientation = orientation
        self.body = body if body is not None else []

    def get_position(self):
        return Point(self.x, self.y)

    def set_pos(self, pos):
        self.x, self.y = pos

    def add_to_body(self, pos=None):
        self.body.append(self.get_position() if pos is None else pos)

    def get_next_position_after_action(self, action):
        factor = 0

        if action == ACTION_TURN_LEFT:
            factor = -90
        elif action == ACTION_TURN_RIGHT:
            factor = 90

        orientation = (self.orientation + factor) % 360
        x, y = self.get_position()

        if orientation == 0:
            y -= 1
        elif orientation == 90:
            x += 1
        elif orientation == 180:
            y += 1
        else:
            x -= 1

        return orientation, Point(x, y)


    def do_action(self, action):
        factor = 0

        if action == ACTION_TURN_LEFT:
            factor = -90
        elif action == ACTION_TURN_RIGHT:
            factor = 90

        self.orientation = (self.orientation + factor) % 360

        self.add_to_body()

        if self.orientation == 0:
            self.y -= 1
        elif self.orientation == 90:
            self.x += 1
        elif self.orientation == 180:
            self.y += 1
        else:
            self.x -= 1

    def clone(self):
        copied = Player(self.name, self.get_position(), self.orientation, list(self.body))
        return copied


class TronGame(object):
    ACTION_TURN_LEFT = ACTION_TURN_LEFT
    ACTION_TURN_RIGHT = ACTION_TURN_RIGHT
    ACTION_STRAIGHT = ACTION_STRAIGHT

    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        # Start positions
        self.reset()

    def reset(self):
        x_offset = 10
        y_offset = 10
        self.players = [Player('P1', Point(x_offset, y_offset), orientation=180), Player('P2', Point(self.width - x_offset - 1, self.height - y_offset - 1), orientation=0)]
        self.has_played = [False, False]
        self.player_lost = [False, False]
        self.tick = 0
        self.get_game_field()

    def set_player_pos(self, player_1_pos, player_2_pos):
        for player, pos in zip(self.players, [player_1_pos, player_2_pos]):
            player.set_pos(pos)

    def set_action(self, player, action):
        if self.has_played[player]:
            print('Warning: player {} already did an action this tick. Ignoring'.format(player))
            return

        if np.all(self.has_played) and self.game_over():
            print('Warning: tried to do an action for player {}, but the game is already over! Aborting'.format(player))
            return

        player_ = self.players[player]
        player_.do_action(action)
        self.has_played[player] = True

        if np.all(self.has_played):
            self.get_game_field()
            self.check_player_lost_status()
            self.has_played = [False, False]
            for player in self.players:
                player.add_to_body()
            self.tick += 1


    def get_game_field(self):
        self.game_field = np.zeros((self.height, self.width), dtype=np.int8)

        for player_idx, (x, y) in self.get_player_positions_flat():
            self.game_field[y, x] = player_idx + 1

        return self.game_field

    def check_player_lost_status(self):
        collision_found = False
        for player_idx, player in enumerate(self.players):
            player_lost = False
            pos = player.get_position()
            x, y = pos
            position_invalid = self.check_pos_is_invalid(x, y)
            if position_invalid or self.game_field[y][x] != 0:
                player_lost = True
            # other_player = self.players[(player_idx + 1) % 2]
            #for x, y in other_player.body + player.body[:-1]:
            #    if player.x == x and player.y == y:
            #        collision_found_ = True
            #        break
            if player_lost:
                collision_found = True
                self.player_lost[player_idx] = True
        return collision_found

    def get_player_pos(self):
        return [player.get_position() for player in self.players]

    def get_player_orientation(self):
        return [player.orientation for player in self.players]


    def check_pos_is_invalid(self, x, y):
        res = y < 0 or y >= self.height or x >= self.width or x < 0
        return res

    def get_available_actions(self):
        return [ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_STRAIGHT]

    def get_player_positions_flat(self, check_valid = True):
        player_bodies = []
        for player in [PLAYER_1, PLAYER_2]:
            player_bodies += [(player, pos) for pos in self.players[player].body if not check_valid or not self.check_pos_is_invalid(*pos)]

        return player_bodies


    def get_game_state(self):
        return self.game_over(), self.game_field, self.get_player_pos(), self.get_player_orientation(), self.player_lost
        #return self.game_over(), self.get_game_field(), self.get_player_pos(), self.get_player_orientation(), self.player_lost

    def get_game_state_flattened(self):
        return np.array(self.get_game_state()).flatten()

    def get_game_state_as_class(self):
        return GameState(*self.get_game_state())

    def get_random_pos(self):
        return Point(np.random.choice(self.width), np.random.choice(self.height))

    def clone(self):
        new_game = TronGame()
        new_game.width = self.width
        new_game.height = self.height
        new_game.players = [player.clone() for player in self.players]
        new_game.has_played = np.copy(self.has_played)
        new_game.player_lost = np.copy(self.player_lost)
        new_game.tick = self.tick
        new_game.game_field = None
        return new_game

    def game_over(self):
        player_has_lost = np.any(self.player_lost)
        return player_has_lost

    def __str__(self):
        out = 'Tick: {}\n'.format(self.tick)
        field_width_padded = (self.width * 2 + 2)
        out += '_' * field_width_padded
        out += '\n'
        for row in self.get_game_field():
            out += '|'
            for cell in row:
                if cell == 0:
                    out += ' '
                else:
                    out += str(cell)
                out += ' '
            out += '|\n'
        out += '-' * field_width_padded
        return out
