import pandas as pd
import os
from portfolio import Portfolio

if __name__ == '__main__':
    PREDICTION_DIR = "data/predictions"
    TEST_DIR = "data/test"
    stock_names = ['AAPL', 'AXP', 'BA', 'CAT', 'CSCO', 'CVX', 'DOW', 'DIS', 'WBA', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE',  'PG', 'TRV', 'UNH',  'VZ', 'V', 'WMT', 'HON', 'AMGN', 'CRM']

    portfolio = Portfolio()

    for return_strategy in ['simple_return', 'long_short_return']:
        portfolio.reset()
    
        for stock_name in stock_names:
            prediction_file = os.path.join(PREDICTION_DIR, stock_name + "_predictions.csv")
            test_file = os.path.join(TEST_DIR, stock_name + ".csv")
            prediction = pd.read_csv(prediction_file, usecols=['predicted_RET']).to_numpy().flatten()
            stock_price = pd.read_csv(test_file, usecols=['PRC']).to_numpy().flatten()
            if return_strategy == 'simple_return':
                portfolio.simple_return(prediction, stock_price, stock_name)
            elif return_strategy == 'long_short_return':
                portfolio.long_short_return(prediction, stock_price, stock_name)

        portfolio.get_return(return_strategy)
