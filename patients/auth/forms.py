from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=6, max=32),
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=32),
    ])
