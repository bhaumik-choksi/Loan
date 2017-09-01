import tensorflow as tf
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Params
num_features = 18
num_classes = 1
no_hidden_1 = 128
no_hidden_2 = 128
learning_rate = 0.001

X_train = tf.placeholder(tf.float32, shape=[None, num_features])
Y_train = tf.placeholder(tf.float32, shape=[None, num_classes])


weights = {

    'HL1': tf.Variable(tf.random_normal([num_features, no_hidden_1])),
    'HL2': tf.Variable(tf.random_normal([num_features, no_hidden_2])),
    'out': tf.Variable(tf.random_normal([no_hidden_2, num_classes]))
}

biases = {

    'b1': tf.Variable(tf.random_normal([no_hidden_1])),
    'b2': tf.Variable(tf.random_normal([no_hidden_2])),
    'out': tf.Variable(tf.random_normal([num_classes]))
}

def get_input():
    pass


def neural_net(X):
    with tf.name_scope("Layer_1"):
        # Hidden fully connected layer with 128 neurons
        layer_1 = tf.add(tf.matmul(X, weights['h1']), biases['b1'])
        # Hidden fully connected layer with 128 neurons
        layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
        # Output fully connected layer
        out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
        return out_layer


x, y_real = get_input()
y_pred = tf.sigmoid(neural_net(x))

cost = tf.reduce_mean(-tf.reduce_sum(y_real*tf.log(y_pred), reduction_indices=1))
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

