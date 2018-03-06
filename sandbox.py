import numpy as np
import pandas as pd
from keras.utils import to_categorical
data = pd.read_excel('sandbox.xlsx')

def npize(a):
    return np.asarray(a)

p = data['A1']
q = data['A2']


pc = to_categorical(p)

print(pc)

q = npize(q).reshape(-1,1)

z = np.hstack((pc,q))
print(z)