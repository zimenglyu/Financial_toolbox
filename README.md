# Portfolio Management System

This repository contains a simple portfolio management system written in Python. It allows users to calculate returns on investment for different stocks based on predicted returns and actual prices.

## Files

- `portfolio.py`: Contains the `Portfolio` class responsible for managing financial portfolios.
- `main.py`: Main script to execute portfolio calculations.
- `README.md`: This documentation file.

## Usage

1. Ensure you have Python installed on your system.
2. Clone this repository to your local machine.
3. Install the required dependencies by running `pip install pandas`.
4. Modify `main.py` to provide appropriate file paths for prediction data and test data.
5. Run `main.py` to execute the portfolio calculations.

## Portfolio Class

The `Portfolio` class provides the following methods:

- `reset()`: Resets the portfolio.
- `add_spend(money)`: Adds spending amount.
- `add_earn(money)`: Adds earning amount.
- `get_return(return_type)`: Calculates and prints the return on investment.
- `is_in_Portfolio(stock_name)`: Checks if a stock is in the portfolio.
- `add_stock(stock_name)`: Adds a stock to the portfolio.
- `remove_stock(stock_name)`: Removes a stock from the portfolio.
- `simple_return(predicted_return, price, stock_name, share=1)`: Calculates return on investment based on predicted returns.
- `long_short_return(predicted_return, price, stock_name)`: Calculates return on investment using a long-short strategy.

## Contributors

- [Zimeng Lyu](https://github.com/zimenglyu)
- [Rohaan Nadeem](https://github.com/rohaan2614)
