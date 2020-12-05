import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from patients.db import get_db
from patients.auth import login_required

bp = Blueprint('patient', __name__, url_prefix='/patient')


@bp.route('/', methods=('GET',))
def index():
    db = get_db()

    patients = db.execute(
        'SELECT * FROM patient',
    ).fetchall()
    return render_template('patient/index.html', patients=patients)


@login_required
@bp.route('/create', methods=('GET',))
def create():
    return render_template('patient/create.html')


@login_required
@bp.route('/create', methods=('POST',))
def create_post():
    db = get_db()
    err = None
    phone = request.form['phone']
    if not phone:
        err = 'Phone is requiered'

    name = request.form['name']
    if not name:
        err = 'Name is required'

    gender = request.form['gender']
    if not gender:
        err = 'Gender is required'

    if err:
        flash(err)
        return redirect(url_for('patient.create'))

    db.execute(
        'INSERT INTO patient (phone, name, gender, creator_user) VALUES (?,?,?,?)',
        (phone, name, gender, g.user['username']),
    )
    db.commit()

    return redirect(url_for('patient.index'))


@bp.route('/edit/<int:pk>', methods=('GET',))
def edit(pk: int):
    db = get_db()

    patient = db.execute(
        'SELECT * FROM patient WHERE id=?',
        (pk,),
    ).fetchone()
    return render_template('patient/edit.html', patient=patient)


@bp.route('/edit/<int:pk>', methods=('POST',))
def edit_post(pk: int):
    db = get_db()
    err = None

    patient = db.execute(
        'SELECT * FROM patient WHERE id=?',
        (pk,),
    ).fetchone()
    if not patient:
        err = f'Patient {pk} does not exists'
        flash(err)
        return redirect(url_for('patient.edit', pk=pk))

    phone = request.form['phone']
    if not phone:
        err = f'Phone is required'
        flash(err)
    name = request.form['name']
    if not name:
        err = f'Name is required'
        flash(err)
    gender = request.form['gender']
    if not gender:
        err = f'Gender is required'
        flash(err)

    if not err:
        db.execute(
            'UPDATE patient SET phone=?, name=?, gender=? WHERE id=?',
            (phone, name, gender, pk),
        )
        db.commit()

    return redirect(url_for('patient.edit', pk=pk))
