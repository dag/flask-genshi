from __future__ import with_statement

from contextlib import contextmanager

from attest import Tests, Assert
from flaskext.genshi import template_generated, render_template
from flask import current_app

from tests.utils import appcontext


@contextmanager
def captured_templates(app):
    recorded = Assert([])
    def record(app, template, context):
        recorded.append((template, context))
    template_generated.connect(record, app)
    try:
        yield recorded
    finally:
        template_generated.disconnect(record, app)


signals = Tests()

@signals.context
def context():
    with appcontext():
        yield dict(name='Rudolf')


@signals.test
def signals_are_emitted(context):
    """Signal is emitted when templates are generated"""

    app = current_app._get_current_object()
    with captured_templates(app) as templates:
        render_template('test.html', context)

    assert templates.__len__() == 1
    assert templates[0][0].filename == 'test.html'
    assert templates[0][1]['name'] == 'Rudolf'
