import re

from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Regexp


class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=6, max=32),
        Regexp(re.compile('^[a-zA-Z-_]+$'),
               message='must contain letters, - and _ only'),
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=32),
    ])
    org = SelectField('Org')
    perms = SelectMultipleField('Permissions')
