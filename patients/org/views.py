import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)

from patients.db import get_db
from .forms import OrgCreateForm


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
    form = OrgCreateForm(request.form)

    if request.method == 'POST':
        db = get_db()

        if form.validate():
            org = db.execute(
                'SELECT * FROM org WHERE slug=?',
                (form.slug.data,),
            ).fetchone()

            if org:
                form.slug.errors.append(f'org {form.slug.data} already exists')
            else:
                db.execute(
                    'INSERT INTO org (slug, name) VALUES (?, ?)',
                    (form.slug.data, form.name.data),
                )
                db.commit()
                return redirect(url_for('org.index'))

    return render_template('org/create.html', form=form)


@bp.route('/edit/<slug>', methods=('GET', 'POST'))
def edit(slug: str):
    db = get_db()

    org = db.execute(
        'SELECT * FROM org WHERE slug=?',
        (slug,),
    ).fetchone()
    if not org:
        abort(404)

    if request.method == 'POST':
        form = OrgCreateForm(request.form)

        if form.validate():
            db.execute(
                'UPDATE org SET name=? WHERE slug=?',
                (form.name.data, slug),
            )
            db.commit()
            return redirect(url_for('org.index'))

        return render_template('org/edit.html', form=form)
    
    if request.method == 'GET':
        form = OrgCreateForm()
        form.slug.data = org['slug']
        form.name.data = org['name']

        return render_template('org/edit.html', form=form)
