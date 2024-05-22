import pandas as pd
import os


if __name__ == '__main__':
    # prediction_folder = "/Users/zimenglyu/Documents/cluster_results/0216/predictions"
    test_file_path = "/Users/zimenglyu/Documents/datasets/CRSP/DJI_company_2023/test"
    
    stock_names = ['AAPL', 'AXP', 'BA', 'CAT', 'CSCO', 'CVX', 'DOW', 'DIS', 'WBA', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE',  'PG', 'TRV', 'UNH',  'VZ', 'V', 'WMT', 'HON', 'AMZN', 'CRM']
    print(f"number of companies: {len(stock_names)}")
    # money_spend = 0
    # money_earned = 0
    company_return = 0
    for stock_name in stock_names:
        test_file = os.path.join(test_file_path, stock_name + ".csv")
        stock_price = pd.read_csv(test_file, usecols=['PRC']).to_numpy().flatten()
        # money_spend += stock_price[0]
        # money_earned += stock_price[-2]
        company_return = (stock_price[-2] - stock_price[0]) / stock_price[0] * 100
        print(" Company: ", stock_name, " Return: ", company_return)
    total_return = company_return /len(stock_names) 
    print(f"Total return: {total_return}")

    # profile.get_return(return_strategy)

