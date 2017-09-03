import tensorflow as tf
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Params
num_features = 18
num_classes = 1
no_hidden_1 = 128
no_hidden_2 = 128
learning_rate = 0.1

X = tf.placeholder(tf.float32, shape=[None, num_features])
Y = tf.placeholder(tf.float32, shape=[None, num_classes])


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
	path = "loan_small.csv"
	data = pd.read_csv(path, usecols = ['loan_amnt', 'term', 'int_rate', 'installment', 'emp_length', 
			'home_ownership', 'annual_inc', 'verification_status', 'purpose', 'dti', 'delinq_2yrs',
			'inc_last_6mths', 'mths_since_last_delinq', 'open_acc', 'pub_rec', 'revol_bal', 'revol_util'
			'total_acc'])

    return x,y


def neural_net(X):
    with tf.name_scope("Layer_1"):
        # Hidden fully connected layer with 128 neurons
        layer_1 = tf.add(tf.matmul(X, weights['h1']), biases['b1'])
        # Hidden fully connected layer with 128 neurons
        layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
        # Output fully connected layer
        out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
        return out_layer


y_pred = tf.sigmoid(neural_net(X))

cost = tf.reduce_mean(-tf.reduce_sum(Y*tf.log(y_pred), reduction_indices=1))
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    inp, op = get_input()
    for (i, o) in zip(inp, op):
        sess.run(optimizer, feed_dict={x:i, y:o})