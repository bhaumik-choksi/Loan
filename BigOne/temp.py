import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize,minmax_scale,Normalizer
import math
import numpy as np
from numpy.linalg import norm as no

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

    def normalizee(arr):
        mean = sum(arr)/len(arr)
        print(np.std(arr))
        sd = math.sqrt(sum(list(map((lambda x: (x-mean)**2), arr)))/len(arr))
        print(sd)
        mmm = min(arr)
        arr = list(map((lambda x: (x-mmm)/(max(arr)-min(arr))), arr))
        return arr


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
        'total_acc'])

    data['term'] = data['term'].apply(lambda x : int(x.replace("months","").strip()))
    data['mths_since_last_delinq'] = data['mths_since_last_delinq'].fillna(0)
    data['emp_length'] = intify_categories(data['emp_length'])
    data['home_ownership'] = intify_categories(data['home_ownership'])
    data['verification_status'] = intify_categories(data['verification_status'])
    data['purpose'] = intify_categories(data['purpose'])
    print(data.dtypes)
    for index,row in data.iterrows():
        row = row.fillna(0)
    data = np.asarray(data)
    test = np.array([1,2,3,4,5])
    print(list(map()))
    print(normalize([1,2,3,4,5]))
    return data

get_data()
