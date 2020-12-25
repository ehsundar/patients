from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField

from patients.db import get_db


class StatePickerForm(FlaskForm):
    state = SelectField('State')

    def fill_state_choices(self):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM state",
        )
        self.state.choices = [('all', 'All')] + list(map(lambda s: (s.slug, s.name), cur.fetchall()))
        cur.close()


class CreateReportForm(FlaskForm):
    patient = SelectField('Patient')
    res = SelectField('Reservation')
    state = SelectField('State')

    submit = SubmitField('Create Report')
