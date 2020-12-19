from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class CreateReportForm(FlaskForm):
    patient = SelectField('Patient')

    submit = SubmitField('Create Report')
