import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error 

data_path = ''
data = pd.read_csv(data_path)

expected = data.iloc[:, 1]
predicted = data.iloc[:, 2]

mse = mean_squared_error(expected, predicted)
print("Mean Squared Error of prediction: {:.6f}".format(mse))

mse_naive = mean_squared_error(expected[1:], expected[:-1])
print("Mean Squared Error of naive prediction: {:.6f}".format(mse_naive))

