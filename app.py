import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort
import requests, json
from secrets import API_KEY
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, TransactionForm, MessageForm, UserEditForm
from models import db, connect_db, User, Stock, Transaction

CURR_USER_KEY = "curr_user"

# "Quote" API endpoint
API_DATA_URL= "https://cloud.iexapis.com/stable/stock/{}/quote?token=" + API_KEY


testsymbol = 'csco'
# "Key Stats" API endpoint
DIVIDEND_URL = "https://cloud.iexapis.com/stable/stock/"+testsymbol+"/stats?token=" + API_KEY


app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///stock_project_db'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)


##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                pwd=form.password.data,
                
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect(f"/holdings/{user.id}")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    # IMPLEMENT THIS
    do_logout()
    flash("You have successfully logged out", "success")
    return redirect('/login')


##############################################################################
# General user routes:

@app.route('/holdings')
def list_user_holdings():
    """Page with listing stock holdings

    Can take a 'q' param in querystring to search by that username.
    """

    search = request.args.get('q')

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template('users/holdings.html', users=users)


@app.route('/holdings/<int:user_id>')
def list_holding(user_id):
    # you can use g.user
    user = User.query.get_or_404(user_id)
    
    ############################### "Pythonic" way ###################################################
    #stock_info = [requests.get(API_DATA_URL.format(stock.ticker_symbol)).json() for stock in stocks]
    ############################### "Pythonic" way ###################################################
    
    ############################### long version ###################################################
    # just get ticker symbols
    all_ticker_symbols = []
    stocks = []
    for user_stock in user.stocks:
        # ['CSCO', 'AAPL']
        all_ticker_symbols.append(user_stock.stock.ticker_symbol)
        stocks.append(user_stock.stock)
    
    # loop through ticker symbols and make GET request
    stock_info = []
    for all_symbols in all_ticker_symbols:
        data = requests.get(API_DATA_URL.format(all_symbols)).json()
        stock_info.append(data)
    ############################### long version ###################################################
    
    dividend = requests.get(DIVIDEND_URL).json()

    return render_template('users/holdings.html', user=user, stock_info=stock_info, API2=dividend, stocks=stocks)

@app.route('/transactions', methods=["GET", "POST"])
def list_transactions():
    
    user = g.user
    
    form = TransactionForm()
    if form.validate_on_submit():
        #timestamp = form.timestamp.data
        transaction_type = form.transactionType.data,
        stock_ticker = form.stock_ticker.data,
        transacted_shares = form.transactedShares.data,
        transacted_price_per_share = form.transactedPricePerShare.data,
        transaction_fees = form.transactionFees.data or 0.0,
        stock_split_ratio = form.stockSplitRatio.data or 0.0

        stock = Stock.query.filter(Stock.ticker_symbol == stock_ticker).first()
        trans = Transaction(user_id=user.id,
                            stock_id=stock.id,
                            transaction_type=transaction_type,
                            stock_ticker=stock_ticker, 
                            transacted_shares=transacted_shares,
                            transacted_price_per_share=transacted_price_per_share,
                            transaction_fees=transaction_fees,
                            stock_split_ratio=stock_split_ratio)
        db.session.add(trans)
        db.session.commit()
        return redirect('/transactions/list')
       
    else:
        return render_template('transaction_form.html', form=form)


@app.route('/transactions/list', methods=["GET"])
def show_transactions():
    """Show list of your transactions."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    all_transactions = Transaction.query.filter(Transaction.user_id == user.id).all()
    return render_template('transactions_list.html', all_transactions=all_transactions)


@app.route('/users/<int:user_id>/followers')
def users_followers(user_id):
    """Show list of followers of this user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    return render_template('users/followers.html', user=user)



@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""

    # IMPLEMENT THIS
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
        
    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data or "/static/images/default-pic.png"
            user.header_image_url = form.header_image_url.data or "/static/images/warbler-hero.jpg"
            user.bio = form.bio.data
            user.location = form.location.data

            db.session.commit()
            return redirect(f"/users/{user.id}")
        else:
            flash("Incorrect password, please try again", "danger")

    return render_template('users/edit.html', form=form, user_id=user.id)


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")



##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    if g.user:
        print("hello")

        return render_template('home.html')

    else:
        return render_template('home-anon.html')


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
