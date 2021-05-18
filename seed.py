from models import db, User, Stock, UserStock, Transaction
from datetime import datetime
from app import app

# Create all tables
db.drop_all()
db.create_all()

# password is '123'
user1 = User(username='test1', password='$2b$12$uixTQhtpGqTgO0XeAo30g.M9h2mSfTTOEwFO3vjfRo2UHQojguT7C', email='a@a.com')
user2 = User(username='test2', password='$2b$12$RmrRz7X1ojWnLZaRN4n75uIIfVAVvGwBjvrgeG7tPp46kOWZ5tRUi', email='b@b.com')
#user2 = User(username='test', password='123')

db.session.add(user1)
db.session.add(user2)
db.session.commit()

stock1 = Stock(company_name="cisco", ticker_symbol="CSCO")
stock2 = Stock(company_name="apple", ticker_symbol="AAPL")
stock3 = Stock(company_name="Tesla", ticker_symbol="TSLA")
stock4 = Stock(company_name="3M", ticker_symbol="MMM")
stock5 = Stock(company_name="amazon", ticker_symbol="AMZN")


db.session.add_all([stock1, stock2, stock3, stock4, stock5])
db.session.commit()



user_stock1 = UserStock(user_id=user1.id, stock_id=stock1.id)
user_stock2 = UserStock(user_id=user1.id, stock_id=stock2.id)
user_stock3 = UserStock(user_id=user1.id, stock_id=stock3.id)
user_stock4 = UserStock(user_id=user1.id, stock_id=stock4.id)
user_stock5 = UserStock(user_id=user2.id, stock_id=stock5.id)

db.session.add_all([user_stock1, user_stock2, user_stock3, user_stock4, user_stock5])
db.session.commit()

transaction1 = Transaction(
    user_id=user1.id,
    stock_id=stock1.id,
    timestamp=datetime(2021, 4, 27, 22, 43, 21, 722303), 
    transaction_type="buy", 
    stock_ticker="CSCO", 
    transacted_shares=5.0, 
    transacted_price_per_share=51.40, 
    transaction_fees=0.00, 
    stock_split_ratio=0.0,
    )
db.session.add(transaction1)
db.session.commit()

# select ticker_symbol from stocks JOIN users_stocks ON stocks.id=users_stocks.stock_id JOIN users ON users.id=users_stocks.
# user_id WHERE users.id=1;
