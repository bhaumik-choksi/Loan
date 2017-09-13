import tensorflow as tf
import numpy as np
import pandas as pd

tf.reset_default_graph()

def normalize(arr):
    arr = np.asarray(list(map((lambda x: (x - np.min(arr)) / (np.max(arr) - np.min(arr))), arr)))
    return arr


def intify_categories(arr):
    unique_items = list(set(arr))
    mapping = {}
    i = 0
    for unique_item in unique_items:
        mapping[unique_item] = i
        i += 1

    output = list(map((lambda x: mapping[x]), arr))
    return output


data = pd.read_csv("loan_small.csv",
                   usecols=["loan_amnt",
                            "term",
                            "installment",
                            "annual_inc",
                            "dti",
                            "loan_status",
                            'dti',
                            'delinq_2yrs',
                            'inq_last_6mths',
                            'open_acc',
                            'total_acc'
                            ])

NUM_FEATURES = data.shape[1] - 1
data = data[data.loan_status != "Current"]
status = data['loan_status']
bad = ["Late (16-30 days)", "Default", "Late (31-120 days)", "Charged Off", 'In Grace Period']
status = status.apply(lambda x: 0 if x in bad else 1)

print("Total num vals ", data.shape[0])
data["term"] = data["term"].apply((lambda x: int(x.replace(" months", ""))))
data['total_acc'] = data['total_acc'].fillna(0)
del data["loan_status"]
in_data = normalize(np.asarray(data)).reshape(data.shape[0], 1, NUM_FEATURES)
status = np.asarray(status).reshape(data.shape[0], 1, 1)
print(in_data.shape, status.shape)

LEARNING_RATE = 0.1
STEPS = 5
BATCH_SIZE = 100
DISPLAY_STEP = 1

n_hidden_1 = 100
n_hidden_2 = 100
num_input = NUM_FEATURES
num_outputs = 1

X = tf.placeholder("float", [None, num_input])
Y = tf.placeholder("float", [None, 1])

with tf.name_scope("Weights"):
    weights = {
        'h1': tf.Variable(tf.random_normal([num_input, n_hidden_1])),
        'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
        'out': tf.Variable(tf.random_normal([n_hidden_2, num_outputs]))
    }

with tf.name_scope("Biases"):
    biases = {
        'b1': tf.Variable(tf.random_normal([n_hidden_1])),
        'b2': tf.Variable(tf.random_normal([n_hidden_2])),
        'out': tf.Variable(tf.random_normal([num_outputs]))
    }

with tf.name_scope("Neural_Network"):
    def neural_net(x):
        layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
        layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
        output_layer = tf.matmul(layer_2, weights['out']) + biases['out']
        return output_layer

with tf.name_scope("Prediction"):
    logit = neural_net(X)
    prediction = tf.nn.softmax(neural_net(X))

with tf.name_scope("Optimizer"):
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=logit, labels=Y))
    optimizer = tf.train.RMSPropOptimizer(learning_rate=LEARNING_RATE)
    train_op = optimizer.minimize(loss)

with tf.name_scope("Metrics"):
    correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init_variables = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init_variables)
    for step in range(1, STEPS + 1):
        t_i, t_o = [None, None]

        for (i, o) in list(zip(in_data, status)):
            sess.run(train_op, feed_dict={X: i, Y: o})
            t_i, t_o = [i, o]

        if step % DISPLAY_STEP == 0 or step == 1:
            loss_at_step, acc = sess.run([loss, accuracy], feed_dict={X: t_i, Y: t_o})
            print("Step", step, "Loss", loss_at_step, "Acc", acc)

    writer = tf.summary.FileWriter('my_graph', sess.graph)
    writer.add_graph(sess.graph)
    writer.close()

    sess.close()
    print("Training complete!")

