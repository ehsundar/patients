from datetime import datetime

from flask import (
    Blueprint, render_template, url_for, g
)

from patients.db import get_db

bp = Blueprint('home', __name__, url_prefix='')


@bp.route('/', methods=('GET',))
def index():
    db = get_db()
    cur = db.cursor()

    pages = [
        {'name': 'Organizations', 'url': url_for('org.index')},
        {'name': 'Patients', 'url': url_for('patient.index')},
        {'name': 'User', 'url': url_for('user.index')},
        {'name': 'Reports', 'url': url_for('report.index')},
        {'name': 'Reservations', 'url': url_for('res.index')},
    ]

    cur.execute(
        'select report.id, p.name, r.start_t from report join patient p on p.id = report.patient join res r on r.id = report.res where r.start_t > timestamp %s limit 15',
        (datetime.now(),),
    )
    reports = cur.fetchall()

    cur.execute(
        '''
        select report.id, p.name, r.start_t from report 
        join patient p on p.id = report.patient join res r on r.id = report.res 
        where r.start_t > timestamp %s and report.creator_user in 
            (select username from users where org = %s)
        order by r.start_t 
        limit 5
        ''',
        (datetime.now(), g.user.org),
    )
    reports_org = cur.fetchall()

    cur.close()
    return render_template('home/index.html', pages=pages, reports=reports, reports_org=reports_org)
