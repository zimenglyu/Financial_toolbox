import yfinance as yf
import pandas as pd

# Define the stock ticker
ticker = "^DJI"  # Example: Apple Inc.

# Fetch data
stock_data = yf.download(ticker, start="1920-12-29", end="2024-01-22")

# Save to CSV
stock_data.to_csv(f"{ticker}_stock_data.csv")
