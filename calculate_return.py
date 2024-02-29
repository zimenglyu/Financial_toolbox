import pandas as pd
import os


class Profile:
    def __init__(self):
        self.MoneySpend = 0
        self.MoneyEarn = 0
        self.ProfileNames = []
    
    def reset(self):
        self.MoneySpend = 0
        self.MoneyEarn = 0
        self.ProfileNames = []
        
    def add_spend(self, money):
        self.MoneySpend += money
    
    def add_earn(self, money):
        self.MoneyEarn += money
    
    def get_return(self, return_type):
        profile_return = ((self.MoneyEarn - self.MoneySpend) / self.MoneySpend) * 100
        print(f"Profile return for {return_type} is {profile_return}")
        return profile_return
    
    def is_in_profile(self, stock_name):
        return stock_name in self.ProfileNames
    
    def add_stock(self, stock_name):
        if not self.is_in_profile(stock_name):
            self.ProfileNames.append(stock_name)
        else:
            print(f"{stock_name} is already in the profile")
    
    def remove_stock(self, stock_name):
        if self.is_in_profile(stock_name):
            self.ProfileNames.remove(stock_name)
        else:
            print(f"{stock_name} is not in the profile")
    
    def simple_return(self, predicted_return, price, stock_name, share=1):
        if(len(predicted_return) + 1 != len(price)):
            print('length of predicted_return is not equal to price')
            exit()
        stock_spend = 0
        stock_earn = 0
        # add it to profile first
        # self.add_stock(stock_name)
        # self.add_spend(price[0] * share)
        # stock_spend += price[0] * share
        # bought_price = price[0]
        for i in range(len(predicted_return)-1):
            if predicted_return[i] > 0:
                if not self.is_in_profile(stock_name):
                    self.add_stock(stock_name)
                    self.add_spend(price[i] * share)
                    stock_spend += price[i] * share
                    bought_price = price[i]
            else:
                if self.is_in_profile(stock_name):
                    # if bought_price < price[i]:
                    if (price[i] - bought_price)/bought_price * 100 > 7:
                        print(f"Stock {stock_name}, bought price: {bought_price}, sold price: {price[i]}")
                        self.add_earn(price[i] * share)
                        self.remove_stock(stock_name)
                        stock_earn += price[i] * share
        if self.is_in_profile(stock_name):
            self.add_earn(price[-2] * share)
            self.remove_stock(stock_name)
            stock_earn += price[-2] * share
        stock_return = ((stock_earn - stock_spend) / stock_spend) * 100
        print(f"Stock return for {stock_name} is {stock_return}")
    
    def long_short_return(self, predicted_return, price, stock_name):
        if(len(predicted_return) + 1 != len(price)):
            print('length of predicted_return is not equal to price')
            exit()
        # add it to profile first
        self.add_stock(stock_name)
        self.add_spend(price[0])
        for i in range(1, len(predicted_return)-1):
            if predicted_return[i] > 0:
                if not self.is_in_profile(stock_name):
                    print("This should never happen for long short strategy, stock: ", stock_name )
                    self.add_stock(stock_name)
                    self.add_spend(price[i])
            else:
                if self.is_in_profile(stock_name):
                    self.add_earn(price[i])
                    self.remove_stock(stock_name)
                    self.add_spend(price[i+1])
                    self.add_stock(stock_name)
        if self.is_in_profile(stock_name):
            self.add_earn(price[-2])
            self.remove_stock(stock_name)

if __name__ == '__main__':
    prediction_folder = "/Users/zimenglyu/Documents/cluster_results/0216/predictions"
    test_file_path = "/Users/zimenglyu/Documents/datasets/CRSP/DJI_history_new/single_stocks/test"
    # stock_names = ['AAPL', 'AXP', 'BA', 'CAT', 'CSCO', 'CVX', 'DOW', 'DIS', 'WBA', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE',  'PG', 'TRV', 'UNH',  'VZ', 'V', 'WMT']
    stock_names = ['AAPL', 'AXP', 'BA', 'CAT', 'CSCO', 'CVX', 'DOW', 'DIS', 'WBA', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE',  'PG', 'TRV', 'UNH',  'VZ', 'V', 'WMT', 'HON', 'AMGN', 'CRM']

    profile = Profile()

    return_strategy = 'long_short_return'
    for return_strategy in ['simple_return', 'long_short_return']:
        profile.reset()
    
        for stock_name in stock_names:
            # print(f"Processing {stock_name}")
            prediction_file = os.path.join(prediction_folder, stock_name + "_predictions.csv")
            test_file = os.path.join(test_file_path, stock_name + ".csv")
            prediction = pd.read_csv(prediction_file, usecols=['predicted_RET']).to_numpy().flatten()
            stock_price = pd.read_csv(test_file, usecols=['PRC']).to_numpy().flatten()
            # print(stock_price)
            if return_strategy == 'simple_return':
                profile.simple_return(prediction, stock_price, stock_name)
            elif return_strategy == 'long_short_return':
                profile.long_short_return(prediction, stock_price, stock_name)

        profile.get_return(return_strategy)