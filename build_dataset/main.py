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
    test_year = 2022
    CRSP_file_path = "/Users/zimenglyu/Documents/datasets/CRSP/DJI_company.csv"
    dataset_output_path = f"/Users/zimenglyu/Documents/datasets/CRSP/DJI_company_{test_year}"
    DJI_file_path = "/Users/zimenglyu/Documents/datasets/stock/DJI_stock_data.csv"
    if not os.path.exists(dataset_output_path):
        os.mkdir(dataset_output_path)
        print(f"Directory '{dataset_output_path}' is created.")
    else:
        print(f"Directory '{dataset_output_path}' already exists.")

    train_start = pd.to_datetime('1/1/1990')
    train_end = pd.to_datetime(f'12/31/{test_year-2}')
    validation_start = pd.to_datetime(f'1/1/{test_year-1}')
    validation_end = pd.to_datetime(f'12/31/{test_year-1}')
    test_start = pd.to_datetime(f'1/1/{test_year}')
    test_end = pd.to_datetime(f'12/30/{test_year}')
    company_tickers = ['AAPL', 'AMZN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'DOW', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WBA', 'WMT']
    # company_tickers = ['AAPL', 'AXP', 'BA', 'CAT', 'CSCO', 'CVX', 'DOW', 'DIS', 'WBA', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'HON', 'PG', 'TRV', 'UNH', 'AMZN', 'VZ', 'V', 'WMT', 'CRM']
    # company_names = ['APPLE INC', 'AMERICAN EXPRESS CO', 'BOEING CO', 'CATERPILLAR INC', 'CISCO SYSTEMS INC', 'CHEVRON CORP NEW', 'DOW INC', 'DISNEY WALT CO', 'WALGREENS BOOTS ALLIANCE INC', 'GOLDMAN SACHS GROUP INC', 'HOME DEPOT INC', 'INTERNATIONAL BUSINESS MACHS COR', 'INTEL CORP', 'JOHNSON & JOHNSON', 'JPMORGAN CHASE & CO', 'COCA COLA CO', 'MCDONALDS CORP', '3M CO', 'MERCK & CO INC NEW', 'MICROSOFT CORP', 'NIKE INC', 'HONEYWELL INTERNATIONAL INC', 'PROCTER & GAMBLE CO', 'TRAVELERS COMPANIES INC', 'UNITEDHEALTH GROUP INC', 'AMGEN INC', 'VERIZON COMMUNICATIONS INC', 'VISA INC', 'WALMART INC', 'SALESFORCE INC']
    list_columns = ["date", "CUSIP", "COMNAM", "RET", "VOL_CHANGE", "BA_SPREAD", "ILLIQUIDITY", "sprtrn", "TURNOVER", "DJI_Return", "PRC", "TRAN_COST", "ASK", "BID"]
    make_dir(os.path.join(dataset_output_path, "train"))
    make_dir(os.path.join(dataset_output_path, "validation"))
    make_dir(os.path.join(dataset_output_path, "test"))
    make_dir(os.path.join(dataset_output_path, "raw_data"))

    CRSP = CRSP_Dataset(CRSP_file_path, company_tickers)
    CRSP.get_CRSP_company()
    CRSP.add_predictors()
    CRSP.add_DJI_return(DJI_file_path)
    CRSP.select_columns(list_columns)
    CRSP.remove_nan()
    CRSP.save_raw_data(dataset_output_path)
    CRSP.split_train_validation_test(train_start, train_end, validation_start, validation_end, test_start, test_end)
    CRSP.save_to_csv(dataset_output_path)
