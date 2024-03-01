"""
This module contains the `Portfolio` class, which provides methods 
for tracking spending and earnings, managing stocks in the portfolio, 
and calculating returns on investment using various investment strategies.

"""
from typing import List
from stock import Stock

class Portfolio:
    """
    A class to manage financial portfolios including spending, earning, and stock investments.

    Attributes:
        stocks (List[Stock]): List of Stock objects representing the stocks in the portfolio.
        initial_capital (float): Initial capital amount for the portfolio.
        initial_spend_per_stock (float): Initial spend per stock in the portfolio.
        money_spend (float): Total amount spent in the portfolio.
        money_earn (float): Total amount earned in the portfolio.
        portfolio_list (list): List of stocks currently held in the portfolio.
        portfolio_return (float): Return on investment for the portfolio.
    """
    
    def __init__(self, stocks : List[Stock], initial_capital=0.0, initial_spend_per_stock=0.0, money_spend=0.0, money_earn=0.0, portfolio_return=0.0):
        """
        Initializes a Portfolio object with default attributes.
        """
        self.initial_spend_per_stock = initial_spend_per_stock
        self.initial_capital = initial_capital
        self.balance = initial_capital
        self.stocks = stocks
        self.money_spend = money_spend
        self.money_earn = money_earn
        self.portfolio_return = portfolio_return
        print("Portfolio created")
        
    def stats(self):
        """returns a brief summary of class object.

        Returns:
            _type_: _description_
        """
        number_of_stocks = len(self.stocks)
        if number_of_stocks > 1 :
            substring_1 = f"This portfolio has {len(self.stocks)} stocks."
        elif number_of_stocks == 0:
            substring_1 = f"This portfolio has NO stocks."
        else: 
            substring_1 = f"This portfolio has just 1 stock."
        return f"Stats:\n\t{substring_1} Its initial capital was ${self.initial_capital}.\n\tThe portfolio has spent ${self.money_spend} & earned ${self.money_earn}.\n\tStocks currently held:\n\t\t\t{self.__get_stock_strings()}"

    def __get_stock_strings(self):
        """returns a list of strings with currently held stocks' names.

        Returns:
            _type_: _description_
        """
        stocks_strings = []
        for stock in self.stocks:
            stocks_strings.append(stock.get_stock_name())
        return stocks_strings
        
    def reset(self):
        """
        Resets the portfolio by clearing spending, earning, and the list of stock names.
        """
        self.money_earn = 0
        for stock in self.stocks:
            stock.reset()
        
        if (self.strategy == 'simple_return'):
            self.money_spend = self.initial_spend_per_stock * len(self.stocks)
        elif (self.strategy == 'portfolio_simple_return'):
            self.money_spend = self.initial_capital
        elif (self.strategy == 'long_short_return'):
            print("do something here")
            exit()
        else:
            print("Invalid strategy, can't reset portfolio")
            exit()
    
    def add_stock_to_portfolio(self, stock):
        """
        Adds a stock to the portfolio.

        Args:
            stock (Stock): Stock object to be added to the portfolio.
        """
        self.stocks.append(stock)
        print (f"added stock {stock.get_stock_name()} to portfolio list" )

    def set_initial_capital(self, capital):
        """
        Sets the initial capital for the portfolio.

        Args:
            capital (float): Initial capital amount.
        """
        self.initial_capital = capital
    
    def set_initial_spend_per_stock(self, spend_per_stock):
        """
        Sets the initial spend per stock for the portfolio.

        Args:
            spend_per_stock (float): Initial spend per stock amount.
        """
        self.initial_spend_per_stock = spend_per_stock

    def trade(self, strategy):
        """
        Executes trading based on the specified strategy.

        Args:
            strategy (str): The trading strategy to be executed.

        Raises:
            ValueError: If the specified strategy is not supported.
        """
        self.strategy = strategy
        print(f"Trading with {self.strategy} strategy")
        self.reset()
        if self.strategy == 'simple_return':
            self.simple_return()
        elif self.strategy == 'portfolio_simple_return':
            self.portfolio_simple_return()
        elif self.strategy == 'long_short_return':
            self.long_short_return()
        else:
            print("Invalid trading strategy")
            exit()
    
    def simple_return(self):
        """
        Calculates the return on investment using the simple return strategy.
        """
        print("Calculating simple return")
        for stock in self.stocks:
            self.money_earn += stock.simple_return(self.initial_spend_per_stock)
        return self.calculate_return()

    def add_spend(self, money):
        """
        Adds spending amount to the portfolio.

        Args:
            money (float): Amount of money spent.
        """
        self.money_spend += money

    def add_earn(self, money):
        """
        Adds earning amount to the portfolio.

        Args:
            money (float): Amount of money earned.
        """
        self.money_earn += money

    def calculate_return(self):
        """
        Calculates and prints the portfolio's return on investment.

        Returns:
            float: Portfolio return on investment.
        """
        print(f"Total money spent: {self.money_spend}")
        print(f"Total money earned: {self.money_earn}")
        self.portfolio_return = ((self.money_earn - self.money_spend) / self.money_spend) * 100
        print(f"Portfolio return for {self.strategy} is {self.portfolio_return:.2f}%")
        return self.portfolio_return

    def is_in_portfolio(self, stock_name):
        """
        Checks if a stock is present in the portfolio.

        Args:
            stock_name (str): Name of the stock.

        Returns:
            bool: True if the stock is in the portfolio, False otherwise.
        """
        return stock_name in self.__get_stock_strings()

    def add_stock(self, stock_name):
        """
        Adds a stock to the portfolio if it's not already present.

        Args:
            stock_name (str): Name of the stock.
        """
        if not self.is_in_portfolio(stock_name):
            self.stocks.append(stock_name)
        else:
            print(f"{stock_name} is already in the portfolio")

    def remove_stock(self, stock_name):
        """
        Removes a stock from the portfolio if it's present.

        Args:
            stock_name (str): Name of the stock.
        """
        if self.is_in_portfolio(stock_name):
            self.stocks.remove(stock_name)
        else:
            print(f"{stock_name} is not in the portfolio")

    def portfolio_simple_return(self):
        """
        Calculates the return on investment for the entire portfolio.
        At each time, the portfolio buys stocks with positive predicted returns 
        and sells stocks with negative predicted returns.

        """
        testing_period = self.stocks[0].testing_period


        for time in range(testing_period - 1):
            # sell stocks with negative predicted returns
            for stock in self.stocks:
                if stock.get_predicted_return(time) < 0:
                    if stock.get_bought_price() < stock.get_stock_price(time):
                        self.balance += stock.sell_stock(time)
            companies_to_buy = []
            # find all stocks to buy at time t
            for stock in self.stocks:
                if stock.get_predicted_return(time) > 0:
                    companies_to_buy.append(stock)
            if len(companies_to_buy) == 0:
                print(f"No stock to buy at time {time}")
                continue
            else:
                # just give each stock equal amount of money
                quota_per_stock = self.balance / len(companies_to_buy)
                for stock in companies_to_buy:
                    if self.balance >= quota_per_stock:
                        stock.buy_stock(quota_per_stock, time)
                        self.balance -= quota_per_stock
                    elif abs(self.balance - quota_per_stock) < 1:
                        stock.buy_stock(self.balance, time)
                        self.balance = 0
                    else:
                        print(f"Can't buy stock {stock.get_stock_name()} at time {time} because of insufficient money")
                        print("current money pool: ", self.balance)
                        print("quota per stock: ", quota_per_stock)
                if self.balance > 1:
                    print(f"current money pool {self.balance} at time {time}")
        # sell all stocks at the end
        for stock in self.stocks:
            self.money_earn += stock.sell_stock(-2)
        return self.calculate_return()

    def long_short_return(self, predicted_return, price, stock_name):
        """
        Calculates the return on investment for a stock using a long-short strategy.

        Args:
            predicted_return (list): Predicted returns for the stock.
            price (list): Prices of the stock over time.
            stock_name (str): Name of the stock.
        """
        if len(predicted_return) + 1 != len(price):
            print('Length of predicted_return is not equal to price')
            exit()

        self.add_stock(stock_name)
        self.add_spend(price[0])

        for i in range(1, len(predicted_return) - 1):
            if predicted_return[i] > 0:
                if not self.is_in_portfolio(stock_name):
                    print("This should never happen for long short strategy, stock: ", stock_name)
                    self.add_stock(stock_name)
                    self.add_spend(price[i])
            else:
                if self.is_in_portfolio(stock_name):
                    self.add_earn(price[i])
                    self.remove_stock(stock_name)
                    self.add_spend(price[i + 1])
                    self.add_stock(stock_name)

        if self.is_in_portfolio(stock_name):
            self.add_earn(price[-2])
            self.remove_stock(stock_name)
