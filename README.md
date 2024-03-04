# Portfolio Management System

This repository contains a simple portfolio management system written in Python. It allows users to calculate returns on investment for different stocks based on predicted returns and actual prices.

## Files

- `portfolio.py`: Contains the `Portfolio` class responsible for managing financial portfolios.
- `stock.py`: Contains the `Stock` class responsible for managing stocks in portfolios.
- `main.py`: Main script to execute portfolio calculations.
- `README.md`: This documentation file.

## Usage

1. Ensure you have Python installed on your system.
2. Clone this repository to your local machine.
3. Install the required dependencies by running `pip install pandas`.
4. Modify `main.py` to provide appropriate file paths for prediction data and test data.
5. Define return_strategy in `main.py`.
6. Run `main.py` to execute the portfolio calculations.

## Portfolio Class

The `Portfolio` class contains the following trading strategies:

- `simple_return`: Trade each stock individually based on the predicted return. Each stock has the same initial capital for investment. If predicted return > 0, buy or hold; if predicted return <= 0, sell.
- `portfolio_simple_return`: At time t, sell all stocks with negative predicted return, and use the gained capital to invest all the stocks with positive capital.
- `long_short_return`: Short the stocks with predicted negative return, STILL UNDER DEVELOPMENT.


## Contributors

- [Zimeng Lyu](https://github.com/zimenglyu)
- [Rohaan Nadeem](https://github.com/rohaan2614)
