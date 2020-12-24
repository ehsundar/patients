from flask import (
    Blueprint, render_template, url_for
)

bp = Blueprint('home', __name__, url_prefix='')


@bp.route('/', methods=('GET',))
def index():
    pages = [
        {'name': 'Organizations', 'url': url_for('org.index')},
        {'name': 'Patients', 'url': url_for('patient.index')},
        {'name': 'User', 'url': url_for('user.index')},
        {'name': 'Reports', 'url': url_for('report.index')},
        {'name': 'Reservations', 'url': url_for('res.index')},
    ]
    return render_template('home/index.html', pages=pages)
