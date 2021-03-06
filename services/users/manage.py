import unittest
from unittest import result

from flask.cli import FlaskGroup
import coverage

from project import create_app, db
from project.api.models import User


app = create_app()
cli = FlaskGroup(create_app=create_app)

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py'
    ]
)
COV.start()

@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('tests')
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage summary:')
        COV.report()
        COV.html_report()
        COV.erase
        return 0
    return 1

@cli.command('seed_db')
def seed_db():
    db.session.add(User(username='johndoe', email='johndoe@gmail.com'))
    db.session.add(User(username='johnwick', email='johnwick@gmail.com'))
    db.session.commit()


if __name__ == '__main__':
    cli()

