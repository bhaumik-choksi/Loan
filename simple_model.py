import tensorflow as tf
import pandas as pd
import numpy as np

data = pd.read_csv('loan_small.csv')
amnt = data['loan_amnt']
status = data['loan_status']
bad = ["Charged Off","Late (16-30 days)","Default","Late (31-120 days)"]
status = status.apply(lambda x: 0 if x in bad else 1)
income = data['annual_inc']

# Params
learning_rate = 0.01
training_epochs = 5
batch_size = 100
display_step = 1
num = len(amnt)

tf.reset_default_graph()

inp = np.asarray(amnt)/np.asarray(income)
op = status.values

x = tf.placeholder(dtype=tf.float32, name="Input")
y = tf.placeholder(dtype=tf.float32, name="Output")

W = tf.Variable(1.0, name="Weights")
b = tf.Variable(1.0, name="Biases")

with tf.name_scope("Basic_model"):
    pred = tf.nn.sigmoid(tf.multiply(x, W) + b)
    cost = tf.reduce_mean(tf.pow(y - pred, 2))
    optimizer = tf.train.RMSPropOptimizer(learning_rate).minimize(cost)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for (i, o) in zip(inp, op):
        sess.run(optimizer, feed_dict={x:i, y:o})
    print(sess.run(pred, feed_dict={x:0.5}))
    writer = tf.summary.FileWriter('./my_graph/', sess.graph)
    writer.add_graph(sess.graph)
    writer.close()