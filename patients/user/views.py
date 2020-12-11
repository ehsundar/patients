import functools
from sqlite3 import Connection

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from werkzeug.security import check_password_hash, generate_password_hash

from patients.db import get_db
from .forms import CreateUserForm


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
    form = CreateUserForm()

    fill_form_org_and_perms(db, form)

    return render_template('user/create.html', form=form)


@bp.route('/create', methods=('POST',))
def create_post():
    db = get_db()
    form = CreateUserForm(request.form)

    fill_form_org_and_perms(db, form)

    if form.validate():
        user = db.execute(
            'SELECT * FROM user WHERE username=?',
            (form.username.data,)
        ).fetchone()
        if user:
            form.username.errors.append(
                f'Username {form.username.data} already exists')
            return render_template('user/create.html', form=form)

        db.execute(
            'INSERT INTO user (username, password, org) VALUES (?, ?, ?)',
            (form.username.data, generate_password_hash(
                form.password.data), form.org.data)
        )
        db.commit()

        flash('User created')
        return redirect(url_for('user.index'))

    return render_template('user/create.html', form=form)


@bp.route('/<username>', methods=('GET',))
def edit(username: str):
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE username=?',
        (username,)
    ).fetchone()
    if not user:
        abort(404)

    form = CreateUserForm(request.form)
    fill_form_org_and_perms(db, form)

    form.username.data = user['username']
    form.password.data = '*' * 8
    form.org.data = user['org']
    form.org.default = user['org']
    form.perms.default = []

    return render_template('user/edit.html', form=form)


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


def fill_form_org_and_perms(db: Connection, form: CreateUserForm):
    orgs = db.execute(
        'SELECT * FROM org',
    ).fetchall()
    perms = db.execute(
        'SELECT * FROM perm',
    ).fetchall()

    orgs_list = list(
        map(lambda o: (o['slug'], o['slug'] + ' - ' + o['name']), orgs))
    form.org.choices = orgs_list

    perms_list = list(
        map(lambda o: (o['slug'], o['slug'] + ' - ' + o['name']), perms)
    )
    form.perms.choices = perms_list
