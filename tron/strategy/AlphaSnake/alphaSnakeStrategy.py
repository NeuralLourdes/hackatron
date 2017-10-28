import sys
import os
import numpy as np
import tensorflow as tf
#from tfsave import *
import random
from strategy import player_game
import strategy.AlphaSnake.GameStatePredictionNetwork as gspn
from strategy.AlphaSnake.AlphaSnakeHelper import *

learning_rate = 0.000008

class alphaSnakeStrategy(player_game.PlayerStrategy):

    def __init__(self, player_idx, width, height):
        super(alphaSnakeStrategy, self).__init__(player_idx)

        self.game_stat_buffer=[]
        self.keep_prob_tensor = tf.placeholder(tf.float32)
        self.input_tensor = tf.placeholder(tf.float32, [None, height, width, 4])
        self.output_tensor = tf.placeholder(tf.float32, [None, 2])
        self.model_out_with_softmax_tensor, self.cost_tensor = gspn.get_prediction_network(self.input_tensor, self.output_tensor, self.keep_prob_tensor,"ASPN"+str(player_idx))
        self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.cost_tensor)

        self.tf_sess = tf.Session()
        self.tf_sess.run(tf.global_variables_initializer())


    def get_action(self, game, game_state, other = None):
        p1pos = game_state.player_pos[self.get_player_idx()]
        p2pos = game_state.player_pos[self.get_enemy_idx()]
        train_mat = get_training_matrix(game_state.game_field, p1pos, p2pos, self.get_player_idx(), self.get_enemy_idx())

        self.game_stat_buffer.append(train_mat)

        #print(np.shape(train_mat))

        #print(game.get_available_actions())
        return 2

    def train(self, x_train, y_train, x_test, y_test, dropout):
        batch_training_iters=1
        #for step in range(batch_training_iters):
            #batch_x, batch_y = x_train, y_train

        print(self.input_tensor)
        print(np.shape(x_train))

        self.tf_sess.run(self.optimizer, feed_dict={self.input_tensor: x_train, self.output_tensor: y_train, self.keep_prob_tensor: dropout})

        #cost_val = self.tf_sess.run(self.cost_tensor, feed_dict={x_pretrain: x_train, y_pretrain: y_train, keep_prob: 1.})
        #print("TestCost: ", cost_val)

        print("trained")

    def on_game_over(self, game, game_state):

        print("over")

        if len(self.game_stat_buffer)>0:

            train_inp = self.game_stat_buffer
            train_outp = np.ones((len(self.game_stat_buffer),2))*(self.player_has_won(game), self.enemy_has_won(game))

            self.train(train_inp, train_outp, None, None, 0.9)

            self.game_stat_buffer=[]


    def game_is_over(self, game):
        return game.game_over()

    def player_has_won(self, game):
        return game.player_lost[self.get_player_idx()]

    def enemy_has_won(self, game):
        return game.player_lost[self.get_enemy_idx()]


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
