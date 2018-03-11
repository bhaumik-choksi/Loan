import pandas as pd
import numpy as np
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder, Normalizer
from keras.layers import Dense, BatchNormalization
from keras.models import Sequential
from sklearn.model_selection import train_test_split
import pickle

class Trainer:
    def __init__(self):
        return

    def train_all_and_save(self, filename, epochs=20, batch_size=5):
        raw_data = pd.read_excel('../'+filename)
        # Extract status into a separate DF. Delete from main DF.
        raw_output_status = raw_data['status'].apply(lambda x: 0 if x == 2 else x)
        del raw_data["status"]
        # One-Hot output
        output_status = to_categorical(raw_output_status)
        all_attributes = raw_data.columns.values
        numerical_attributes = ['duration', 'amount', 'rate', 'resi_since', 'age', 'existing_credits', 'liability']
        arr = np.zeros(shape=(1000, 1))

        # These dicts store encoders or normalizers for each attribute. Reuse during prediction.
        encoders = {}
        normalizers = {}
        # TODO: Normalization does not work as expected. Fix it.


        for attr in all_attributes:
            if attr not in numerical_attributes:
                le = LabelEncoder()
                numerical_col = le.fit_transform(raw_data[attr])
                cat_col = to_categorical(numerical_col)
                arr = np.hstack((arr, cat_col))
                encoders[attr] = {"encoder":le, "n_classes":len(list(le.classes_))}
            else:
                N = Normalizer()
                temp = np.asarray(raw_data[attr].reshape(-1, 1))
                temp = N.fit_transform(temp)
                temp = np.asarray(temp).reshape(-1, 1)
                arr = np.hstack((arr, temp))
                normalizers[attr] = N

        good_data = np.asarray(arr)

        good_data = np.delete(good_data, 0, 1)

        x_train, x_test, y_train, y_test = train_test_split(good_data, output_status, test_size=0.2,
                                                            stratify=output_status)
        model_1 = Sequential()
        model_1.add(Dense(200, input_dim=good_data.shape[1]))
        model_1.add(BatchNormalization())
        model_1.add(Dense(500))
        model_1.add(Dense(500))
        model_1.add(Dense(2, activation="softmax"))
        model_1.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
        model_1.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)
        scores = model_1.evaluate(np.array(x_test), np.array(y_test), verbose=0)
        print("TEST SCORE 1")
        print("%s: %.2f%%" % (model_1.metrics_names[1], scores[1] * 100))

        x_train, x_test, y_train, y_test = train_test_split(good_data, output_status, test_size=0.2,
                                                            stratify=output_status)
        model_2 = Sequential()
        model_2.add(Dense(200, input_dim=good_data.shape[1]))
        model_2.add(BatchNormalization())
        model_2.add(Dense(500))
        model_2.add(Dense(500))
        model_2.add(Dense(2, activation="softmax"))
        model_2.compile(loss="categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])
        model_2.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)
        scores = model_2.evaluate(np.array(x_test), np.array(y_test), verbose=0)
        print("TEST SCORE 2")
        print("%s: %.2f%%" % (model_2.metrics_names[1], scores[1] * 100))

        x_train, x_test, y_train, y_test = train_test_split(good_data, output_status, test_size=0.2,
                                                            stratify=output_status)
        model_3 = Sequential()
        model_3.add(Dense(200, input_dim=good_data.shape[1]))
        model_3.add(BatchNormalization())
        model_3.add(Dense(500))
        model_3.add(Dense(500))
        model_3.add(Dense(2, activation="softmax"))
        model_3.compile(loss="categorical_crossentropy", optimizer="sgd", metrics=["accuracy"])
        model_3.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)
        scores = model_3.evaluate(np.array(x_test), np.array(y_test), verbose=0)
        print("TEST SCORE 3")
        print("%s: %.2f%%" % (model_3.metrics_names[1], scores[1] * 100))

        model_1.save('../Models/model_1.h5')
        model_2.save('../Models/model_2.h5')
        model_3.save('../Models/model_3.h5')

        pickle.dump(encoders, open("../Models/encoder.p", "wb"))
        pickle.dump(normalizers, open("../Models/normalizer.p", "wb"))

        print("Models trained and saved")
        return True
