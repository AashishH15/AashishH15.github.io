import pandas as pd
import numpy as np

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

class Stock:
    def __init__(self, symbol, prices):
        self.symbol = symbol
        self.prices = prices

    def moving_average(self, window_size):
        return pd.Series(self.prices).rolling(window=window_size).mean()

if __name__ == '__main__':
    portfolio = Portfolio()

    while True:
        symbol = input("Enter stock symbol (or type 'done' to finish): ")
        if symbol.lower() == 'done':
            break
        shares = int(input("Enter number of shares: "))
        price = float(input("Enter price: "))
        portfolio.buy(symbol, shares, price)

    portfolio_value = portfolio.value(price)

    while True:
        symbol = input("Enter stock symbol to update (or type 'done' to finish): ")
        if symbol.lower() == 'done':
            break
        shares = int(input("Enter new number of shares: "))
        cost_basis = float(input("Enter new cost basis: "))
        portfolio.update(symbol, shares, cost_basis)

    print("Portfolio holdings:")
    print(portfolio.holdings)
    print(f"Portfolio value: ${portfolio_value:.2f}")
