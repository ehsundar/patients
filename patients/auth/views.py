import functools

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash

from patients.db import get_db
from .forms import LoginForm
from ..row_trans import Model, User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        db = get_db()
        cur = db.cursor()
        form = LoginForm(request.form)

        if not form.validate():
            return render_template('auth/login.html', form=form)

        cur.execute(
            'select * from users where username = %s',
            (form.username.data,)
        )
        user = cur.fetchone()
        user = Model(User, user)

        if not user:
            form.username.errors.append('invalid login')
            return render_template('auth/login.html', form=form)

        if not check_password_hash(user.password, form.password.data):
            form.password.errors.append('invalid login')
            return render_template('auth/login.html', form=form)

        session.clear()
        session['username'] = user.username
        return redirect(url_for('home.index'))

    return render_template('auth/login.html', form=LoginForm())


@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')

    if username is None:
        g.user = None
    else:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            'select * from users where username = %s', (username,)
        )
        g.user = cur.fetchone()
        cur.close()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function
