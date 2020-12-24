from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField


class CreateResForm(FlaskForm):
    date = SelectField('Date')
    start_time = SelectField('Start Time')
    end_time = SelectField('End Time')

    cap = IntegerField('Capacity')

    submit = SubmitField('Create Report')
