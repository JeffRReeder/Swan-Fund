from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired, Email, Length, InputRequired, Optional
from wtforms.fields.html5 import DateField

stocks = ["ABBV", "ABC", "ABT", "ADM", "AFL", "AMP", "AOS", "BEN", "CAH", "CMCSA", "CMI",
          "CSCO", "CVS", "ECL", "ED", "EV", "FAST", "FLO", "GD", "GIS", "HON", "HRL", 
          "ITW", "KMB", "KO", "LEG", "LMT", "LOW", "MDT", "MMM", "NEP", "NOC", "O", "ORI",
          "PBCT", "PFE", "PG", "QCOM", "RTX", "SBSI", "SPHD", "T", "TDS", "TGT", "TROW", 
          "TXN", "UBSI", "UNP", "VFC", "VZ", "WBA", "WEC", "WEYS", "IVV", "AIEQ", "TSLA",
          "AMNF", "BA", "CBRL", "DIS", "EAT", "JPM", "STX", "WDC", "WHG", "WSM", ".INX"]

class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=3)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=3)])

class TransactionForm(FlaskForm):
    
    #timestamp = DateTimeField("Date", validators=[InputRequired()])
    timestamp = DateField('DatePicker', format='%Y-%m-%d')
    transactionType = SelectField("Type", choices=[('buy','BUY'),('sell','SELL'),('div','DIVIDEND'),('split','SPLIT')])

    stock_ticker = SelectField("Stock", choices=[(st, st) for st in stocks])
    transactedShares = FloatField("Transacted Shares", validators=[InputRequired()])
    transactedPricePerShare = FloatField("Transacted Price/Share", validators=[InputRequired()])
    transactionFees = FloatField("Fees", validators=[Optional()])
    stockSplitRatio = FloatField("Stock Split", validators=[Optional()])

class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    header_image_url = StringField('(Optional) Header Image URL')
    bio = TextAreaField('Tell us about yourself')
    location = TextAreaField('Location')
    password = PasswordField('Password', validators=[Length(min=3)])
