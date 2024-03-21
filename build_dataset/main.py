import pandas as pd
import os
from CRSP_Dataset import CRSP_Dataset

def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print(f"Directory '{path}' is build.")
    else:
        print(f"Directory '{path}' already exists)")

if __name__ == '__main__':
    CRSP_file_path = "/Users/zimenglyu/Documents/datasets/CRSP/DJI_company.csv"
    dataset_output_path = "/Users/zimenglyu/Documents/datasets/CRSP/DJI_company_2023"
    DJI_file_path = "/Users/zimenglyu/Documents/datasets/stock/DJI_stock_data.csv"

    train_start = pd.to_datetime('1/1/1990')
    train_end = pd.to_datetime('12/31/2021')
    validation_start = pd.to_datetime('1/1/2022')
    validation_end = pd.to_datetime('12/31/2022')
    test_start = pd.to_datetime('1/1/2023')
    test_end = pd.to_datetime('12/30/2023')
    company_names = ['AAPL', 'AXP', 'BA', 'CAT', 'CSCO', 'CVX', 'DOW', 'DIS', 'WBA', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'HON', 'PG', 'TRV', 'UNH', 'AMGN', 'VZ', 'V', 'WMT', 'CRM']
    list_columns = ["date", "RET", "VOL_CHANGE", "BA_SPREAD", "ILLIQUIDITY", "sprtrn", "TURNOVER", "DJI_Return"]
    make_dir(os.path.join(dataset_output_path, "train"))
    make_dir(os.path.join(dataset_output_path, "validation"))
    make_dir(os.path.join(dataset_output_path, "test"))
    make_dir(os.path.join(dataset_output_path, "raw_data"))

    CRSP = CRSP_Dataset(CRSP_file_path, company_names)
    CRSP.get_CRSP_company()
    CRSP.add_predictors()
    CRSP.add_DJI_return(DJI_file_path)
    CRSP.select_columns(list_columns)
    CRSP.remove_nan()
    CRSP.save_raw_data(dataset_output_path)
    CRSP.split_train_validation_test(train_start, train_end, validation_start, validation_end, test_start, test_end)
    CRSP.save_to_csv(dataset_output_path)
