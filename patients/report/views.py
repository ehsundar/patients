from flask import (
    Blueprint, g, redirect, render_template, request, url_for, abort
)

from patients.auth import login_required
from patients.db import get_db
from patients.report.forms import CreateReportForm

bp = Blueprint('report', __name__, url_prefix='/report')


@bp.route('/', methods=('GET',))
def index():
    db = get_db()
    cur = db.cursor()

    cur.execute(
        'SELECT report.id, patient.name FROM report LEFT JOIN patient on patient.id = report.patient',
    )
    reports = cur.fetchall()

    cur.close()
    return render_template('report/index.html', reports=reports)


@login_required
@bp.route('/create', methods=('GET', 'POST'))
def create():
    db = get_db()
    cur = db.cursor()
    form = CreateReportForm(request.form)
    fill_form_patients(form)

    if request.method == 'POST' and form.validate():
        cur.execute(
            'INSERT INTO report (patient, creator_user) VALUES (%s,%s)',
            (form.patient.data, g.user.username),
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
        fill_form_patients(form)

        if form.validate():
            cur.execute(
                'UPDATE report SET patient = %s WHERE id=%s',
                (form.patient.data, pk),
            )
            db.commit()
            cur.close()
            return redirect(url_for('report.index'))

        cur.close()
        return render_template('report/edit.html', form=form)

    if request.method == 'GET':
        form = CreateReportForm()
        fill_form_patients(form)
        form.patient.data = str(report.patient)

        cur.close()
        return render_template('report/edit.html', form=form)


def fill_form_patients(form: CreateReportForm):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        'SELECT * FROM patient',
    )

    form.patient.choices = list(map(lambda p: (p.id, p.name), cur.fetchall()))
    cur.close()
