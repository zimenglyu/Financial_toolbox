import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error 
from glob import glob

# data_path = ''
# data = pd.read_csv(data_path)

# expected = data.iloc[:, 1]
# predicted = data.iloc[:, 2]

# mse = mean_squared_error(expected, predicted)
# print("Mean Squared Error of prediction: {:.6f}".format(mse))

# mse_naive = mean_squared_error(expected[1:], expected[:-1])
# print("Mean Squared Error of naive prediction: {:.6f}".format(mse_naive))

# data_dir = '/Users/zimenglyu/Documents/cluster_results/DJI_Company_2023_lr_prediction'
# files = glob(data_dir + "/*.csv")
# overall_mse = []
# for file in files:
#     data = pd.read_csv(file)
#     expected = data["expected_RET"]
#     predicted = data["predicted_RET"]

#     mse = mean_squared_error(expected, predicted)
#     print("Mean Squared Error of prediction: {:.6f}".format(mse))
#     overall_mse.append(mse)
# print("Overall Mean Squared Error: {:.6f}".format(sum(overall_mse) / len(overall_mse)))
stock_names = ['AAPL', 'AMZN', 'AXP', 'BA', 'CAT', 'CSCO', 'CVX', 'DOW', 'DIS', 'WBA', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE',  'PG', 'TRV', 'UNH',  'VZ', 'V', 'WMT',  'HON', 'CRM']
prediction_dir = '/Users/zimenglyu/Downloads/TESTING_FILES/SVR'
expected_dir = '/Users/zimenglyu/Documents/datasets/CRSP/DJI_company_2023/test'
overall_mse = []
for stock in stock_names:
    prediction_file = f'{prediction_dir}/{stock}.csv'
    expected_file = f'{expected_dir}/{stock}.csv'
    # files = glob(data_dir + "/*.csv")
    expected_data = pd.read_csv(expected_file)
    prediction_data = pd.read_csv(prediction_file)

    expected = expected_data["RET"]
    predicted = prediction_data["Predicted_RET"]

    mse = mean_squared_error(expected, predicted)
    print("Mean Squared Error of prediction: {:.6f}".format(mse))
    overall_mse.append(mse)
print("Overall Mean Squared Error: {:.6f}".format(sum(overall_mse) / len(overall_mse)))


