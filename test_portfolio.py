""""
This module is not a core component of the code. 
Its just my experimental space like scratch notes.
"""
from stock import Stock
from portfolio import Portfolio

apple_stock = Stock("Apple")
apple_stock.load_predictions('data/predictions/AAPL_predictions.csv')
apple_stock.load_real_prices('data/test/AAPL.csv')

portfolio = Portfolio(stocks=[apple_stock])
print(portfolio.stats())
# portfolio.trade()