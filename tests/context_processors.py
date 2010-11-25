from __future__ import with_statement

from attest import Tests
from flask import current_app
from flaskext.genshi import render_response

from tests.utils import appcontext


contexts = Tests()

@contexts.context
def context():
    with appcontext():
        yield


@contexts.test
def updates_context():
    """Render calls update the template context with context processors"""

    @current_app.context_processor
    def inject_rudolf():
        return dict(rudolf='The red-nosed reindeer')

    render_response('context.html')
