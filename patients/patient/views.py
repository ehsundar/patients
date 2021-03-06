from flask import (
    Blueprint, g, redirect, render_template, request, url_for, abort
)

from patients.auth import login_required
from patients.db import get_db
from patients.patient.forms import CreatePatientForm
from patients.row_trans import Model, Patient

bp = Blueprint('patient', __name__, url_prefix='/patient')


@bp.route('/', methods=('GET',))
def index():
    db = get_db()
    cur = db.cursor()

    cur.execute(
        'select * from patient',
    )
    patients = cur.fetchall()
    patients = list(map(lambda row: Model(Patient, row), patients))

    cur.close()
    return render_template('patient/index.html', patients=patients)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    db = get_db()
    cur = db.cursor()
    form = CreatePatientForm(request.form)

    if request.method == 'POST' and form.validate():
        cur.execute(
            'insert into patient (phone, name, gender, creator_user) values (%s,%s,%s,%s)',
            (form.phone.data, form.name.data, form.gender.data, g.user.username),
        )
        db.commit()
        cur.close()
        return redirect(url_for('patient.index'))

    cur.close()
    return render_template('patient/create.html', form=form)


@bp.route('/edit/<int:pk>', methods=('GET', 'POST'))
def edit(pk: int):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        'select * from patient where id=%s',
        (pk,),
    )
    patient = cur.fetchone()
    if not patient:
        abort(404)

    patient = Model(Patient, patient)

    if request.method == 'POST':
        form = CreatePatientForm(request.form)

        if form.validate():
            cur.execute(
                'update patient set phone = %s, name = %s, gender = %s where id=%s',
                (form.phone.data, form.name.data, form.gender.data, pk),
            )
            db.commit()
            cur.close()
            return redirect(url_for('patient.index'))

        cur.close()
        return render_template('patient/edit.html', form=form)

    if request.method == 'GET':
        form = CreatePatientForm()
        form.name.data = patient.name
        form.phone.data = patient.phone
        form.gender.data = patient.gender

        cur.close()
        return render_template('patient/edit.html', form=form)
