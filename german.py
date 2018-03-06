import pandas as pd
import numpy as np
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder, Normalizer
from keras.layers import Dense, BatchNormalization
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier


# Read raw excel data. 1000 tuples.
raw_data = pd.read_excel('german.xlsx')

# Print col names
print("Number of features including output ",len(raw_data.columns.values))
print(raw_data.columns.values)

# Extract status into a separate DF. Delete from main DF.
raw_output_status = raw_data['status'].apply(lambda x: 0 if x==2 else x)
del raw_data["status"]
# print(np.count_nonzero(np.asarray(raw_output_status)))

# One-Hot output
output_status = to_categorical(raw_output_status)


all_attributes = raw_data.columns.values
numerical_attributes = ['duration', 'amount', 'rate', 'resi_since', 'age', 'existing_credits', 'liability']

arr = np.zeros(shape=(1000,1))

for attr in all_attributes:
    if attr not in numerical_attributes:
        le = LabelEncoder()
        numerical_col = le.fit_transform(raw_data[attr])
        cat_col = to_categorical(numerical_col)
        arr = np.hstack((arr, cat_col))
    else:
        N = Normalizer()
        temp = np.asarray(raw_data[attr].reshape(-1, 1))
        temp = N.fit_transform(temp)
        temp = np.asarray(temp).reshape(-1,1)
        arr = np.hstack((arr, temp))



good_data = np.asarray(arr)
good_data = np.delete(good_data, 0, 1)



# x_train, x_test, y_train, y_test = train_test_split(good_data, output_status, test_size=0.2, stratify=output_status)

x_train, x_test, y_train, y_test = train_test_split(good_data, raw_output_status, test_size=0.2, stratify=raw_output_status)


# model = Sequential()
# model.add(Dense(200, input_dim=good_data.shape[1]))
# model.add(BatchNormalization())
# model.add(Dense(500))
# model.add(Dense(500))
# model.add(Dense(2, activation="softmax"))
# model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
# model.fit(x_train, y_train, epochs=50, batch_size=5)
# scores = model.evaluate(np.array(x_test), np.array(y_test), verbose=0)
# print("TEST SCORE")
# print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

clf = SVC()
clf.fit(x_train,y_train)
print("Score with Support Vector Classifier", clf.score(x_test, y_test))

clf2 = GaussianNB()
clf2.fit(x_train,y_train)
print("Score with Naive Bayes", clf2.score(x_test, y_test))

clf3 = KNeighborsClassifier()
clf3.fit(x_train,y_train)
print("Score with KNN", clf3.score(x_test, y_test))
