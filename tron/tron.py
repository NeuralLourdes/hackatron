import numpy as np
import collections

GameState = collections.namedtuple('GameState', ['game_over', 'game_field', 'player_pos', 'player_orientation', 'player_lost'])
Point = collections.namedtuple('Point', ['x', 'y'])

PLAYER_1 = 0
PLAYER_2 = 1
ACTION_TURN_LEFT = 0
ACTION_TURN_RIGHT = 1
ACTION_STRAIGHT = 2


class Player(object):
    def __init__(self, name='default', pos=Point(0, 0), orientation=90, body=None):
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
        self.players = [Player('P1', Point(x_offset, y_offset)), Player('P2', Point(self.width - x_offset - 1, self.height - y_offset - 1), 270)]
        self.has_played = [False, False]
        self.player_lost = [False, False]
        self.tick = 0
        self.game_field = None

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
            self.check_player_lost_status()
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

    def check_player_lost_status(self):
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
                    break
                self.game_field[y][x] = player_idx + 1
        return self.game_field

    def get_game_state(self):
        return self.game_over(), self.get_game_field(), self.get_player_pos(), self.get_player_orientation(), self.player_lost

    def get_game_state_flattened(self):
        return np.array(self.get_game_state()).flatten()

    def get_game_state_as_class(self):
        return GameState(*self.get_game_state())

    def game_over(self):
        self.check_player_lost_status()
        player_has_lost = np.any(self.player_lost)
        has_collision = self.check_for_collision()
        return player_has_lost or has_collision

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
