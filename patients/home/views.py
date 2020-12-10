import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('home', __name__, url_prefix='')


@bp.route('/', methods=('GET',))
def index():
    pages = [
        {'name': 'Organizations','url': url_for('org.index')},
        {'name': 'Patients','url': url_for('patient.index')},
        {'name': 'User','url': url_for('user.index')},
    ]
    return render_template('home/index.html', pages=pages)
