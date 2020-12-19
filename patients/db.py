import click
import psycopg2
import psycopg2.extras
from flask import current_app, g
from flask.cli import with_appcontext

from patients.commands import create_user_command


def get_db():
    if 'db' not in g:
        conn = psycopg2.connect(host='localhost', database='patients', user='postgres', password='testpass',
                                cursor_factory=psycopg2.extras.NamedTupleCursor)
        g.db = conn
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_user_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db = get_db()
    cur = db.cursor()

    with current_app.open_resource('schema.sql') as f:
        cur.execute(f.read().decode())

    with current_app.open_resource('preset.sql') as f:
        cur.execute(f.read().decode())

    db.commit()
    cur.close()

    click.echo('Initialized the database.')
