"""
This module contains the `Portfolio` class, which provides methods 
for tracking spending and earnings, managing stocks in the portfolio, 
and calculating returns on investment using various investment strategies.

"""
from stock import Stock
from Logger import Logger
import numpy as np
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
        self.initial_capital = 0
        self.stock_names = stock_names
        self.money_spend = 0
        self.money_earn = 0
        self.portfolio_list = []
        self.portfolio_return = 0
        self.borrow_ratio = 0.5
        self.use_TC = False
        self.calculate_bound = False
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
        else:
            self.money_spend = self.initial_capital
    
    def set_logger(self, logger):
        self.logger = logger
        for company in self.portfolio_list:
            company.set_logger(logger)

    def add_company_to_protfolio(self, company):
        self.portfolio_list.append(company)
        self.logger.log(f"added company {company.get_stock_name()} to portfolio list", 'DEBUG')

    def set_initial_capital(self, money_pool):
        self.initial_capital = money_pool
    
    def set_initial_spend_per_stock(self, spend_per_stock):
        self.initial_spend_per_stock = spend_per_stock
    
    def set_risk_tolenrance(self, risk_tolenrance):
        self.risk_tolenrance = risk_tolenrance

    def trade(self, strategy, long_company_number=10, short_company_number=5):
        portfolio_return = 0
        self.strategy = strategy
        self.logger.log(f"Trading with {self.strategy} strategy", 'INFO')
        self.reset()
        if self.strategy == 'simple_return':
            portfolio_return = self.simple_return()
        elif self.strategy == 'portfolio_simple_return':
            portfolio_return = self.portfolio_simple_return()
        elif self.strategy == 'portfolio_shorting_return':
            portfolio_return = self.portfolio_shorting_return()
        elif self.strategy == 'long_short_return':
            portfolio_return = self.long_short_return(long_company_number, short_company_number)
        elif self.strategy == 'daily_long_return':
            portfolio_return = self.daily_long_return(long_company_number, short_company_number)
        elif self.strategy == 'daily_long_short_return':
            portfolio_return = self.daily_long_short_return(long_company_number, short_company_number)
        elif self.strategy == 'daily_zimeng_long_short_return':
            portfolio_return = self.daily_zimeng_long_short_return(long_company_number, short_company_number)
        else:
            self.logger.log("Invalid trading strategy", 'ERROR')
            exit()
        return portfolio_return
    
    def simple_return(self):
        self.logger.log("Calculating simple return", 'INFO')
        for company in self.portfolio_list:
            self.money_earn += company.simple_return(self.initial_spend_per_stock)
        return self.calculate_return()
    
    def set_waiting_period(self, waiting_period):
        for company in self.portfolio_list:
            company.set_waiting_period(waiting_period)

    def calculate_return(self):
        """
        Calculates and prints the portfolio's return on investment.

        Returns:
            float: Portfolio return on investment.
        """
        self.logger.log(f"Total money spent: {self.money_spend}", 'DEBUG')
        self.logger.log(f"Total money earned: {self.money_earn}", 'DEBUG')
        self.portfolio_return = ((self.money_earn - self.money_spend) / self.money_spend) * 100
        self.logger.log(f"Portfolio return for {self.strategy} is {self.portfolio_return:.2f}%", 'INFO')
        return self.portfolio_return

    def add_stock(self, stock_name):
        """
        Adds a stock to the portfolio if it's not already present.

        Args:
            stock_name (str): Name of the stock.
        """
        if not self.is_in_portfolio(stock_name):
            self.portfolio_names.append(stock_name)
        else:
            self.logger.log(f"{stock_name} is already in the portfolio", 'ERROR')

    def remove_stock(self, stock_name):
        """
        Removes a stock from the portfolio if it's present.

        Args:
            stock_name (str): Name of the stock.
        """
        if self.is_in_portfolio(stock_name):
            self.portfolio_names.remove(stock_name)
        else:
            self.logger.log(f"{stock_name} is not in the portfolio", "ERROR")
    
    def set_use_TC(self, use_TC):
        self.use_TC = use_TC
        for company in self.portfolio_list:
            company.set_use_TC(use_TC)

    def set_trade_with_bid_ask(self, trade_with_bid_ask):
        self.trade_with_bid_ask = trade_with_bid_ask
        for company in self.portfolio_list:
            company.set_trade_with_bid_ask(trade_with_bid_ask)
    
    def get_sorted_return_list(self, time):
        predicted_return_list = []
        for company in self.portfolio_list:
            predicted_return_list.append(company.get_predicted_return(time))
        sorted_index = np.argsort(predicted_return_list)
        # sorted_index = sorted(range(len(predicted_return_list)), key=lambda k: predicted_return_list[k])
        return sorted_index, predicted_return_list

    def daily_long_return(self, number_top = 5, number_bottom = 5):
        """
        Calculates the return on investment for a stock using a long strategy.
        """
        self.reset()
        self.current_cash_amount = self.initial_capital
        testing_period = self.portfolio_list[0].testing_period
        for time in range(testing_period - 1):
            self.logger.log(f"[time {time}]: current cash amount: {self.current_cash_amount}", 'DEBUG')
            sorted_index, predicted_return_list = self.get_sorted_return_list(time)
            daily_long_quota = self.current_cash_amount / number_top

            sold_company = 0
            for i in range(30):
                if sold_company < number_bottom:
                    company = self.portfolio_list[sorted_index[i]]
                    if company.get_share() > 0:
                        self.current_cash_amount += company.sell_stock(time)
                        sold_company += 1
            self.logger.log(f"[time {time}]: current cash amount after selling stocks: {self.current_cash_amount}", 'DEBUG')
            
            for i in range(number_top):
                index = -(i+1)
                company = self.portfolio_list[sorted_index[index]]
                if self.current_cash_amount >= daily_long_quota:
                    company.buy_stock(daily_long_quota, time)
                    self.current_cash_amount -= daily_long_quota
                elif abs(self.current_cash_amount - daily_long_quota) < 1:
                    company.buy_stock(self.current_cash_amount, time)
                    self.current_cash_amount = 0
                else:
                    self.logger.log(f"Can't buy stock {company.get_stock_name()} at time {time} because of insufficient money", 'DEBUG')
        self.logger.log("/*-----Clearing all stocks-------*/", 'DEBUG')
        for company in self.portfolio_list:
            self.money_earn += company.clear_holdings(-2)
        return self.calculate_return()


    def portfolio_simple_return(self):
        testing_period = self.portfolio_list[0].testing_period
        self.current_cash_amount = self.initial_capital

        for time in range(testing_period - 1):
            self.logger.log("------------------------------------------", 'DEBUG')
            self.logger.log(f"[time {time}]: current cash amount: {self.current_cash_amount}", 'DEBUG')
            # sell stocks with negative predicted returns
            for company in self.portfolio_list:
                if company.get_predicted_return(time) < 0:
                    if company.get_bought_price() < company.get_stock_price(time):
                        self.current_cash_amount += company.sell_stock(time)
            companies_to_buy = []
            self.logger.log(f"[time {time}]: current cash amount after selling stocks: {self.current_cash_amount}", 'DEBUG')
            # find all stocks to buy at time t
            for company in self.portfolio_list:
                if company.get_predicted_return(time) > 0:
                    companies_to_buy.append(company)
            if len(companies_to_buy) == 0:
                self.logger.log(f"No stock to buy at time {time}", 'DEBUG')
                continue
            else:
                # just give each stock equal amount of money
                if self.current_cash_amount > 0.0001:
                    quota_per_stock = self.current_cash_amount / len(companies_to_buy)
                    self.logger.log(f"[time {time}]: number of company to buy: {len(companies_to_buy)}, quota per stock: {quota_per_stock}", 'DEBUG')
                    for company in companies_to_buy:
                        if self.current_cash_amount >= quota_per_stock:
                            company.buy_stock(quota_per_stock, time)
                            self.current_cash_amount -= quota_per_stock
                        elif abs(self.current_cash_amount - quota_per_stock) < 1:
                            company.buy_stock(self.current_cash_amount, time)
                            self.current_cash_amount = 0
                        else:
                            self.logger.log(f"Can't buy stock {company.get_stock_name()} at time {time} because of insufficient money", 'DEBUG')
                            self.logger.log("current money pool: ", self.current_cash_amount, 'DEBUG')
                            self.logger.log("quota per stock: ", quota_per_stock, 'DEBUG')
                    if self.current_cash_amount > 1:
                        self.logger.log(f"current money pool {self.current_cash_amount} at time {time}", 'DEBUG')
                self.logger.log(f"[End of time {time}], current cash amount: {self.current_cash_amount}", 'DEBUG')
            for company in self.portfolio_list:
                company.print_current_holdings(time)
            
        # sell all stocks at the end
        self.logger.log("/*-----Clearing all stocks-------*/", 'DEBUG')
        for company in self.portfolio_list:
            self.money_earn += company.clear_holdings(testing_period - 2)
        return self.calculate_return()

    def portfolio_shorting_return(self):
        testing_period = self.portfolio_list[0].testing_period
        # current money pool is the current cash amount
        self.current_cash_amount = self.initial_capital
        # current liquid is currently how much we have minus how much we borrowed
        current_liquid = self.initial_capital
        self.logger.log(f"[time 0]: current liquid: {current_liquid}", 'DEBUG')

        for time in range(testing_period - 1):
            for company in self.portfolio_list:
                if company.get_predicted_return(time) > 0:
                    if company.get_share() < 0:
                        # if company.get_sold_price() > company.get_stock_price(time):
                        self.current_cash_amount += company.return_stock(time)
            self.logger.log(f"[time {time}]: current cash amount after covering stocks {self.current_cash_amount}", 'DEBUG')
            current_liquid = 0
            for company in self.portfolio_list:
                current_liquid += company.get_current_liquid(time)
            current_liquid += self.current_cash_amount
            self.logger.log(f"[time {time}]: current liquid: {current_liquid}", 'DEBUG')
            # --------- start to short stocks ------------
            company_to_short = []
            for company in self.portfolio_list:
                if company.get_predicted_return(time) < 0 and company.get_share() >= 0:
                    company_to_short.append(company)
            if len(company_to_short) == 0:
                self.logger.log(f"[time {time}]: No stock to short today", 'DEBUG')
                continue
            else:
                self.logger.log(f"[time {time}]: number of company to short: {len(company_to_short)}", 'DEBUG' )
                borrow_cash_amount = current_liquid
                # borrow_cash_amount = self.borrow_ratio * current_liquid
                quota_per_stock = borrow_cash_amount / len(company_to_short)
                # 
                self.logger.log(f"[time {time}]: borrow cash amount:{borrow_cash_amount}, quota per stock {quota_per_stock}", 'DEBUG')
                for company in company_to_short:
                    # self.logger.log("shorting stock: ", company.get_stock_name())
                    if borrow_cash_amount >= quota_per_stock:
                        company.short_stock(quota_per_stock, time)
                        borrow_cash_amount -= quota_per_stock
                        self.current_cash_amount += quota_per_stock
                        self.logger.log(f"[time {time}]: current cash: {borrow_cash_amount}, current cash amount: {self.current_cash_amount}", 'DEBUG')
                    elif abs(borrow_cash_amount - quota_per_stock) < 1:
                        company.short_stock(borrow_cash_amount, time)
                        self.current_cash_amount += borrow_cash_amount
                        borrow_cash_amount = 0
                        self.logger.log(f"[time {time}]: current cash: {borrow_cash_amount}, current cash amount: {self.current_cash_amount}", 'DEBUG')
                    else:
                        self.logger.log(f"[time {time}]: Can't short stock {company.get_stock_name()} because of insufficient money", 'DEBUG')
                        self.logger.log(f"[time {time}]: current money pool: {borrow_cash_amount}", 'DEBUG')
                self.logger.log(f"[time {time}]: current cash amount at end {self.current_cash_amount}".format(time, self.current_cash_amount), 'DEBUG')

        for company in self.portfolio_list:
            self.current_cash_amount += company.clear_holdings(-2)
        self.money_earn = self.current_cash_amount
        return self.calculate_return()
    
    def daily_long_short_return(self, long_company_number=10, short_company_number=5):
        """
        Calculates the return on investment for a stock using a long-short strategy.
        simple strategies only "long" the stocks, but long-short strategy can "short" the stocks
        """

        self.logger.log(f"Using {long_company_number} companies to long and {short_company_number} companies to short", 'INFO')
        self.reset()
        self.current_cash_amount = self.initial_capital
        # self.long_short_return_helper(list_length)
        testing_period = self.portfolio_list[0].testing_period
        # current money pool is the current cash amount
        self.current_cash_amount = self.initial_capital
        # current liquid is currently how much we have minus how much we borrowed
        longed_stock_yesterday = []
        shorted_stock_yesterday = []
        for time in range(testing_period - 1):
            do_trade = True
            longed_stock_today = []
            shorted_stock_today = []
