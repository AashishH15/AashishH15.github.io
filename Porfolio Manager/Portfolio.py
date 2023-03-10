import pandas as pd

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
