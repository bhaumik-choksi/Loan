import tensorflow as tf
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import LSTM
from keras.layers import RepeatVector
from keras.layers import Permute
from sklearn.preprocessing import normalize
import keras.callbacks as K

data = pd.read_csv("loan_small.csv",
                   usecols=["loan_amnt",
                            "term",
                            "installment",
                            "annual_inc",
                            "dti",
                            "loan_status"
                            ])

status = data['loan_status']
print(set(status))
bad = ["Charged Off","Late (16-30 days)","Default","Late (31-120 days)"]
status = status.apply(lambda x: 0 if x in bad else 1)

data["term"] = data["term"].apply((lambda x : int(x.replace(" months",""))))

del data["loan_status"]
in_data = normalize(np.asarray(data)).reshape(10000,1,5)
status = np.asarray(status).reshape(10000,1,1)
print(in_data.shape,status.shape)

tf.reset_default_graph()

model = Sequential()
model.add( Dense(5,input_shape=(None,5),name="input_dense_layer") )
model.add(Dense(5,name="hidden_dense_layer") )
model.add(Dense(1,activation="sigmoid",name="output_dense_layer"))
model.compile(optimizer="adam",loss="mse",metrics=['accuracy'])
model.fit(in_data,status,callbacks=[K.TensorBoard(log_dir="./my_graph")],epochs=100,batch_size=10)
model.summary()