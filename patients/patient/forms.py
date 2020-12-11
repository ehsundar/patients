import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Regexp, Length


class CreatePatientForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=6, max=32)])
    phone = StringField('Phone Number', validators=[DataRequired(), Regexp(re.compile('^[0-9]{11,12}$'))])
    gender = SelectField('Gender', choices=['Male', 'Female', 'Other'])

    submit = SubmitField('Create Patient')
