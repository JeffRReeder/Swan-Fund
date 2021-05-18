from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)
 
# MODELS GO BELOW
class User(db.Model):
    """User model"""

    __tablename__ = "users"

    # make it easier to see object details
    def __repr__(self):
        return f"<User id={self.id} username={self.username}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    

    #stocks = db.relationship('UserStock')
    #transactions = db.relationship('Transaction')
    

    @classmethod
    def signup(cls, username, email, pwd):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(pwd).decode('UTF-8')
        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, pwd):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        u = User.query.filter_by(username=username).first()

        # u.password = crazy long string in database, pwd = what user typed into form
        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance (aka <User 3>)
            return u
        else:
            return False


class Stock(db.Model):
    """Stocks Model"""

    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    company_name = db.Column(db.Text, nullable=False, unique=True)
    ticker_symbol = db.Column(db.Text, nullable=False, unique=True)
    #bug_bunny = db.relationship('UserStock')
    #daffy_duck = db.relationship('Transaction')



class UserStock(db.Model):
    """UserStocks model"""

    __tablename__ = "users_stocks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user = db.relationship('User', backref='stocks')

    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'),primary_key=True)
    stock = db.relationship('Stock', backref='bug_bunny')

class Transaction(db.Model):
    """Transaction Model"""

    __tablename__ = "transactions"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user = db.relationship('User', backref='transactions')
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), primary_key=True)
    stock = db.relationship('Stock', backref='daffy_duck')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #timestamp = db.Column(db.Date, default=datetime.utcnow())
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    transaction_type = db.Column(db.Text, nullable=False)
    stock_ticker = db.Column(db.Text, nullable=False)
    transacted_shares = db.Column(db.Float, nullable=False)
    transacted_price_per_share = db.Column(db.Float, nullable=False)
    transaction_fees = db.Column(db.Float, nullable=False)
    stock_split_ratio = db.Column(db.Float, nullable=False)

