"""
This module contains the `Portfolio` class, which provides methods 
for tracking spending and earnings, managing stocks in the portfolio, 
and calculating returns on investment using various investment strategies.

"""
from stock import Stock
class Portfolio:
    """
    A class to manage financial portfolios including spending, earning, and stock investments.

    Attributes:
        money_spend (float): Total amount spent.
        money_earn (float): Total amount earned.
        portfolio_names (list): List of stock names in the portfolio.
    """

    def __init__(self, stock_names):
        """
        Initializes a Portfolio object with default attributes.
        """
        self.initial_spend_per_stock = 0
        self.initial_money_pool = 0
        self.stock_names = stock_names
        self.money_spend = 0
        self.money_earn = 0
        self.portfolio_list = []
        self.portfolio_return = 0
        self.risk_tolenrance = 0.2
        print("Portfolio created")

    def reset(self):
        """
        Resets the portfolio by clearing spending, earning, and the list of stock names.
        """
        self.money_earn = 0
        for company in self.portfolio_list:
            company.reset()
        
        if (self.strategy == 'simple_return'):
            self.money_spend = self.initial_spend_per_stock * len(self.stock_names)
        elif (self.strategy == 'portfolio_simple_return'):
            self.money_spend = self.initial_money_pool
        elif (self.strategy == 'long_short_return'):
            self.money_spend = self.initial_spend_per_stock * len(self.stock_names)
        else:
            print("Invalid strategy, can't reset portfolio")
            exit()
    
    def add_company_to_protfolio(self, company):
        self.portfolio_list.append(company)
        print (f"added company {company.get_stock_name()} to portfolio list" )

    def set_initial_money_pool(self, money_pool):
        self.initial_money_pool = money_pool
    
    def set_initial_spend_per_stock(self, spend_per_stock):
        self.initial_spend_per_stock = spend_per_stock
    
    def set_risk_tolenrance(self, risk_tolenrance):
        self.risk_tolenrance = risk_tolenrance

    def trade(self, strategy):
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
        print("Calculating simple return")
        for company in self.portfolio_list:
            self.money_earn += company.simple_return(self.initial_spend_per_stock)
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

    def portfolio_simple_return(self):
        """
        Calculates the return on investment for the entire portfolio.
        At each time, the portfolio buys stocks with positive predicted returns 
        and sells stocks with negative predicted returns.

        """
        testing_period = self.portfolio_list[0].testing_period
        self.current_money_pool = self.initial_money_pool


        for time in range(testing_period - 1):
            # sell stocks with negative predicted returns
            for company in self.portfolio_list:
                if company.get_predicted_return(time) < 0:
                    if company.get_bought_price() < company.get_stock_price(time):
                        self.current_money_pool += company.sell_stock(time)
            companies_to_buy = []
            # find all stocks to buy at time t
            for company in self.portfolio_list:
                if company.get_predicted_return(time) > 0:
                    companies_to_buy.append(company)
            if len(companies_to_buy) == 0:
                print(f"No stock to buy at time {time}")
                continue
            else:
                # just give each stock equal amount of money
                quota_per_stock = self.current_money_pool / len(companies_to_buy)
                for company in companies_to_buy:
                    if self.current_money_pool >= quota_per_stock:
                        company.buy_stock(quota_per_stock, time)
                        self.current_money_pool -= quota_per_stock
                    elif abs(self.current_money_pool - quota_per_stock) < 1:
                        company.buy_stock(self.current_money_pool, time)
                        self.current_money_pool = 0
                    else:
                        print(f"Can't buy stock {company.get_stock_name()} at time {time} because of insufficient money")
                        print("current money pool: ", self.current_money_pool)
                        print("quota per stock: ", quota_per_stock)
                if self.current_money_pool > 1:
                    print(f"current money pool {self.current_money_pool} at time {time}")
        # sell all stocks at the end
        for company in self.portfolio_list:
            self.money_earn += company.sell_stock(-2)
        return self.calculate_return()

    def long_short_return(self):
        """
        Calculates the return on investment for a stock using a long-short strategy.
        simple strategies only "long" the stocks, but long-short strategy can "short" the stocks
        """
        for company in self.portfolio_list:
            self.money_earn += company.long_short_return(self.initial_spend_per_stock, self.risk_tolenrance)
        return self.calculate_return()
    