
from __future__ import absolute_import

from flask import current_app
from flaskext.genshi import render_response

from .utils import test


@test
def updates_context():
    """Render calls update the template context with context processors"""

    @current_app.context_processor
    def inject_rudolf():
        return dict(rudolf='The red-nosed reindeer')

    render_response('context.html')
