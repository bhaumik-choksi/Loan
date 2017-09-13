import tensorflow as tf
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def get_data():
    path = "loan_small.csv"

    def intify_categories(arr):
        unique_items = list(set(arr))
        mapping = {}
        i = 0
        for unique_item in unique_items:
            mapping[unique_item] = i
            i += 1

        output = list(map((lambda x : mapping[x]),arr))
        return output

    data = pd.read_csv(path, usecols = ['loan_amnt',
        'term',
        'int_rate',
        'installment',
        'emp_length',
        'home_ownership',
        'annual_inc',
        'verification_status',
        'purpose',
        'dti',
        'delinq_2yrs',
        'inq_last_6mths',
        'mths_since_last_delinq',
        'open_acc',
        'pub_rec',
        'revol_bal',
        'revol_util',
        'total_acc',
        'loan_status'
        ])

    data['term'] = data['term'].apply(lambda x : int(x.replace("months","").strip()))
    outputs = intify_categories(data['loan_status'])
    data['emp_length'] = intify_categories(data['emp_length'])
    data['home_ownership'] = intify_categories(data['home_ownership'])
    data['verification_status'] = intify_categories(data['verification_status'])
    data['purpose'] = intify_categories(data['purpose'])
    del data['loan_status']
    print(data.dtypes)
    data = np.asarray(data).reshape(-1, 18)
    outputs = np.asarray(outputs).reshape(-1, 1)
    print(data.shape)
    print(outputs.shape)
    return data, outputs


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


def neural_net(X):
    with tf.name_scope("Layer_1"):
        # Hidden fully connected layer with 128 neurons
        layer_1 = tf.add(tf.matmul(tf.transpose(X), weights['HL1']), biases['b1'])
        # Hidden fully connected layer with 128 neurons
        layer_2 = tf.add(tf.matmul(tf.transpose(layer_1), weights['HL2']), biases['b2'])
        # Output fully connected layer
        out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
        return out_layer


y_pred = tf.sigmoid(neural_net(X))

cost = tf.reduce_mean(-tf.reduce_sum(Y*tf.log(y_pred), reduction_indices=1))
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    inp, op = get_data()
    for i,o in zip(inp,op):
        i = np.asarray(i).reshape(1,len(i))
        o = np.asarray(0).reshape(1,1)
        sess.run(optimizer, feed_dict={X: i, Y: o})