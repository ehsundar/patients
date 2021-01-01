from datetime import date, timedelta, datetime

from flask import (
    Blueprint, redirect, render_template, request, url_for
)

from patients.auth import login_required
from patients.db import get_db
from patients.res.forms import CreateResForm

bp = Blueprint('res', __name__, url_prefix='/res')


@bp.route('/', methods=('GET',))
def index():
    db = get_db()
    cur = db.cursor()

    cur.execute(
        'select res.*, count(r.id) as occupied_cnt from res left join report r on res.id = r.res group by res.id',
    )
    reses = cur.fetchall()

    cur.close()
    return render_template('res/index.html', reses=reses)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    db = get_db()
    cur = db.cursor()
    form = CreateResForm(request.form)
    fill_form_choices(form)

    if request.method == 'POST' and form.validate():
        d_start = datetime.strptime(form.date.data, '%Y-%m-%d')
        d_start += timedelta(hours=int(form.start_time.data))
        d_end = datetime.strptime(form.date.data, '%Y-%m-%d')
        d_end += timedelta(hours=int(form.end_time.data))

        cur.execute(
            'insert into res (start_t, end_t, cap) values (%s, %s, %s)',
            (d_start, d_end, form.cap.data),
        )
        db.commit()
        cur.close()
        return redirect(url_for('res.index'))

    cur.close()
    return render_template('res/create.html', form=form)


@bp.route('/<int:pk>/details', methods=('GET',))
@login_required
def details(pk: int):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        'select * from res where id = %s',
        (pk,),
    )
    res = cur.fetchone()

    cur.execute(
        'select p.id as pid, p.name, r.* from report r join patient p on p.id = r.patient where r.res = %s',
        (pk,),
    )
    reports = cur.fetchall()

    cur.close()
    return render_template('res/details.html', res=res, reports=reports)


def fill_form_choices(form: CreateResForm):
    date_choices = []
    for i in range(30):
        d = date.today() + timedelta(days=i)
        date_choices.append(
            (d.strftime('%Y-%m-%d'), d.strftime('%Y/%m/%d'))
        )

    time_choices = []
    for i in range(24):
        time_choices.append(
            (str(i), f'{i}:00')
        )

    form.date.choices = date_choices
    form.start_time.choices = time_choices
    form.end_time.choices = time_choices
