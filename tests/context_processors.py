from __future__ import with_statement

from flask import current_app
from flaskext.genshi import render_response

from tests.utils import flask_tests


contexts = flask_tests()


@contexts.test
def updates_context():
    """Render calls update the template context with context processors"""

    @current_app.context_processor
    def inject_rudolf():
        return dict(rudolf='The red-nosed reindeer')

    render_response('context.html')
