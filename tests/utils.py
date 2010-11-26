from __future__ import with_statement
from attest import Tests

from flask_genshi_testapp import create_app


def flask_tests():
    tests = Tests()
    @tests.context
    def request_context():
        app = create_app()
        with app.test_request_context():
            yield dict(name='Rudolf')
    return tests
