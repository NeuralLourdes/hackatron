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

import tron as tron

from strategy.AlphaSnake.Tree_Node import tree_node
from strategy.AlphaSnake.Game_State_Predictor import Game_State_Predictor



class alphaSnakeStrategy(player_game.PlayerStrategy):

    def __init__(self, player_idx, width, height):
        super(alphaSnakeStrategy, self).__init__(player_idx)

        self.GSP=Game_State_Predictor(player_idx, width, height)




    def get_action(self, game, game_state, other = None):
        p1pos = game_state.player_pos[self.get_player_idx()]
        p2pos = game_state.player_pos[self.get_enemy_idx()]

        self.GSP.on_new_data(game_state.game_field,p1pos,p2pos,self.get_player_idx(),self.get_enemy_idx())

        #self.framecounter += 1
        #if debug_mode and print_every_x_frames!=0 and self.framecounter%print_every_x_frames==0:
        #    prediction=self.tf_sess.run(self.model_out_with_softmax_tensor, feed_dict={self.input_tensor: [train_mat], self.keep_prob_tensor: 1.0})
        #    print("{} player{}".format(prediction[0],self.player_idx))


        player = game.players[self.player_idx]
        used_action = -1
        actions = [game.ACTION_TURN_LEFT, game.ACTION_TURN_RIGHT]
        np.random.shuffle(actions)
        for action in [game.ACTION_STRAIGHT] + actions:
            orientation, next_position = player.get_next_position_after_action(action)
            if not game.check_pos_is_invalid(*next_position) and game_state.game_field[next_position.y][next_position.x] == 0:
                used_action = action
                break
        if used_action == -1:
            used_action = 0

        return np.random.choice([np.random.choice(game.get_available_actions()),action,action,action,action,action,action])



    def on_game_over(self, game, game_state):
        self.GSP.on_game_finished(self.player_has_won(game),  self.enemy_has_won(game))


    def game_is_over(self, game):
        return game.game_over()

    def player_has_won(self, game):
        return game.player_lost[self.get_player_idx()]

    def enemy_has_won(self, game):
        return game.player_lost[self.get_enemy_idx()]

    '''

    def get_new_point(self, pos, action, orientation, id):
        factor = 0

        if action == tron.ACTION_TURN_LEFT:
            factor = -90
        elif action == tron.ACTION_TURN_RIGHT:
            factor = 90

        orientation = (orientation + factor) % 360
        x, y = pos

        if orientation == 0:
            y -= 1
        elif orientation == 90:
            x += 1
        elif orientation == 180:
            y += 1
        else:
            x -= 1

        return orientation, tron.Point(x, y)


    def get_new_field_node(self, parent, p1move, p2move):
        field = np.clone(parent.field)

        score = -1

        p1o, p1p = self.get_new_point(parent.p_position, p1move, parent.orientation[self.get_player_idx()-1], self.get_player_idx())
        if field[p1p.y,p1p.x] == 0:
            score = 0
        else:
            field[p1p.y, p1p.x]=self.get_player_idx()

        p2o , p2p=self.get_new_point(parent.position[self.get_enemy_idx()-1],p2move,parent.orientation[self.get_enemy_idx()-1],self.get_enemy_idx())
        if field[p2p.y,p2p.x] == 0:
            score=1
        else:
            field[p2p.y, p2p.x]=self.get_player_idx()

        if score==-1:
            score=self.get_game_score(field, p1p, p2p, self.get_player_idx(), self.get_enemy_idx())

        return tree_node(field, score, [p1o,p2o], [p1p,p2p])





    def get_next_move(self, game, game_state):

        field=np.copy(game_state.game_field)
        orientation=game_state.player_orientation
        position=game_state.player_pos
        tree = tree_node(field, 0, orientation[self.get_player_idx()-1], position[self.get_player_idx()-1], orientation[self.get_enemy_idx()-1], position[self.get_enemy_idx()-1])

        for p1_move in range(3):
            for p2_move in range(3):

                tree.add_node(self.get_new_field_node(tree, 0, p1_move, p2_move))
    '''


