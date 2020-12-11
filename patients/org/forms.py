import re

from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import DataRequired, Length, Regexp


class OrgCreateForm(FlaskForm):
    slug = StringField('Slug', validators=[
        DataRequired(),
        Length(min=4, max=32),
        Regexp(re.compile('^[a-zA-Z-]+$'), message='must contain letters and - only'),
    ])
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=4, max=32),
    ])
