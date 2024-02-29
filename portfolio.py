"""
This module contains the `Portfolio` class, which provides methods 
for tracking spending and earnings, managing stocks in the portfolio, 
and calculating returns on investment using various investment strategies.

"""
class Portfolio:
    """
    A class to manage financial portfolios including spending, earning, and stock investments.

    Attributes:
        money_spend (float): Total amount spent.
        money_earn (float): Total amount earned.
        portfolio_names (list): List of stock names in the portfolio.
    """

    def __init__(self, stock_names, spend_per_stock=200):
        """
        Initializes a Portfolio object with default attributes.
        """
        self.spend_per_stock = spend_per_stock
        self.stock_names = stock_names
        self.money_spend = self.spend_per_stock * len(self.stock_names)
        self.money_earn = 0
        self.portfolio_names = []

    def reset(self):
        """
        Resets the portfolio by clearing spending, earning, and the list of stock names.
        """
        self.money_spend = self.spend_per_stock * len(self.stock_names)
        self.money_earn = 0
        self.portfolio_names = []

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

    def get_return(self, return_type):
        """
        Calculates and prints the portfolio's return on investment.

        Args:
            return_type (str): Type of return, e.g., 'simple_return' or 'long_short_return'.

        Returns:
            float: Portfolio return on investment.
        """
        portfolio_return = ((self.money_earn - self.money_spend) / self.money_spend) * 100
        print(f"Portfolio return for {return_type} is {portfolio_return}")
        return portfolio_return

    def is_in_portfolio(self, stock_name):
        """
        Checks if a stock is present in the portfolio.

        Args:
            stock_name (str): Name of the stock.

        Returns:
            bool: True if the stock is in the portfolio, False otherwise.
        """
        return stock_name in self.portfolio_names

    def add_stock(self, stock_name):
        """
        Adds a stock to the portfolio if it's not already present.

        Args:
            stock_name (str): Name of the stock.
        """
        if not self.is_in_portfolio(stock_name):
            self.portfolio_names.append(stock_name)
        else:
            print(f"{stock_name} is already in the portfolio")

    def remove_stock(self, stock_name):
        """
        Removes a stock from the portfolio if it's present.

        Args:
            stock_name (str): Name of the stock.
        """
        if self.is_in_portfolio(stock_name):
            self.portfolio_names.remove(stock_name)
        else:
            print(f"{stock_name} is not in the portfolio")

    def simple_return(self, predicted_return, price, stock_name, share=1):
        """
        Calculates the return on investment for a stock based on predicted returns.

        Args:
            predicted_return (list): Predicted returns for the stock.
            price (list): Prices of the stock over time.
            stock_name (str): Name of the stock.
            share (int): Number of shares (default is 1).
        """
        if(len(predicted_return) + 1 != len(price)):
            print('length of predicted_return is not equal to price')
            exit()
        money_pool = 200
        share = 0
        for i in range(len(predicted_return)-1):
            if predicted_return[i] > 0:
                if not self.is_in_portfolio(stock_name):
                    self.add_stock(stock_name)
                    share = money_pool / price[i]
                    # print(f"Stock {stock_name}, bought price: {price[i]}, share: {share}")
                    money_pool = 0
                    bought_price = price[i]
            else:
                if self.is_in_portfolio(stock_name):
                    if bought_price < price[i]:
                        money_pool = price[i] * share
                        print(f"Stock {stock_name}, bought price: {bought_price}, sold price: {price[i]}, number of shares: {share} money_pool: {money_pool}")
                        self.remove_stock(stock_name)
        if self.is_in_portfolio(stock_name):
            self.remove_stock(stock_name)
            money_pool = price[-2] * share
        if (money_pool == 0):
            print(f"Stock {stock_name} is in the profolio, but not sold")
            exit()
        self.add_earn(money_pool)
        print(f"Stock {stock_name}, earned: {money_pool}")



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
