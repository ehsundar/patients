import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from werkzeug.security import check_password_hash, generate_password_hash

from patients.db import get_db
from patients.auth import login_required
from patients.patient.forms import CreatePatientForm


bp = Blueprint('patient', __name__, url_prefix='/patient')


@bp.route('/', methods=('GET',))
def index():
    db = get_db()

    patients = db.execute(
        'SELECT * FROM patient',
    ).fetchall()
    return render_template('patient/index.html', patients=patients)


@login_required
@bp.route('/create', methods=('GET', 'POST'))
def create():
    db = get_db()
    form = CreatePatientForm(request.form)

    if request.method == 'POST' and form.validate():
        db.execute(
            'INSERT INTO patient (phone, name, gender, creator_user) VALUES (?,?,?,?)',
            (form.phone.data, form.name.data,
             form.gender.data, g.user['username']),
        )
        db.commit()
    return render_template('patient/create.html', form=form)


@bp.route('/edit/<int:pk>', methods=('GET', 'POST'))
def edit(pk: int):
    db = get_db()

    patient = db.execute(
        'SELECT * FROM patient WHERE id=?',
        (pk,),
    ).fetchone()
    if not patient:
        abort(404)

    if request.method == 'POST':
        form = CreatePatientForm(request.form)

        if form.validate():
            db.execute(
                'UPDATE patient SET phone=?, name=?, gender=? WHERE id=?',
                (form.phone.data, form.name.data, form.gender.data, pk),
            )
            db.commit()
            return redirect(url_for('patient.index'))
        return render_template('patient/edit.html', form=form)

    if request.method == 'GET':
        form = CreatePatientForm()
        form.name.data = patient['name']
        form.phone.data = patient['phone']
        form.gender.data = patient['gender']

        return render_template('patient/edit.html', form=form)
