import os
from flask import Flask, render_template, request, redirect, url_for
from PortfolioSQL import PortfolioSQL

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'portfolio.db')


@app.route('/')
def home():
    return 'Hello, world!'

@app.route('/portfolio')
def portfolio():
    portfolio_data = portfolio.get_portfolio()
    portfolio_value = 0
    csrf_token = csrf_token = request.form.get('csrf_token') or request.args.get('csrf_token')

    if request.method == 'POST':
        symbol = request.form['symbol']
        shares = int(request.form['shares'])
        price = float(request.form['price'])
        portfolio.add_purchase(symbol, shares, price)
        prices = {symbol: price}
        portfolio_value = portfolio.value(prices)

    return render_template('portfolio.html', portfolio=portfolio, portfolio_value=portfolio_value, csrf_token=csrf_token, portfolio_data=portfolio_data)


@app.route('/update')
def update():
    db_path = os.path.join(basedir, 'data', 'portfolio.db')
    portfolio = PortfolioSQL(db_path)
    portfolio_data = portfolio.get_portfolio()
    portfolio_value = 0
    csrf_token = request.form.get('csrf_token') or request.args.get('csrf_token')

    if request.method == 'POST':
        symbol = request.form['symbol']
        shares = int(request.form['shares'])
        cost_basis = float(request.form['cost_basis'])
        portfolio.update(symbol, shares, cost_basis)
        prices = {symbol: cost_basis / shares}
        portfolio_value = portfolio.value(prices)

    return render_template('portfolio.html', portfolio=portfolio, portfolio_value=portfolio_value, csrf_token=csrf_token, portfolio_data=portfolio_data)

if __name__ == '__main__':
    app.run(debug=True)
