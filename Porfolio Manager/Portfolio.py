# Import required libraries
import pandas as pd
import numpy as np

# Define portfolio class
class Portfolio:
    def __init__(self):
        self.holdings = pd.DataFrame(columns=['symbol', 'shares', 'cost_basis'])

    def buy(self, symbol, shares, price):
        cost_basis = shares * price
        if symbol in self.holdings['symbol'].tolist():
            index = self.holdings.index[self.holdings['symbol'] == symbol].tolist()[0]
            self.holdings.loc[index, 'shares'] += shares
            self.holdings.loc[index, 'cost_basis'] += cost_basis
        else:
            new_holding = pd.DataFrame({'symbol': [symbol], 'shares': [shares], 'cost_basis': [cost_basis]})
            self.holdings = pd.concat([self.holdings, new_holding], ignore_index=True)

    def update(self, symbol, shares, cost_basis):
        if symbol in self.holdings['symbol'].tolist():
            index = self.holdings.index[self.holdings['symbol'] == symbol].tolist()[0]
            self.holdings.loc[index, 'shares'] = shares
            self.holdings.loc[index, 'cost_basis'] = cost_basis
        else:
            print("Symbol not found in portfolio.")

    def value(self, prices):
        if self.holdings.empty:
            return 0
        else:
            value_series = self.holdings.set_index('symbol')['shares'] * prices
            return value_series.sum()

# Define stock class
class Stock:
    def __init__(self, symbol, prices):
        self.symbol = symbol
        self.prices = prices

    def moving_average(self, window_size):
        return pd.Series(self.prices).rolling(window=window_size).mean()

# Example usage
if __name__ == '__main__':
    # Create portfolio
    portfolio = Portfolio()

    # Buy stocks
    while True:
        symbol = input("Enter stock symbol (or type 'done' to finish): ")
        if symbol.lower() == 'done':
            break
        shares = int(input("Enter number of shares: "))
        price = float(input("Enter price: "))
        portfolio.buy(symbol, shares, price)

    # Define stocks
    aapl_prices = [130.0, 132.0, 131.0, 129.0, 133.0, 134.0, 135.0, 137.0, 136.0, 140.0]
    msft_prices = [255.0, 252.0, 250.0, 248.0, 247.0, 246.0, 245.0, 242.0, 241.0, 240.0]

    aapl = Stock('AAPL', aapl_prices)
    msft = Stock('MSFT', msft_prices)

    # Calculate moving average for AAPL
    aapl_ma = aapl.moving_average(5)

    # Calculate portfolio value
    prices = pd.Series({'AAPL': aapl_prices[-1], 'MSFT': msft_prices[-1]})
    portfolio_value = portfolio.value(prices)

    # Update portfolio holdings
    while True:
        symbol = input("Enter stock symbol to update (or type 'done' to finish): ")
        if symbol.lower() == 'done':
            break
        shares = int(input("Enter new number of shares: "))
        cost_basis = float(input("Enter new cost basis: "))
        portfolio.update(symbol, shares, cost_basis)

    # Calculate new portfolio value
    prices = pd.Series({'AAPL': aapl_prices[-1], 'MSFT': msft_prices[-1]})
    new_portfolio_value = portfolio.value(prices)

    # Print results
    print("Portfolio holdings:")
    print(portfolio.holdings)
    print(f"Portfolio value: ${portfolio_value:.2f}")
    print(f"New portfolio value: ${new_portfolio_value:.2f}")