import pandas as pd
import os
from glob import glob
import shutil

rnn_type = 'gru'
year = 2022
# result_path = '/Users/zimenglyu/Documents/cluster_results/DJI_Company_2023_lr'
prediction_path = f"/Users/zimenglyu/Documents/cluster_results/{rnn_type}_prediction_{year}"

best_mse = 100
overall_mse = []
if not os.path.exists(prediction_path):
    os.makedirs(prediction_path)
    print("Created directory: {}".format(prediction_path))

for stock in ['AAPL', 'AXP', 'BA', 'CAT', 'CSCO', 'CVX', 'DOW', 'DIS', 'WBA', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE',  'PG', 'TRV', 'UNH',  'VZ', 'V', 'WMT', 'HON', 'AMZN', 'CRM']:
    print("Processing stock: {}".format(stock))
    best_mse = 100
    for i in range(10):
        fitness_filepath = f"/Users/zimenglyu/Documents/code/git/exact/DJI_Company/{year}_{rnn_type}/{stock}/{i}"
        if os.path.exists(fitness_filepath) and os.path.isdir(fitness_filepath):

            df = pd.read_csv("{}/fitness.csv".format(fitness_filepath))
            mse = df[' BEST Val. MSE'].iloc[-1]
            if mse < best_mse:
                best_mse = mse
                prediction_file_path = f"{fitness_filepath}/{stock}_test_predictions.csv"
    overall_mse.append(best_mse)
    prediction_file = os.path.join(prediction_path, "{}_predictions.csv".format(stock))
    shutil.copy(prediction_file_path, prediction_file)
    print("copied {} to {}".format(prediction_file_path, prediction_file))

print("Overall best MSE: {}".format(sum(overall_mse) / len(overall_mse)))
    

