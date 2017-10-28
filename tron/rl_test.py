from strategy.reinforcement_learning.rl_strategy_train import *
import tron
import pickle
import os

env = tron.TronGame(width = 30, height = 30)

STRATEGY_FILE = 'tmp/rl_strategy.npy'

def calculate_reward(player_idx):
    return env.tick + (-10 if env.player_lost[player_idx] else 20)

USE_CHECK_POINT = True
NUM_GAMES = 1000000

if USE_CHECK_POINT and os.path.exists(STRATEGY_FILE):
    with open(STRATEGY_FILE, 'rb') as f:
        RLS = pickle.load(f)
else:
    RLS = [QLearningTable(actions=list(env.get_available_actions())) for x in range(2)]

def check_point():
    with open(STRATEGY_FILE, 'wb') as f:
        pickle.dump(RLS, f)

def get_observation_presentation(observation):
    return str(observation.reshape(-1))

try:
    for games in range(NUM_GAMES):
        # initial observation
        observation = env.game_field

        if games % 5 == 0:
            check_point()

        env.reset()
        while True:
            # fresh env
            actions = []
            for player_idx, RL in enumerate(RLS):
                # RL choose action based on observation
                action = RL.choose_action(get_observation_presentation(observation))
                actions.append(action)
                env.set_action(player_idx, action)

            observation_ = env.game_field
            for player_idx, (RL, action) in enumerate(zip(RLS, actions)):
                reward = calculate_reward(player_idx)

                # RL learn from this transition
                RL.learn(get_observation_presentation(observation), action, reward, get_observation_presentation(observation_))

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if env.game_over():
                break
        print('({:4}/{}) {} ticks'.format(games + 1, NUM_GAMES, env.tick))
except:
    print('Saving strategy')
    check_point()

# Play test game
for i in range(2):
    env.reset()
    while not env.game_over():
        game_state = env.game_field
        for player_idx, RL in enumerate(RLS):
            action = RL.choose_action(str(game_state))
            env.set_action(player_idx, action)
    print(env)
