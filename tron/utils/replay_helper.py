import os
from glob import glob
import pickle
import datetime
import time

REPLAY_FOLDER = 'replays'

def init_replay(folder):
    global REPLAY_FOLDER
    REPLAY_FOLDER = folder
    if not os.path.exists(REPLAY_FOLDER):
        os.makedirs(folder)

def get_all_replays(replay_folder = None, verbose = False):
    replays = []
    for filename in glob('{}/replay_*'.format(replay_folder)):
        try:
            replays.append((filename, get_replay(filename)))
        except:
            if verbose:
                print('Warning: could not load replay: {}'.format(filename))
    return reversed(replays)

def save_replay(replay, filename = None, info = {}):
    if filename is None:
        filename = 'replay_{}.npy'.format(get_time_formatted())

    for key, val in info.items():
        replay.info[key] = val

    with open('{}/{}'.format(REPLAY_FOLDER, filename), 'wb') as f:
        pickle.dump(replay, f)

def get_replay(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def get_time_formatted():
    return str(datetime.datetime.now())

def get_timestamp():
    return time.strftime("%Y%m%d-%H%M%S")
    #return datetime.datetime.now().timestamp()

def seconds_to_human_readable(s, remove_milliseconds=True):
    return str(datetime.timedelta(seconds=s)).rsplit('.')[0]