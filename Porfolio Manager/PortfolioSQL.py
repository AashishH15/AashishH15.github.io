import sqlite3

class PortfolioSQL:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS portfolio
                       (id INTEGER PRIMARY KEY,
                        name TEXT,
                        symbol TEXT,
                        num_shares INTEGER,
                        purchase_price REAL,
                        purchase_date TEXT)''')
        self.conn.commit()

    def add_purchase(self, name, symbol, num_shares, purchase_price, purchase_date):
        cur = self.conn.cursor()
        cur.execute('''INSERT INTO portfolio (name, symbol, num_shares, purchase_price, purchase_date)
                       VALUES (?, ?, ?, ?, ?)''', (name, symbol, num_shares, purchase_price, purchase_date))
        self.conn.commit()

    def get_portfolio(self):
        cur = self.conn.cursor()
        cur.execute('''SELECT name, symbol, SUM(num_shares), AVG(purchase_price), MIN(purchase_date), MAX(purchase_date)
                       FROM portfolio
                       GROUP BY name, symbol''')
        return cur.fetchall()
