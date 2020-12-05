import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from patients.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/', methods=('GET',))
def index():
    db = get_db()

    users = db.execute(
        'SELECT * FROM user',
    ).fetchall()
    return render_template('user/index.html', users=users)


@bp.route('/create', methods=('GET',))
def create():
    db = get_db()
    orgs = db.execute(
        'SELECT * FROM org',
    ).fetchall()
    perms = db.execute(
        'SELECT * FROM perm',
    ).fetchall()
    return render_template('user/create.html', orgs=orgs, perms=perms)


@bp.route('/create', methods=('POST',))
def create_post():
    db = get_db()
    err = None

    username = request.form['username']
    if not username:
        err = 'Username is requiered'

    password = request.form['password']
    if not password:
        err = 'Password is requiered'

    user = db.execute(
        'SELECT * FROM user WHERE username=?',
        (username,)
    ).fetchone()
    if user:
        err = f'User {username} already exists'

    if not err:
        db.execute(
            'INSERT INTO user (username, password) VALUES (?, ?)',
            (username, generate_password_hash(password))
        )
        db.commit()
        return redirect(url_for('user.index'))

    flash(err)
    return redirect(url_for('user.index'))


@bp.route('/<username>', methods=('GET',))
def edit(username: str):
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE username=?',
        (username,)
    ).fetchone()
    if not user:
        err = f'User {username} already exists'
        flash(err)
        return redirect(url_for('user.index'))

    orgs = db.execute(
        'SELECT * FROM org',
    ).fetchall()
    perms = db.execute(
        'SELECT * FROM perm',
    ).fetchall()

    return render_template('user/edit.html', user=user, orgs=orgs, perms=perms)


@bp.route('/<username>', methods=('POST',))
def edit_post(username: str):
    db = get_db()
    err = None

    user = db.execute(
        'SELECT * FROM user WHERE username=?',
        (username,)
    ).fetchone()
    if not user:
        err = f'User {username} does not exists'

    new_password = request.form['password']

    db.execute(
        'UPDATE user SET password=? WHERE username=?',
        (generate_password_hash(new_password), username)
    )

    flash(err)
    return redirect(url_for('user.index'))