# ----------------------- find company -------------------------------------
            sorted_index, predicted_return_list = self.get_sorted_return_list(time)
            for i in range(long_company_number):
                index = -(i+1) # get the last 10 stocks
                company = self.portfolio_list[sorted_index[index]]
                # if company.get_predicted_return(time) > 0:
                longed_stock_today.append(company)
                # else:
                #     self.logger.log(f"[time {time}]: No Trade Today!", 'DEBUG')
                #     do_trade = False
                #     break

            for i in range(short_company_number):
                company = self.portfolio_list[sorted_index[i]]
                # if company.get_predicted_return(time) < 0:
                shorted_stock_today.append(company)
                # else:
                #     self.logger.log(f"[time {time}]: No Trade Today!", 'DEBUG')
                #     do_trade = False
                #     break
# ---------------------------- trade -------------------------------------
            if do_trade:
                # clear all holdings
                self.logger.log(f"[time {time}]: clearing all holdings", 'DEBUG')
                for company in longed_stock_yesterday:
                    self.current_cash_amount += company.clear_holdings(time)
                    self.logger.log(f"[time {time}]: current cash amount: {self.current_cash_amount}", 'DEBUG')
                for company in shorted_stock_yesterday:
                    self.current_cash_amount += company.clear_holdings(time)
                    self.logger.log(f"[time {time}]: current cash amount: {self.current_cash_amount}", 'DEBUG')
                self.logger.log(f"[time {time}]: current cash amount after clearing all holdings: {self.current_cash_amount}", 'DEBUG')

                # sorted_index, predicted_return_list = self.get_sorted_return_list(time)
                borrow_cash_amount = self.current_cash_amount
                quota_per_stock = self.current_cash_amount / long_company_number

                self.logger.log(f"[time {time}]: longing {long_company_number} stocks, current cash amount: {self.current_cash_amount}, quota per stock: {quota_per_stock}", 'DEBUG')

                for company in longed_stock_today:
                    self.logger.log(f"[time {time}]: longing stock {company.get_stock_name()}, quota per stock: {quota_per_stock}, predicted return: {company.get_predicted_return(time)}", 'DEBUG')
                    if self.current_cash_amount > quota_per_stock:
                        company.buy_stock(quota_per_stock, time)
                        self.current_cash_amount -= quota_per_stock
                    elif abs(self.current_cash_amount - quota_per_stock) < 1:
                        company.buy_stock(self.current_cash_amount, time)
                        self.current_cash_amount = 0
                    else:
                        self.logger.log(f"[time {time}]: Can't buy stock {company.get_stock_name()} at time {time} because of insufficient money", 'DEBUG')

                # short the last 10 stocks
                quota_per_stock = borrow_cash_amount / short_company_number
                self.logger.log(f"[time {time}]: shorting {short_company_number} stocks, quota per stock: {quota_per_stock}", 'DEBUG')

                for company in shorted_stock_today:
                    self.logger.log(f"[time {time}]: shorting stock {company.get_stock_name()}, quota per stock: {quota_per_stock}, predicted return: {company.get_predicted_return(time)}", 'DEBUG')
                    if borrow_cash_amount >= quota_per_stock:
                        company.short_stock(quota_per_stock, time)
                        borrow_cash_amount -= quota_per_stock
                        self.current_cash_amount += quota_per_stock
                        # self.current_cash_amount -= quota_per_stock
                    elif abs(borrow_cash_amount - quota_per_stock) < 1:
                        company.short_stock(borrow_cash_amount, time)
                        self.current_cash_amount += borrow_cash_amount
                        borrow_cash_amount = 0
                    else:
                        self.logger.log(f"[time {time}]: Can't short stock {company.get_stock_name()} at time {time} because of insufficient money", 'DEBUG')
                longed_stock_yesterday = longed_stock_today
                shorted_stock_yesterday = shorted_stock_today

        for company in self.portfolio_list:
            self.current_cash_amount += company.clear_holdings(time)
        self.money_earn = self.current_cash_amount
        return self.calculate_return()
    
    def daily_hybrid_long_short_return(self, long_company_number=10, short_company_number=5):
        """
        Calculates the return on investment for a stock using a long-short strategy.
        simple strategies only "long" the stocks, but long-short strategy can "short" the stocks
        """

        self.logger.log(f"Using {long_company_number} companies to long and {short_company_number} companies to short", 'INFO')
        self.reset()
        self.current_cash_amount = self.initial_capital
        # self.long_short_return_helper(list_length)
        testing_period = self.portfolio_list[0].testing_period
        # current money pool is the current cash amount
        self.current_cash_amount = self.initial_capital
        # current liquid is currently how much we have minus how much we borrowed
        longed_stock_yesterday = []
        shorted_stock_yesterday = []
        for time in range(testing_period - 1):
            do_trade = True
            longed_stock_today = []
            shorted_stock_today = []
