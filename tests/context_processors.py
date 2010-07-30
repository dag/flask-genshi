
from __future__ import absolute_import

from flaskext.genshi import render_response

from .utils import test
from .flask_genshi_testapp import app


@app.context_processor
def inject_rudolf():
    return dict(rudolf='The red-nosed reindeer')


@test
def updates_context():
    """Render calls update the template context with context processors"""

    rendered = render_response('context.html')

