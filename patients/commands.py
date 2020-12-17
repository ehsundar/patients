import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash


@click.command('new-user')
@click.option('--username', prompt='Username')
@click.option('--password', prompt='Password')
@click.option('--org-slug', prompt='Organization Slug')
@with_appcontext
def create_user_command(username, password, org_slug):
    """Creates a new user with the passed or prompted arguments"""
    from patients.db import get_db
    db = get_db()
    cur = db.cursor()

    password_hash = generate_password_hash(password)

    cur.execute('INSERT INTO users (username, password, org) VALUES (%s, %s, %s)', (username, password_hash, org_slug))

    db.commit()
    cur.close()

    click.echo('User created.')
