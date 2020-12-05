import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from patients.db import get_db

bp = Blueprint('org', __name__, url_prefix='/org')


@bp.route('/', methods=('GET',))
def index():
    db = get_db()

    orgs = db.execute(
        'SELECT * FROM org',
    ).fetchall()
    return render_template('org/index.html', orgs=orgs)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        db = get_db()
        err = None

        slug = request.form['slug']
        if not slug:
            err = 'Slug is requiered'

        name = request.form['name']
        if not name:
            err = 'Name is requiered'

        org = db.execute(
            'SELECT * FROM org WHERE slug=?',
            (slug,),
        ).fetchone()
        if org:
            err = f'Org {slug} already exists'
        else:
            db.execute(
                'INSERT INTO org (slug, name) VALUES (?, ?)',
                (slug, name),
            )
            db.commit()

        if err:
            flash(err)
        return redirect(url_for('org.index'))

    return render_template('org/create.html')


@bp.route('/edit/<slug>', methods=('GET',))
def edit(slug: str):
    db = get_db()

    org = db.execute(
        'SELECT * FROM org WHERE slug=?',
        (slug,),
    ).fetchone()
    return render_template('org/edit.html', org=org)


@bp.route('/edit/<slug>', methods=('POST',))
def edit_post(slug: str):
    db = get_db()
    err = None

    org = db.execute(
        'SELECT * FROM org WHERE slug=?',
        (slug,),
    ).fetchone()
    if not org:
        err = f'Org {slug} does not exists'

    name = request.form['name']
    db.execute(
        'UPDATE org SET name=? WHERE slug=?',
        (name, slug),
    )

    flash(err)
    return redirect(url_for('org.edit', slug=slug))
