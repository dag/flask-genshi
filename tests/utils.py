
from __future__ import with_statement

from functools import wraps

from nose.tools import nottest, istest
from flask import g

from flask_genshi_testapp import create_app


@nottest
def test(f):
    """Mark a function as a test and wrap it in a request context."""

    @istest
    @wraps(f)
    def wrapper():
        app = create_app()
        with app.test_request_context():
            g.context = dict(name='Rudolf')
            f()

    return wrapper