'''

training_file = ""

callcount = 0

def get_training_file(training_level = 0,specific=None):

    if specific is not None:
        return specific

    if "level" in sys.argv:
        pos = sys.args.index("level")
        training_level = sys.args[pos + 1]

    if training_level < 0:
        training_level = random.randint(0, training_level*-1)

    subfoldername = "100x100_Single_Level{}_block10000".format(training_level)
    path = "../Data/" + subfoldername + "/"

    #if "download" in sys.argv:
    if True:
        if not os.path.exists(path):
            getTrainingFilesWithThread("OneCharNew", subfoldername, 10)

    return get_random_file(path, [".zip"], avoid=training_file)


knowncharacters = "#0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
charactercount = len(knowncharacters)
max_string_length = 15
learning_rate = 0.000008#0.00004
data_iterations = 100000
batch_training_iters = 1000
batch_size = 512
display_step = 50
dropout = 0.3


def get_data(zipfile, str_len, test_count=5):
    x_data, y_data = generate_training_pairs(zipfile, knowncharacters, str_len)
    return split_train_test(x_data, y_data, test_count)


def print_data_outputs(p_x, p_y):
    result = sess.run(model_out_with_softmax, feed_dict={x_pretrain: p_x, y_pretrain: p_y, keep_prob: 1.})
    result = np.swapaxes(result, 0, 1)
    for out, real_out in zip(result, p_y):
        print("Net_Output:", net_output_to_string(out.tolist(), knowncharacters), " (", net_output_to_string(real_out, knowncharacters), ") ")


def test(x_train,y_train,x_test,y_test):
    cost_val = sess.run(cost, feed_dict={x_pretrain: x_train, y_pretrain: y_train, keep_prob: 1.})
    print("TrainCost: ", cost_val)

    print("TestOut:")
    print_data_outputs(x_test, y_test)

    print("TrainOut:")
    batch_x, batch_y = get_batch(x_train, y_train, 5)
    print_data_outputs(batch_x, batch_y)


keep_prob = tf.placeholder(tf.float32)

######## setup pretrain
x_pretrain = tf.placeholder(tf.float32, [None, 100, 100, 3])
y_pretrain = tf.placeholder(tf.float32, [None, 1, charactercount])
model_out_with_softmax, cost = get_single_digit_model(x_pretrain, y_pretrain, charactercount, keep_prob)

####### setup
#x = tf.placeholder(tf.float32, [None, 100, 300, 3])
#y = tf.placeholder(tf.float32, [None, max_string_length, charactercount])
#model_out_with_softmax, cost = get_multi_digit_model(x, y, max_string_length, charactercount, keep_prob)


optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

modelname = "testmodel"
variables = ['alx_conv1/kernel:0', 'alx_conv1/bias:0', 'alx_norm1/beta:0', 'alx_norm1/gamma:0', 'alx_norm1/moving_mean:0', 'alx_norm1/moving_variance:0', 'alx_conv2/kernel:0', 'alx_conv2/bias:0', 'alx_norm2/beta:0', 'alx_norm2/gamma:0', 'alx_norm2/moving_mean:0', 'alx_norm2/moving_variance:0', 'alx_conv3/kernel:0', 'alx_conv3/bias:0', 'alx_conv4/kernel:0', 'alx_conv4/bias:0', 'alx_conv5/kernel:0', 'alx_conv5/bias:0', 'alx_norm3/beta:0', 'alx_norm3/gamma:0', 'alx_norm3/moving_mean:0', 'alx_norm3/moving_variance:0', 'alx_dense1/kernel:0', 'alx_dense1/bias:0', 'alx_dense2/kernel:0', 'alx_dense2/bias:0', 'alx_dense_last0/kernel:0', 'alx_dense_last0/bias:0', 'beta1_power:0', 'beta2_power:0']

#print([n.name for n in sess.graph.get_operations()])


def load_check():
    if "load" in sys.argv:
        print("loading model")
        load_Model(sess, modelname, variables)


def save_check():
    print("Saving model...")
    save_Model(sess, modelname, variables)
    #save_Model_all(sess, modelname)
    if "upload" in sys.argv:
        pos = sys.argv.index("upload")
        upload_state(sys.argv[pos + 1], sys.argv[pos + 2])

training_level = 0

def train(data_it,x_train,y_train,x_test,y_test,training_file):
    for step in range(batch_training_iters):
        batch_x, batch_y = get_batch(x_train, y_train, batch_size)
        sess.run(optimizer, feed_dict={x_pretrain: batch_x, y_pretrain: batch_y, keep_prob: dropout})
        if step % display_step == 0:
            cost_val = sess.run(cost, feed_dict={x_pretrain: x_train, y_pretrain: y_train, keep_prob: 1.})
            print("TestCost: ", cost_val)


def get_results():
    batch_x, batch_y, _, _ = get_data("../Data/testL1.zip", 1, 0)
    print_data_outputs(batch_x, batch_y)


def get_new_dataset(data_it,x_train,y_train,x_test,y_test):
    training_level = (int)(data_it/20)
    #if training_level > 8:
    #    training_level = 8
    #training_level = training_level % 5
    #print(training_level)
    training_level = random.randint(0, 5)
    training_file = get_training_file(training_level)#, specific="../Data/Data1.zip")

    x_train_result, y_train_result, x_test_result, y_test_result = get_data(training_file, 1)#max_string_length

    if (data_it != 0): #keep test set
        x_test_result = x_test
        y_test_result = y_test

    print("loaded new dataset", training_file)


    return x_train_result, y_train_result, x_test_result, y_test_result

x_train,y_train,x_test,y_test =None,None,None,None

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    load_check()

    #get_results()

    for data_it in range(data_iterations):
        x_train, y_train, x_test, y_test = get_new_dataset(data_it,x_train,y_train,x_test,y_test)
        train(data_it,x_train,y_train,x_test,y_test,training_file)

        print("Iter:", (data_it+1) * batch_training_iters, "blocknumber:", data_it + 1)
        test(x_train, y_train, x_test, y_test)

        save_check()

    print("Finished!")

'''
