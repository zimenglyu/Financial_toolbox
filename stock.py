import pandas as pd
import os


class Stock:

    def __init__(self, name):
        self.name = name
        self.share = 0
        self.bought_price = 0
        self.return_prediction = []
        self.return_price = []
        
    def reset(self):
        self.share = 0
        self.bought_price = 0

    def read_return_prediction(self, file_path):
        self.return_prediction = pd.read_csv(file_path, usecols=['predicted_RET']).to_numpy().flatten()
        self.testing_period = len(self.return_prediction)

    def read_stock_price(self, file_path):
        self.stock_price = pd.read_csv(file_path, usecols=['PRC']).to_numpy().flatten()
        if len(self.return_prediction) != 0:
            if len(self.return_prediction) + 1 != len(self.stock_price):
                print('Length of predicted_return is not equal to price')
                print('stock name: ', self.name)
                print('Length of predicted_return: ', len(self.return_prediction))
                print('Length of price: ', len(self.stock_price))
                exit()
    
    def buy_stock(self, money_pool, time):
        # buy as many shares as possible, when buying, their might be existing shares
        self.share += money_pool / self.stock_price[time] 
        self.bought_price = self.stock_price[time]

    def sell_stock(self, time): 
        # sell all shares
        money_pool = self.stock_price[time] * self.share
        self.share = 0
        return money_pool
    
    def simple_return(self, money_pool):
        """
        Calculates the return on investment for a stock based on predicted returns.
        """
        self.money_pool = money_pool
        for i in range(len(self.return_prediction)-1):
            if self.return_prediction[i] > 0:
                if self.share == 0:
                    self.share = money_pool / self.stock_price[i]
                    money_pool = 0
                    self.bought_price = self.stock_price[i]
                    print(f"Stock {self.name}, bought price: {self.bought_price}, number of shares: {self.share}")
            else:
                if self.share != 0:
                    if self.bought_price < self.stock_price[i]:
                        money_pool = self.stock_price[i] * self.share
                        print(f"Stock {self.name}, bought price: {self.bought_price}, sold price: {self.stock_price[i]}, number of shares: {self.share} money_pool: {money_pool}") 
                        self.share = 0
        if self.share != 0:
            money_pool = self.stock_price[-2] * self.share
            self.share = 0
        return money_pool
    
    def long_short_return(self, money_pool, risk):
        """
        Calculates the return on investment for a stock using a long-short strategy.
        simple strategies only "long" the stocks, but long-short strategy can "short" the stocks
        """
        self.money_pool = money_pool
        share_borrowed = 0
        borrow_price = 0
        
        for i in range(len(self.return_prediction)-1):
            if self.return_prediction[i] > 0:
                if money_pool != 0:
                    self.share += money_pool / self.stock_price[i]
                    money_pool = 0
                    self.bought_price = self.stock_price[i]
                if share_borrowed != 0:
                    self.share -= share_borrowed
                    share_borrowed = 0
            else:
                if self.share > 0:
                    if self.bought_price < self.stock_price[i]:
                        money_pool = self.stock_price[i] * self.share
                        print(f"Stock {self.name}, bought price: {self.bought_price}, sold price: {self.stock_price[i]}, number of shares: {self.share} money_pool: {money_pool}") 
                        self.share = 0
                    
                borrow_dollar_amount = risk * self.money_pool
                share_borrowed = borrow_dollar_amount / self.stock_price[i]
                borrow_price = self.stock_price[i]
                money_pool += borrow_dollar_amount
                print(f"Stock {self.name}, borrow dollar amount: {borrow_dollar_amount}, borrowed price: {borrow_price}, number of shares: {share_borrowed}")
        if self.share > 0:
            if self.share > share_borrowed:
                self.share -= share_borrowed
                share_borrowed = 0
                money_pool += self.stock_price[-2] * self.share
                self.share = 0
        money_pool += self.stock_price[-2] * self.share
        money_pool -= self.stock_price[-2] * share_borrowed
        return money_pool

    def get_predicted_return(self, time):
        return self.return_prediction[time]
    
    def get_stock_price(self, time):
        return self.stock_price[time]
    
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
    