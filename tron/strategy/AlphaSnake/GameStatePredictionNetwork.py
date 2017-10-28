import tensorflow as tf
import numpy as np

def get_prediction_network_head(input,keep_prob,name_pref):
    conv1 = tf.layers.conv2d(inputs=input, filters=30, kernel_size=[11, 11], strides=[4, 4], padding="same", activation=tf.nn.relu, name=name_pref+"alx_conv1")# 94
    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[3, 3], strides=1, name=name_pref+"alx_pool1")
    drop1 = tf.layers.dropout(inputs=pool1, rate=keep_prob, name=name_pref+"alx_drop1")
    norm1 = tf.layers.batch_normalization(drop1, name=name_pref+"alx_norm1")

    r1 = tf.contrib.layers.flatten(norm1)
    dense1 = tf.layers.dense(inputs=r1, units=8000, name=name_pref+"alx_dense1")
    dense2 = tf.layers.dense(inputs=dense1, units=4000, name=name_pref+"alx_dense2")

    return dense2


def get_prediction_network(input, output, keep_prob, name_pref):
    nn=get_prediction_network_head(input, keep_prob, name_pref)
    out = tf.layers.dense(inputs=nn, units=2, name=name_pref + "output_layer")

    model_out = tf.nn.softmax(out)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=out, labels=output))

    return model_out, cost

    #digit_blocks = []
    #digit_block_costs = []

    #for digit in range(max_str_len):
    #    digit_block = tf.layers.dense(inputs=network_out, units=charactercount, name="alx_dense_last{}".format(digit))
    #    digit_blocks.append(tf.nn.softmax(digit_block))
    #    digit_block_cost = tf.losses.softmax_cross_entropy(output[:,digit], digit_block)
    #    digit_block_costs.append(digit_block_cost)

    #return digit_blocks, tf.add_n(digit_block_costs)


'''
def get_alexnet_model(input,keep_prob,name_pref=""):
    conv1 = tf.layers.conv2d(inputs=input, filters=30, kernel_size=[11, 11], strides=[4, 4], padding="same", activation=tf.nn.relu, name=name_pref+"alx_conv1")# 94
    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[3, 3], strides=1, name=name_pref+"alx_pool1")
    drop1 = tf.layers.dropout(inputs=pool1, rate=keep_prob, name=name_pref+"alx_drop1")
    norm1 = tf.layers.batch_normalization(drop1, name=name_pref+"alx_norm1")

    conv2 = tf.layers.conv2d(inputs=norm1, filters=60, kernel_size=[5, 5], strides=[4, 4], padding="same", activation=tf.nn.relu, name=name_pref+"alx_conv2")# 256
    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[3, 3], strides=1, name=name_pref+"alx_pool2")
    drop2 = tf.layers.dropout(inputs=pool2, rate=keep_prob, name=name_pref+"alx_drop2")
    norm2 = tf.layers.batch_normalization(drop2, name=name_pref+"alx_norm2")

    conv3 = tf.layers.conv2d(inputs=norm2, filters=26, kernel_size=[3, 3], strides=[1, 1], padding="same", activation=tf.nn.relu, name=name_pref+"alx_conv3")
    conv4 = tf.layers.conv2d(inputs=conv3, filters=26, kernel_size=[3, 3], strides=[1, 1], padding="same", activation=tf.nn.relu, name=name_pref+"alx_conv4")
    conv5 = tf.layers.conv2d(inputs=conv4, filters=26, kernel_size=[3, 3], strides=[1, 1], padding="same", activation=tf.nn.relu, name=name_pref+"alx_conv5")
    pool3 = tf.layers.max_pooling2d(inputs=conv5, pool_size=[3, 3], strides=1, name=name_pref+"alx_pool3")
    norm3 = tf.layers.batch_normalization(pool3, name=name_pref+"alx_norm3")

    r1 = tf.contrib.layers.flatten(norm3)
    dense1 = tf.layers.dense(inputs=r1, units=8000, name=name_pref+"alx_dense1")
    dense2 = tf.layers.dense(inputs=dense1, units=4000, name=name_pref+"alx_dense2")

    return dense2


def get_input_slide_alx_net(input, step, charactercount,keep_prob):
    with tf.variable_scope("CharacterAlexnet") as scope:

        shape = input.get_shape().as_list()
        height = shape[1]
        width = shape[2]

        hd2 = (int)(height / 2)
        subnets = []
        x_pos = 0

        while x_pos < width:

            xmin = x_pos - hd2
            xmax = x_pos + hd2

            if xmin < 0:
                block = input[:, :, 0:-xmin, :]
                inp = tf.concat([block, input[:, :, 0:xmax, :]], 2)
            elif xmax > width:
                block = input[:, :, width - xmax:width, :]
                inp = tf.concat([block, input[:, :, xmin:width, :]], 2)
            else:
                inp = input[:, :, xmin:xmax, :]

            alx = get_alexnet_model(inp,keep_prob)
            character_poss = tf.layers.dense(inputs=alx, units=charactercount, name="alx_dense_last")
            c = tf.nn.softmax(character_poss)
            subnets.append(c)
            scope.reuse_variables()
            x_pos += step

    concat = tf.concat(subnets, 1)
    return tf.contrib.layers.flatten(concat)


def get_output_layers_and_cost_multipledigit(network_out, max_str_len, charactercount, output):
    digit_blocks = []
    digit_block_costs = []

    for digit in range(max_str_len):
        digit_block = tf.layers.dense(inputs=network_out, units=charactercount, name="alx_dense_last{}".format(digit))
        digit_blocks.append(tf.nn.softmax(digit_block))
        digit_block_cost = tf.losses.softmax_cross_entropy(output[:,digit], digit_block)
        digit_block_costs.append(digit_block_cost)

    return digit_blocks, tf.add_n(digit_block_costs)


def get_picture_preprocess_Network(input, keep_prob):
    with tf.variable_scope("PreprocessAlexnet") as scope:
        alx = get_alexnet_model(input, keep_prob, name_pref="pp")
    return alx

def get_final_multidigit_dense_net(input, output, max_str_len, charactercount):
    with tf.variable_scope("FinalDenseNet") as scope:
        dense1 = tf.layers.dense(inputs=input, units=4000, name="dense1")
        dense2 = tf.layers.dense(inputs=dense1, units=2000, name="dense2")
        dense3 = tf.layers.dense(inputs=dense2, units=1000, name="dense2")
    return get_output_layers_and_cost_multipledigit(dense3, max_str_len, charactercount, output)

def get_multi_digit_model(input, output, max_str_len, charactercount, keep_prob):
    slide_alx = get_input_slide_alx_net(input=input, step=5, charactercount=charactercount, keep_prob=keep_prob)#fuer w=300, step=5: 3720
    preprocess_alx = get_picture_preprocess_Network(input=input, keep_prob=keep_prob)
    concat = tf.concat([slide_alx, preprocess_alx], 1)
    return get_final_multidigit_dense_net(concat, output, max_str_len, charactercount)


def get_single_digit_model(input, output, charactercount, keep_prob):
    shape = input.get_shape().as_list()
    if shape[1] != shape[2]:
        print("warning: no quadratic training input")
    alx = get_alexnet_model(input, keep_prob)
    return get_output_layers_and_cost_multipledigit(alx, 1, charactercount, output)

'''

