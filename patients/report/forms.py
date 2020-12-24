from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class CreateReportForm(FlaskForm):
    patient = SelectField('Patient')
    res = SelectField('Reservation')
    state = SelectField('State')

    submit = SubmitField('Create Report')
