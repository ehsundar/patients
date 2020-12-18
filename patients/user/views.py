import psycopg2.extras
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, abort
)
from werkzeug.security import generate_password_hash

from patients.db import get_db
from patients.row_trans import Model, User
from .forms import CreateUserForm

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/', methods=('GET',))
def index():
    db = get_db()
    cur = db.cursor()

    cur.execute(
        'SELECT * FROM users',
    )
    users = cur.fetchall()
    users = list(map(lambda row: Model(User, row), users))

    cur.close()
    return render_template('user/index.html', users=users)


@bp.route('/create', methods=('GET',))
def create():
    form = CreateUserForm()
    fill_form_org_and_perms(form)
    return render_template('user/create.html', form=form)


@bp.route('/create', methods=('POST',))
def create_post():
    db = get_db()
    cur = db.cursor()
    form = CreateUserForm(request.form)

    fill_form_org_and_perms(form)

    if form.validate():
        cur.execute(
            'SELECT * FROM users WHERE username=%s',
            (form.username.data,)
        )
        user = cur.fetchone()

        if user:
            form.username.errors.append(
                f'Username {form.username.data} already exists')
            return render_template('user/create.html', form=form)

        cur.execute(
            'INSERT INTO users (username, password, org) VALUES (%s, %s, %s)',
            (form.username.data, generate_password_hash(form.password.data), form.org.data)
        )
        db.commit()
        cur.close()

        flash('User created')
        return redirect(url_for('user.index'))

    cur.close()
    return render_template('user/create.html', form=form)


@bp.route('/<username>', methods=('GET',))
def edit(username: str):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        'SELECT * FROM users WHERE username=%s',
        (username,)
    )
    user = cur.fetchone()
    user = Model(User, user)
    if not user:
        abort(404)

    form = CreateUserForm(request.form)
    fill_form_org_and_perms(form)

    form.username.data = user['username']
    form.password.data = '*' * 8
    form.org.data = user['org']
    form.org.default = user['org']
    form.perms.default = []

    cur.close()
    return render_template('user/edit.html', form=form)


@bp.route('/<username>', methods=('POST',))
def edit_post(username: str):
    db = get_db()
    cur = db.cursor()
    err = None

    cur.execute(
        'SELECT * FROM users WHERE username=%s',
        (username,)
    )
    user = cur.fetchone()
    if not user:
        err = f'User {username} does not exists'

    new_password = request.form['password']

    cur.execute(
        'UPDATE users SET password = %s WHERE username=%s',
        (generate_password_hash(new_password), username)
    )
    db.commit()
    cur.close()
    flash(err)
    return redirect(url_for('user.index'))


def fill_form_org_and_perms(form: CreateUserForm):
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

    cur.execute(
        'SELECT * FROM org',
    )
    orgs = cur.fetchall()

    cur.execute(
        'SELECT * FROM perm',
    )
    perms = cur.fetchall()

    orgs_list = list(
        map(lambda o: (o.slug, o.slug + ' - ' + o.name), orgs))
    form.org.choices = orgs_list

    perms_list = list(
        map(lambda o: (o.slug, o.slug + ' - ' + o.name), perms)
    )
    form.perms.choices = perms_list

    cur.close()
