from utils import replay_helper
import tron
import pygame
from pygame import locals
import sys

def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Play a replay')
    parser.add_argument('--replay_file', type=str, default = None)
    parser.add_argument('--player_dim', type=int, default=14)
    parser.add_argument('--delay_after_gameover', type=int, default=500)
    parser.add_argument('--tick_delay', type=int, default=1)
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    used_replays = [(args.replay_file, replay_helper.get_replay(args.replay_file))] if args.replay_file else replay_helper.get_all_replays()

    pygame.font.init()
    font = pygame.font.SysFont("Verdana", 20)

    text_color = (120, 120, 120)
    text_position = (5, 5)
    game_offset = (5, 100)

    for replay_file, replay in used_replays:
        info = replay.info
        start_positions = [body[0] for body in replay.bodies]
        start_orientations = [orientation[0] for orientation in replay.orientations]
        width, height = replay.info['width'], replay.info['height']

        game = tron.TronGame(width = width, height = height, save_history=False)
        game.set_player_orientation(start_orientations)
        game.set_player_pos(*start_positions)

        pygame.init()
        screen = pygame.display.set_mode((int(width * args.player_dim) + game_offset[0] * 2 , int(height * args.player_dim) + game_offset[1]))

        pygame.display.set_caption('Tron')
        pygame.mouse.set_visible(0)

        texts = [replay_file.split('/')[-1]]
        if 'strategies' in info:
            strategies = info['strategies']
            texts.append(" vs. ".join(strategies))

        def render_text(t):
            return font.render(t, True, text_color)

        texts = [render_text(t) for t in texts]

        clock = pygame.time.Clock()

        for idx, game_field in enumerate(replay.game_field):
            clock.tick(1000)
            resume_this_game = draw_game(screen, game_field, clock, args.player_dim, args.tick_delay, background_offset = game_offset)

            for idx, text in enumerate(texts + [render_text('Tick: {}'.format(idx))]):
                screen.blit(text, (text_position[0], text_position[1] + (30 * idx)))

            pygame.display.flip()
            pygame.time.wait(args.tick_delay)
            if not resume_this_game:
                break

        pygame.time.wait(args.delay_after_gameover)

        # OLD
        if False:

            for p1_action, p2_action in zip(*replay.actions):
                game.set_action(0, p1_action)
                game.set_action(1, p2_action)
                'FALSE'
                resume_this_game = draw_game(screen, game, clock, args.player_dim, args.tick_delay)
                #



def draw_game(screen, game_field, clock, player_dim, tick_delay, background_offset = (0, 0), player_colors = [(255, 0, 0), (0, 0, 255)]):
    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))  # fill the background white
    background = background.convert()  # prepare for faster blitting

    offset_x, offset_y = background_offset
    for y, row in enumerate(game_field):
        for x, cell in enumerate(row):
            if cell != 0:
                pygame.draw.rect(background, player_colors[cell - 1], (x * player_dim  + offset_x, y * player_dim + offset_y, player_dim, player_dim))

    screen.blit(background, (0, 0))


    events = pygame.event.get()
    if events is None: events = []
    resume = not has_quit(events)

    return resume


def has_quit(events):
    for event in events:
        if event.type == pygame.QUIT:
            return True
        if event.type == locals.KEYDOWN and event.key == locals.K_ESCAPE:
            return True
    return False

if __name__ == '__main__':
    main()