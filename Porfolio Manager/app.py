from flask import Flask, render_template, request
from Portfolio import Portfolio
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AASH'

# Include the CSRF extension
csrf = CSRFProtect(app)


@app.route('/portfolio')
def portfolio():
    portfolio = Portfolio()
    portfolio_value = 0
    csrf_token = csrf_token = request.form.get('csrf_token') or request.args.get('csrf_token') or csrf.protect()


    if request.method == 'POST':
        symbol = request.form['symbol']
        shares = int(request.form['shares'])
        price = float(request.form['price'])
        portfolio.buy(symbol, shares, price)
        prices = {symbol: price}
        portfolio_value = portfolio.value(prices)

    return render_template('portfolio.html', portfolio=portfolio, portfolio_value=portfolio_value, csrf_token=csrf_token)


@app.route('/update')
def update():
    portfolio = Portfolio()
    portfolio_value = 0
    csrf_token = csrf_token = request.form.get('csrf_token') or request.args.get('csrf_token') or csrf.protect()


    if request.method == 'POST':
        symbol = request.form['symbol']
        shares = int(request.form['shares'])
        cost_basis = float(request.form['cost_basis'])
        portfolio.update(symbol, shares, cost_basis)
        prices = {symbol: cost_basis / shares}
        portfolio_value = portfolio.value(prices)

    return render_template('portfolio.html', portfolio=portfolio, portfolio_value=portfolio_value, csrf_token=csrf_token)


if __name__ == '__main__':
    app.run(debug=True)
