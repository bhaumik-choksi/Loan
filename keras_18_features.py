import tensorflow as tf
import pandas as pd
import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.callbacks import TensorBoard
from keras.utils import to_categorical
from sklearn.preprocessing import normalize


def get_data():
    path = "loan_small.csv"

    def intify_categories(arr):
        unique_items = list(set(arr))
        mapping = {}
        i = 0
        for unique_item in unique_items:
            mapping[unique_item] = i
            i += 1

        output = list(map((lambda x: mapping[x]), arr))
        return output

    data = pd.read_csv(path, usecols=['loan_amnt',
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

    bad = ["Charged Off", "Late (16-30 days)", "Default", "Late (31-120 days)"]
    outputs = data['loan_status'].apply(lambda x : 0 if x in bad else 1)
    del data['loan_status']

    data['loan_amnt'] = data['loan_amnt'].fillna(0).apply(normalize)
    data['term'] = data['term'].apply(lambda x: int(x.replace("months", "").strip())).fillna(0).apply(normalize)
    data['int_rate'] = data['int_rate'].fillna(0).apply(normalize)
    data['installment'] = data['installment'].fillna(0).apply(normalize)
    data['emp_length'] = intify_categories(data['emp_length'].fillna(0))
    data['emp_length'].apply(normalize)
    data['home_ownership'] = intify_categories(data['home_ownership'].fillna(0))
    data['home_ownership'].apply(normalize)
    data['annual_inc'] = data['annual_inc'].fillna(0).apply(normalize)
    data['verification_status'] = intify_categories(data['verification_status'].fillna(0))
    data['verification_status'].apply(normalize)
    data['purpose'] = intify_categories(data['purpose'].fillna(0))
    data['purpose'].apply(normalize)
    data['dti'] = data['dti'].fillna(0).apply(normalize)
    data['delinq_2yrs'] = data['delinq_2yrs'].fillna(0).apply(normalize)
    data['inq_last_6mths'] = data['inq_last_6mths'].fillna(0).apply(normalize)
    data['mths_since_last_delinq'] = data['mths_since_last_delinq'].fillna(0).apply(normalize)
    data['open_acc'] = data['open_acc'].fillna(0).apply(normalize)
    data['pub_rec'] = data['pub_rec'].fillna(0).apply(normalize)
    data['revol_bal'] = data['revol_bal'].fillna(0).apply(normalize)
    data['revol_util'] = data['revol_util'].fillna(0).apply(normalize)
    data['total_acc'] = data['total_acc'].fillna(0).apply(normalize)

    outputs = normalize(outputs)

    data = np.asarray(data).reshape(-1, 1, 18)

    outputs = np.asarray(outputs).reshape(-1, 1, 1)
    return data, outputs


inputs, outputs = get_data()
# outputs = outputs.reshape(outputs.shape[0], 1, outputs.shape[1])
model = Sequential()
model.add(Dense(128, input_shape=(None, 18)))
model.add(Dense(128))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer="rmsprop", loss="mse", metrics=["accuracy"])
model.fit(inputs, outputs)
