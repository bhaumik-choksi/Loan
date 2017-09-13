import tensorflow as tf
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
import keras.callbacks as K
from keras.utils.np_utils import to_categorical
import math

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
                            # 'dti',
                            # 'delinq_2yrs',
                            # 'inq_last_6mths',
                            # 'open_acc',
                            # 'total_acc'
                            ])
NUM_FEATURES = data.shape[1]-1
data = data[data.loan_status != "Current"]
status = data['loan_status']
# bad = ["Late (16-30 days)", "Default","Late (31-120 days)","Charged Off",'In Grace Period']
# status = status.apply(lambda x: 0 if x in bad else 1)

status = intify_categories(list(status))
status = to_categorical(status)
print("Total num vals ",data.shape[0], "looooool ")
data["term"] = data["term"].apply((lambda x: int(x.replace(" months", ""))))
# data['total_acc'] = data['total_acc'].fillna(0)
del data["loan_status"]
in_data = normalize(np.asarray(data)).reshape(data.shape[0], 1, NUM_FEATURES)
status = np.asarray(status).reshape(data.shape[0], 1, 6)
print(in_data.shape, status.shape)

tf.reset_default_graph()

model = Sequential()
model.add(Dense(500,input_shape=(None, NUM_FEATURES), name="input_dense_layer"))
model.add(Dense(500, name="hidden_dense_layer"))
model.add(Dense(500))
model.add(Dense(500))
model.add(Dense(500))
model.add(Dense(500))
model.add(Dense(500))
model.add(Dense(6,activation="softmax",name="output_dense_layer"))
model.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=['accuracy'])
model.fit(in_data, status, callbacks=[K.TensorBoard(log_dir="./my_graph")], epochs=10, batch_size=50)
model.summary()