# ----------------------- find company -------------------------------------
            sorted_index, predicted_return_list = self.get_sorted_return_list(time)
            for i in range(long_company_number):
                index = -(i+1) # get the last 10 stocks
                company = self.portfolio_list[sorted_index[index]]
                if company.get_predicted_return(time) > 0:
                    longed_stock_today.append(company)
                else:
                    self.logger.log(f"[time {time}]: No Trade Today!", 'DEBUG')
                    do_trade = False
                    break

            for i in range(short_company_number):
                company = self.portfolio_list[sorted_index[i]]
                if company.get_predicted_return(time) < 0:
                    shorted_stock_today.append(company)
                else:
                    self.logger.log(f"[time {time}]: No Trade Today!", 'DEBUG')
                    do_trade = False
                    break
# ---------------------------- trade -------------------------------------
            if do_trade:
                # clear all holdings
                self.logger.log(f"[time {time}]: clearing all holdings", 'DEBUG')
                for company in longed_stock_yesterday:
                    self.current_cash_amount += company.clear_holdings(time)
                    self.logger.log(f"[time {time}]: current cash amount: {self.current_cash_amount}", 'DEBUG')
                for company in shorted_stock_yesterday:
                    self.current_cash_amount += company.clear_holdings(time)
                    self.logger.log(f"[time {time}]: current cash amount: {self.current_cash_amount}", 'DEBUG')
                self.logger.log(f"[time {time}]: current cash amount after clearing all holdings: {self.current_cash_amount}", 'DEBUG')

                # sorted_index, predicted_return_list = self.get_sorted_return_list(time)
                borrow_cash_amount = self.current_cash_amount
                quota_per_stock = self.current_cash_amount / long_company_number

                self.logger.log(f"[time {time}]: longing {long_company_number} stocks, current cash amount: {self.current_cash_amount}, quota per stock: {quota_per_stock}", 'DEBUG')

                for company in longed_stock_today:
                    self.logger.log(f"[time {time}]: longing stock {company.get_stock_name()}, quota per stock: {quota_per_stock}, predicted return: {company.get_predicted_return(time)}", 'DEBUG')
                    if self.current_cash_amount > quota_per_stock:
                        company.buy_stock(quota_per_stock, time)
                        self.current_cash_amount -= quota_per_stock
                    elif abs(self.current_cash_amount - quota_per_stock) < 1:
                        company.buy_stock(self.current_cash_amount, time)
                        self.current_cash_amount = 0
                    else:
                        self.logger.log(f"[time {time}]: Can't buy stock {company.get_stock_name()} at time {time} because of insufficient money", 'DEBUG')

                # short the last 10 stocks
                quota_per_stock = borrow_cash_amount / short_company_number
                self.logger.log(f"[time {time}]: shorting {short_company_number} stocks, quota per stock: {quota_per_stock}", 'DEBUG')

                for company in shorted_stock_today:
                    self.logger.log(f"[time {time}]: shorting stock {company.get_stock_name()}, quota per stock: {quota_per_stock}, predicted return: {company.get_predicted_return(time)}", 'DEBUG')
                    if borrow_cash_amount >= quota_per_stock:
                        company.short_stock(quota_per_stock, time)
                        borrow_cash_amount -= quota_per_stock
                        self.current_cash_amount += quota_per_stock
                        # self.current_cash_amount -= quota_per_stock
                    elif abs(borrow_cash_amount - quota_per_stock) < 1:
                        company.short_stock(borrow_cash_amount, time)
                        self.current_cash_amount += borrow_cash_amount
                        borrow_cash_amount = 0
                    else:
                        self.logger.log(f"[time {time}]: Can't short stock {company.get_stock_name()} at time {time} because of insufficient money", 'DEBUG')
                longed_stock_yesterday = longed_stock_today
                shorted_stock_yesterday = shorted_stock_today

        for company in self.portfolio_list:
            self.current_cash_amount += company.clear_holdings(time)
        self.money_earn = self.current_cash_amount
        return self.calculate_return()
    

    def long_short_return(self, long_company_number=10, short_company_number=5):
        """
        Calculates the return on investment for a stock using a long-short strategy.
        simple strategies only "long" the stocks, but long-short strategy can "short" the stocks
        """

        self.reset()
        testing_period = self.portfolio_list[0].testing_period
        # current money pool is the current cash amount
        self.current_cash_amount = self.initial_capital
        current_liquid = self.initial_capital   
        # current liquid is currently how much we have minus how much we borrowed

        for time in range(testing_period - 1):
            # self.logger.log(f"[time {time}]: checking waiting time", 'DEBUG')
            # for company in self.portfolio_list:
            #     if company.check_waiting_period():
            #         self.current_cash_amount += company.clear_holdings(time)

            self.logger.log(f"[time {time}]: clearing holdings based on predicted returns", 'DEBUG')
            for company in self.portfolio_list:
                self.current_cash_amount += company.clear_holdings(time)
            self.logger.log(f"[time {time}]: current cash amount after clearing all holdings: {self.current_cash_amount}", 'DEBUG')
            # sorted_index, predicted_return_list = self.get_sorted_return_list(time)
            
            current_liquid = 0
            for company in self.portfolio_list:
                current_liquid += company.get_current_liquid(time)
            current_liquid += self.current_cash_amount
            self.logger.log(f"[time {time}]: current liquid: {current_liquid}", 'DEBUG')
            borrow_cash_amount = current_liquid


                # --------- start to long and short stocks ------------
            company_to_long = []
            for company in self.portfolio_list:
                if company.get_predicted_return(time) > 0:
                    company_to_long.append(company)
            if len(company_to_long) != 0:
                long_quota_per_stock = borrow_cash_amount / len(company_to_long)
                for company in company_to_long:
                    if self.current_cash_amount > long_quota_per_stock:
                        company.buy_stock(long_quota_per_stock, time)
                        self.current_cash_amount -= long_quota_per_stock
                    elif abs(self.current_cash_amount - long_quota_per_stock) < 1:
                        company.buy_stock(self.current_cash_amount, time)
                        self.current_cash_amount = 0
                    else:
                        self.logger.log(f"Can't buy stock {company.get_stock_name()} at time {time} because of insufficient money", 'DEBUG')
                       
                # short the last 10 stocks
            company_to_short = []
            for company in self.portfolio_list:
                if company.get_predicted_return(time) < 0:
                    company_to_short.append(company)
            
            if len(company_to_short) != 0:
                short_quota_per_stock = borrow_cash_amount / len(company_to_short)
                for company in company_to_short:
                    if borrow_cash_amount >= short_quota_per_stock:
                        company.short_stock(short_quota_per_stock, time)
                        borrow_cash_amount -= short_quota_per_stock
                        self.current_cash_amount += short_quota_per_stock
                        # self.current_cash_amount -= quota_per_stock
                    elif abs(borrow_cash_amount - short_quota_per_stock) < 1:
                        company.short_stock(borrow_cash_amount, time)
                        self.current_cash_amount += borrow_cash_amount
                        borrow_cash_amount = 0
                    else:
                        self.logger.log(f"Can't short stock {company.get_stock_name()} at time {time} because of insufficient money", 'DEBUG')
            else:
                self.logger.log(f"[time {time}]: No Trade Today!", 'DEBUG')
                continue


        for company in self.portfolio_list:
            self.current_cash_amount += company.clear_holdings(time)
        self.money_earn = self.current_cash_amount
        return self.calculate_return()
    