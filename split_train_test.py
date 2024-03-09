import pandas as pd
from glob import glob
import os
root_path = "/Users/zimenglyu/Documents/datasets/CRSP/DJI_history_train_vali_test/single_stocks"
file_names = glob(root_path + '/temp/*.csv')

for file in file_names:
    # Step 1: Read the CSV file
    df = pd.read_csv(file, parse_dates=['date'])
    file_name = file.split('/')[-1].split('_13')[0]
    # Step 2: Define your datetime ranges for splitting
    train_start = pd.to_datetime('9/1/2020')
    train_end = pd.to_datetime('12/31/2020')
    validation_start = pd.to_datetime('1/4/2021')
    validation_end = pd.to_datetime('12/31/2021')
    test_start = pd.to_datetime('1/3/2022')
    test_end = pd.to_datetime('12/29/2022')

    # Step 3: Split the DataFrame into train, validation, and test datasets
    # Train dataset
    train_df = df[(df['date'] >= train_start) & (df['date'] <= train_end)]

    # Validation dataset
    validation_df = df[(df['date'] >= validation_start) & (df['date'] <= validation_end)]

    # Test dataset
    test_df = df[(df['date'] >= test_start) & (df['date'] <= test_end)]

    # Optional: Save these datasets to new CSV files if needed
    train_df.to_csv("{}/{}/{}_13.csv".format(root_path, "train", file_name), index=False)
    validation_df.to_csv("{}/{}/{}.csv".format(root_path, "validation", file_name), index=False)
    test_df.to_csv("{}/{}/{}.csv".format(root_path, "test", file_name), index=False)
