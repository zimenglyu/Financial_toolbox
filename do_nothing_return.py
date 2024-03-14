import pandas as pd
import os


if __name__ == '__main__':
    # prediction_folder = "/Users/zimenglyu/Documents/cluster_results/0216/predictions"
    test_file_path = "data/2023_test"

    stock_names = ['AAPL', 'AXP', 'BA', 'CAT', 'CSCO', 'CVX', 'DOW', 'DIS', 'WBA', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE',  'PG', 'TRV', 'UNH',  'VZ', 'V', 'WMT', 'HON', 'AMGN', 'CRM']
    money_spend = 0
    money_earned = 0
    
    for stock_name in stock_names:
        test_file = os.path.join(test_file_path, stock_name + ".csv")
        stock_price = pd.read_csv(test_file, usecols=['PRC']).to_numpy().flatten()
        money_spend += stock_price[0]
        money_earned += stock_price[-2]
        company_return = (stock_price[-2] - stock_price[0]) / stock_price[0] * 100
        print(" Company: ", stock_name, " Return: ", company_return)
    total_return = ((money_earned - money_spend) / money_spend ) * 100
    print(total_return)

    # profile.get_return(return_strategy)

