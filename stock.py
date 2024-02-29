import pandas as pd
import os


class Stock:

    def __init__(self, name):
        self.name = name
        self.share = 0
        self.bought_price = 0
        print("Stock {} created".format(self.name))
    
    def read_return_prediction(self, file_path):
        self.return_prediction = pd.read_csv(file_path, usecols=['predicted_RET']).to_numpy().flatten()
    
    def read_stock_price(self, file_path):
        self.return_price = pd.read_csv(file_path, usecols=['PRC']).to_numpy().flatten()
    
    def simple_return(self, money_pool):
        """
        Calculates the return on investment for a stock based on predicted returns.
        """
   
        self.money_pool = money_pool
        for i in range(len(self.return_prediction)-1):
            if self.return_prediction[i] > 0:
                if self.share == 0:
                    self.share = money_pool / self.return_price[i]
                    money_pool = 0
                    self.bought_price = self.return_price[i]
            else:
                if self.share != 0:
                    if self.bought_price < self.return_price[i]:
                        money_pool = self.return_price[i] * self.share
                        print(f"Stock {self.name}, bought price: {self.bought_price}, sold price: {self.return_price[i]}, number of shares: {self.share} money_pool: {money_pool}") 
                        self.share = 0
        if self.share != 0:
            money_pool = self.return_price[-2] * self.share
        return money_pool

    def get_predicted_return(self, time):
        return self.return_prediction[time]
    
    def get_stock_price(self, time):
        return self.return_price[time]
    
    def get_stock_name(self):
        return self.name

    def get_share(self):
        return self.share
    
    def set_share(self, share):
        self.share = share
    
    def set_bought_price(self, price):
        self.bought_price = price
    
    def get_bought_price(self):
        return self.bought_price
    