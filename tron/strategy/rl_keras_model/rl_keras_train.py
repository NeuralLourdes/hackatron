import os
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam
from keras import callbacks

import rl
from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy, BoltzmannQPolicy
from rl.memory import SequentialMemory

TRAIN_FILE = 'tmp/rl_keras.npy'

def load_progress(model):
    if not os.path.exists(TRAIN_FILE):
        print('File not existing: {}'.format(TRAIN_FILE))
        return
    model.load_weights(TRAIN_FILE)

def save_progress(model):
    model.save_weights(TRAIN_FILE, overwrite=True)

def get_model(env, num_layers = 4, layer_size = 512, window_lenght = 1):
    num_actions = len(env.get_available_actions())
    model = Sequential()

    model.add(Flatten(input_shape=(1,) + env.get_decomposed_game_field().shape))

    #model.add(keras.layers.Conv2D(filters=2, kernel_size = 5, data_format = 'channels_last', input_shape = env.get_decomposed_game_field().shape))
    #model.add(Flatten())

    for i in range(num_layers):
        model.add(Dense(layer_size))
        model.add(Activation('relu'))

    model.add(Dense(num_actions))
    model.add(Activation('linear'))
    print(model.summary())

    policy = EpsGreedyQPolicy(eps=.3)
    memory = SequentialMemory(limit=100000, window_length=window_lenght)

    dqn = DQNAgent(model=model, nb_actions=num_actions, memory=memory, nb_steps_warmup=10000,
    target_model_update=0.5, policy=policy, enable_dueling_network=True)
    dqn.compile(Adam(lr=1e-2), metrics=['mae'])
    return dqn

def get_callbacks(verbose = 2, period = 100):
    return [
        keras.callbacks.ModelCheckpoint(TRAIN_FILE, verbose = verbose, monitor='val_loss', mode='auto', period=period, save_weights_only=True)
    ]