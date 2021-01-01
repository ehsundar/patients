from flask import (
    Blueprint, redirect, render_template, request, url_for, abort
)

from patients.db import get_db
from .forms import OrgCreateForm
from ..row_trans import Model, Org

bp = Blueprint('org', __name__, url_prefix='/org')


@bp.route('/', methods=('GET',))
def index():
    db = get_db()
    cur = db.cursor()

    cur.execute(
        'select * from org',
    )
    orgs = cur.fetchall()
    orgs = list(map(lambda row: Model(Org, row), orgs))

    cur.close()
    return render_template('org/index.html', orgs=orgs)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    conn = get_db()
    cur = conn.cursor()
    form = OrgCreateForm(request.form)

    if request.method == 'POST':
        if form.validate():
            cur.execute(
                'select * from org where slug=%s',
                (form.slug.data,),
            )
            org = cur.fetchone()

            if org:
                form.slug.errors.append(f'org {form.slug.data} already exists')
            else:
                cur.execute(
                    'insert into org (slug, name) values (%s, %s)',
                    (form.slug.data, form.name.data),
                )
                conn.commit()
                cur.close()
                return redirect(url_for('org.index'))

    cur.close()
    return render_template('org/create.html', form=form)


@bp.route('/edit/<slug>', methods=('GET', 'POST'))
def edit(slug: str):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        'select * from org where slug=%s',
        (slug,),
    )
    org = cur.fetchone()
    if not org:
        abort(404)

    org = Model(Org, org)

    if request.method == 'POST':
        form = OrgCreateForm(request.form)

        if form.validate():
            cur.execute(
                'update org set name = %s where slug = %s',
                (form.name.data, slug),
            )
            db.commit()
            cur.close()
            return redirect(url_for('org.index'))

        cur.close()
        return render_template('org/edit.html', form=form)

    if request.method == 'GET':
        form = OrgCreateForm()
        form.slug.data = org.slug
        form.name.data = org.name

        cur.close()
        return render_template('org/edit.html', form=form)
