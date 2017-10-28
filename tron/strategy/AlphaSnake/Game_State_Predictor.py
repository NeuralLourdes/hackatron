import sys
import os
import numpy as np
import tensorflow as tf
#from tfsave import *
import random
from strategy import player_game
import strategy.AlphaSnake.GameStatePredictionNetwork as gspn
from strategy.AlphaSnake.AlphaSnakeHelper import *
import pickle
import time
import zipfile

learning_rate = 0.000001

train_every_x_losses = 100
print_every_x_frames = 10
reset_data_after_training = True
debug_mode=True
batch_size=5

class Game_State_Predictor:


    def __init__(self,player_idx,width,height):
        self.game_state_input_buffer = []
        self.flipped_game_state_input_buffer = []
        self.game_state_output_buffer = []

        self.keep_prob_tensor = tf.placeholder(tf.float32)
        self.input_tensor = tf.placeholder(tf.float32, [None, height, width, 4])
        self.output_tensor = tf.placeholder(tf.float32, [None, 2])
        self.model_out_with_softmax_tensor, self.cost_tensor = gspn.get_prediction_network(self.input_tensor, self.output_tensor, self.keep_prob_tensor,"ASPN"+str(player_idx))
        self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.cost_tensor)

        self.tf_sess = tf.Session()
        self.tf_sess.run(tf.global_variables_initializer())

        self.reset_counter=0
        self.framecounter=0

    def on_new_data(self, field, p1pos, p2pos, p1_idx, p2_idx):

        train_mat = get_training_matrix(field, p1pos, p2pos, p1_idx, p2_idx)
        self.game_state_input_buffer.append(train_mat)

        flipped_train_mat = get_training_matrix(field, p2pos, p1pos, p1_idx, p2_idx)
        self.flipped_game_state_input_buffer.append(flipped_train_mat)

    def get_batch(self, x, y, size):
        if size < len(x):
            choices = np.random.choice(len(x), size, replace=False)
            resx = []
            resy = []
            for i in choices:
                resx.append(x[i])
                resy.append(y[i])
            return resx, resy
        else:
            return x, y

    def train(self, x_train, y_train, x_test, y_test, dropout):
        batch_training_iters=1
        for step in range(batch_training_iters):
            batch_x, batch_y = self.get_batch(x_train, y_train, batch_size)

            self.tf_sess.run(self.optimizer, feed_dict={self.input_tensor: batch_x, self.output_tensor: batch_y, self.keep_prob_tensor: dropout})

        print("trained player")


    def create_data(self, p1_won,p2_won):
        add_length = len(self.flipped_game_state_input_buffer)
        new_output_data = np.ones((add_length, 2)) * (p1_won, p2_won)
        flipped_new_output_data = np.ones((add_length, 2)) * (p2_won, p1_won)


        if len(self.game_state_output_buffer) == 0:
            self.game_state_output_buffer = np.concatenate([new_output_data, flipped_new_output_data], 0)
        else:
            self.game_state_output_buffer = np.concatenate([self.game_state_output_buffer, new_output_data, flipped_new_output_data], 0)

        self.game_state_input_buffer = self.game_state_input_buffer + self.flipped_game_state_input_buffer

        self.flipped_game_state_input_buffer = []


    def load_data(self,t):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        filepath = dir_path + '/Data/{}_in_out.data'.format(t)
        zippath = dir_path + '\\Data\\{}_in_out.zip'.format(t)

        fh=open(zippath, 'rb')
        z = zipfile.ZipFile(fh)
        for name in z.namelist():
            outpath = dir_path+"/Data/"
            z.extract(name, outpath)
        fh.close()

        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        os.remove(filepath)

        return data[0], data[1]


    def save_data(self,inp,outp):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        data = [inp, outp]

        t=time.time()

        filepath = dir_path + '/Data/{}_in_out.data'.format(t)
        zippath = dir_path + '/Data/{}_in_out.zip'.format(t)

        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

        zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED).write(filepath, os.path.basename(filepath))

        os.remove(filepath)

    def get_game_score(self, field, ppos, npos, p1_idx, p2_idx):
        train_mat = get_training_matrix(field, ppos, npos, p1_idx, p2_idx)
        prediction = self.tf_sess.run(self.model_out_with_softmax_tensor, feed_dict={self.input_tensor: [train_mat], self.keep_prob_tensor: 1.0})
        return prediction[0]


    def on_game_finished(self,p1_won,p2_won):
        self.framecounter = 0

        if len(self.game_state_input_buffer) > 0 and not len(self.game_state_input_buffer)==len(self.game_state_output_buffer):

            self.create_data(p1_won,p2_won)

            self.reset_counter += 1

            if debug_mode:
                print("data_added player")

            if self.reset_counter>train_every_x_losses:
                self.reset_counter=0
                self.train(self.game_state_input_buffer, self.game_state_output_buffer, None, None, 0.9)
                if reset_data_after_training:
                    self.save_data(self.game_state_input_buffer, self.game_state_output_buffer)
                    self.game_state_output_buffer = []
                    self.game_state_input_buffer = []