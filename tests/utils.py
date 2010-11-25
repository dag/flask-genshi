from __future__ import with_statement
from contextlib import contextmanager
from flask_genshi_testapp import create_app


@contextmanager
def appcontext():
    app = create_app()
    with app.test_request_context():
        yield
