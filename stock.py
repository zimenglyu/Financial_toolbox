"""
Module: stock.py

This module defines a Stock class for managing stock-related operations 
such as buying, selling, and calculating returns.

Dependencies:
- pandas

Example:
    # Create a new Stock object
    my_stock = stock.Stock('AAPL')

    # Read predicted returns from a file
    my_stock.read_return_prediction('predicted_returns.csv')

    # Read stock prices from a file
    my_stock.read_stock_price('stock_prices.csv')

    # Buy stock
    my_stock.buy_stock(1000, 0)

    # Sell stock
    my_stock.sell_stock(10)
"""

import pandas as pd

class Stock:
    """
    A class to represent a stock.

    Attributes:
    - name (str): The name of the stock.
    - share (float): The number of shares owned.
    - bought_price (float): The price at which the stock was bought.
    - return_prediction (list): List of predicted returns.
    - return_price (list): List of actual return prices.
    """

    def __init__(self, name):
        """
        Initializes a Stock object with the given name.
        """
        self.name = name
        self.share = 0.0
        self.bought_price = 0.0
        self.return_prediction = []
        self.return_price = []
        self.testing_period = None
        self.stock_price = 0.0
        
    def reset(self):
        """
        Resets the number of shares owned and bought price to zero.
        """
        self.share = 0.0
        self.bought_price = 0.0

    def read_return_prediction(self, file_path):
        """
        Reads the predicted returns from a CSV file and stores them in the return_prediction attribute.
        """
        self.return_prediction = pd.read_csv(file_path, usecols=['predicted_RET']).to_numpy().flatten()
        self.testing_period = len(self.return_prediction)

    def read_stock_price(self, file_path):
        """
        Reads the stock prices from a CSV file and stores them in the stock_price attribute.
        """
        self.stock_price = pd.read_csv(file_path, usecols=['PRC']).to_numpy().flatten()
        if len(self.return_prediction) != 0:
            if len(self.return_prediction) + 1 != len(self.stock_price):
                print('Length of predicted_return is not equal to price')
                exit()
    
    def buy_stock(self, capital, time):
        """
        Buys stock based on the amount of money available in the capital and the current stock price.
        """
        self.share += capital / self.stock_price[time] 
        self.bought_price = self.stock_price[time]

    def sell_stock(self, time): 
        """
        Sells all shares of the stock at the current time.
        """
        capital = self.stock_price[time] * self.share
        self.share = 0
        return capital
    
    def simple_return(self, capital):
        """
        Calculates the return on investment for a stock based on predicted returns.
        """
        self.capital = capital
        for i in range(len(self.return_prediction)-1):
            if self.return_prediction[i] > 0:
                if self.share == 0:
                    self.share = capital / self.stock_price[i]
                    capital = 0
                    self.bought_price = self.stock_price[i]
            else:
                if self.share != 0:
                    if self.bought_price < self.stock_price[i]:
                        capital = self.stock_price[i] * self.share
                        print(f"Stock {self.name}, bought price: {self.bought_price}, sold price: {self.stock_price[i]}, number of shares: {self.share} capital: {capital}") 
                        self.share = 0
        if self.share != 0:
            capital = self.stock_price[-2] * self.share
            self.share = 0
        return capital

    def get_predicted_return(self, time):
        """
        Returns the predicted return at a given time.
        """
        return self.return_prediction[time]
    
    def get_stock_price(self, time):
        """
        Returns the stock price at a given time.
        """
        return self.stock_price[time]
    
    def get_stock_name(self):
        """
        Returns the name of the stock.
        """
        return self.name

    def get_share(self):
        """
        Returns the number of shares owned.
        """
        return self.share
    
    def set_share(self, share):
        """
        Sets the number of shares owned.
        """
        self.share = share
    
    def set_bought_price(self, price):
        """
        Sets the price at which the stock was bought.
        """
        self.bought_price = price
    
    def get_bought_price(self):
        """
        Returns the price at which the stock was bought.
        """
        return self.bought_price
