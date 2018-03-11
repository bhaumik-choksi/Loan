import pandas as pd
import numpy as np
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder, Normalizer
from keras.layers import Dense, BatchNormalization
from keras.models import Sequential
import pickle


class Predictor:
    def __init__(self):
        return

    def predict(self, *args, **kwargs):
        all_attributes = ['status_of_account', 'duration', 'history', 'purpose', 'amount', 'saving_bonds',
                          'employment', 'rate', 'status_sex', 'other_coap', 'resi_since', 'property', 'age',
                          'other_plans', 'housing', 'existing_credits', 'job', 'liability',
                          'telephone', 'foreign']
        numerical_attributes = ['duration', 'amount', 'rate', 'resi_since', 'age', 'existing_credits', 'liability']

        encoders = pickle.load(open("Models/encoder.p", "rb"))
        normalizers = pickle.load(open("Models/normalizer.p", "rb"))

        arr = np.asarray([])

        for attr in all_attributes:
            if attr not in numerical_attributes:
                le = encoders[attr]["encoder"]
                numerical_col = le.transform(np.asarray([kwargs[attr]]).reshape(-1, 1))
                cat_col = to_categorical(numerical_col, encoders[attr]["n_classes"])
                arr = np.append(arr, cat_col)
            else:
                N = normalizers[attr]
                temp = np.asarray(np.array(int(kwargs[attr])).reshape(-1, 1))
                temp = N.transform(temp)
                temp = np.asarray(temp).reshape(-1, 1)
                arr = np.append(arr, temp)

        input_vector = np.asarray(arr).reshape(-1, 61)

        model_1 = Sequential()
        model_1.add(Dense(200, input_dim=input_vector.shape[1]))
        model_1.add(BatchNormalization())
        model_1.add(Dense(500))
        model_1.add(Dense(500))
        model_1.add(Dense(2, activation="softmax"))
        model_1.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
        model_1.load_weights('Models/model_1.h5')

        model_2 = Sequential()
        model_2.add(Dense(200, input_dim=input_vector.shape[1]))
        model_2.add(BatchNormalization())
        model_2.add(Dense(500))
        model_2.add(Dense(500))
        model_2.add(Dense(2, activation="softmax"))
        model_2.compile(loss="categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])
        model_2.load_weights('Models/model_2.h5')

        model_3 = Sequential()
        model_3.add(Dense(200, input_dim=input_vector.shape[1]))
        model_3.add(BatchNormalization())
        model_3.add(Dense(500))
        model_3.add(Dense(500))
        model_3.add(Dense(2, activation="softmax"))
        model_3.compile(loss="categorical_crossentropy", optimizer="sgd", metrics=["accuracy"])
        model_3.load_weights('Models/model_3.h5')

        op1 = model_1.predict(input_vector)
        op2 = model_2.predict(input_vector)
        op3 = model_3.predict(input_vector)

        # 0th index is risky. 1st index is safe.
        positive = 100*(op1[0][1] + op2[0][1] + op3[0][1])/3
        negative = 100*(op1[0][0] + op2[0][0] + op3[0][0])/3
        if positive < negative:
            category = "risky"
        else:
            category = "safe"
        return {
            "category": category,
            "confidence": max(positive, negative)
        }