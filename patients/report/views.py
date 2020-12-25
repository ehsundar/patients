from datetime import datetime

from flask import (
    Blueprint, g, redirect, render_template, request, url_for, abort
)

from patients.auth import login_required
from patients.db import get_db
from patients.report.forms import CreateReportForm, StatePickerForm

bp = Blueprint('report', __name__, url_prefix='/report')


@bp.route('/', methods=('GET',))
def index():
    db = get_db()
    cur = db.cursor()

    state = request.args.get('state', None)
    if state and state != 'all':
        cur.execute(
            'SELECT report.id, p.name FROM report JOIN patient p on p.id = report.patient where report.state = %s',
            (state,),
        )
    else:
        cur.execute(
            'SELECT report.id, p.name FROM report JOIN patient p on p.id = report.patient',
        )
    reports = cur.fetchall()

    cur.close()

    state_picker = StatePickerForm()
    state_picker.fill_state_choices()
    return render_template('report/index.html', reports=reports, state_picker=state_picker)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    db = get_db()
    cur = db.cursor()
    form = CreateReportForm(request.form)
    fill_form_choices(form)

    form.state.data = 'not-attached'

    if request.method == 'POST' and form.validate():
        cur.execute(
            'INSERT INTO report (patient, creator_user, res, state) VALUES (%s, %s, %s, %s)',
            (form.patient.data, g.user.username, form.res.data, form.state.data),
        )
        db.commit()
        cur.close()
        return redirect(url_for('report.index'))

    cur.close()
    return render_template('report/create.html', form=form)


@bp.route('/edit/<int:pk>', methods=('GET', 'POST'))
def edit(pk: int):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        'SELECT * FROM report WHERE id=%s',
        (pk,),
    )
    report = cur.fetchone()
    if not report:
        abort(404)

    if request.method == 'POST':
        form = CreateReportForm(request.form)
        fill_form_choices(form)

        if form.validate():
            cur.execute(
                'UPDATE report SET patient = %s, res = %s, state = %s WHERE id=%s',
                (form.patient.data, form.res.data, form.state.data, pk),
            )
            db.commit()
            cur.close()
            return redirect(url_for('report.index'))

        cur.close()
        return render_template('report/edit.html', form=form)

    if request.method == 'GET':
        form = CreateReportForm()
        fill_form_choices(form)
        form.patient.data = str(report.patient)
        form.res.data = report.res
        form.state.data = report.state

        cur.close()
        return render_template('report/edit.html', form=form)


def fill_form_choices(form: CreateReportForm):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        'SELECT * FROM patient',
    )
    form.patient.choices = list(map(lambda p: (p.id, p.name), cur.fetchall()))
    cur.close()

    cur = db.cursor()
    cur.execute(
        "SELECT * FROM res where start_t > timestamp %s",
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),),
    )
    form.res.choices = list(map(lambda r: (r.id, f'{r.start_t} - {r.end_t}'), cur.fetchall()))
    cur.close()

    cur = db.cursor()
    cur.execute(
        "SELECT * FROM state",
    )
    form.state.choices = list(map(lambda s: (s.slug, s.name), cur.fetchall()))
    cur.close()
