import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from patients.db import get_db
from .forms import LoginForm


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        db = get_db()
        form = LoginForm(request.form)

        if not form.validate():
            return render_template('auth/login.html', form=form)
        
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (form.username.data,)
        ).fetchone()

        if not user:
            form.username.errors.append('invalid login')
            return render_template('auth/login.html', form=form)

        if not check_password_hash(user['password'], form.password.data):
            form.password.errors.append('invalid login')
            return render_template('auth/login.html', form=form)

        session.clear()
        session['username'] = user['username']
        return redirect(url_for('home.index'))

    return render_template('auth/login.html', form=LoginForm())


@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')

    if username is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
