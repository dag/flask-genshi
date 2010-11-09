
from __future__ import absolute_import
from __future__ import with_statement

from contextlib import contextmanager

from flaskext.genshi import template_generated, render_template
from flask import current_app, g

from .utils import test


@contextmanager
def captured_templates(app):
    recorded = []
    def record(app, template, context):
        recorded.append((template, context))
    template_generated.connect(record, app)
    try:
        yield recorded
    finally:
        template_generated.disconnect(record, app)

@test
def signals_are_emitted():
    """Signal is emitted when templates are generated"""

    app = current_app._get_current_object()
    with captured_templates(app) as templates:
        render_template('test.html', g.context)

    assert len(templates) == 1
    assert templates[0][0].filename == 'test.html'
    assert templates[0][1]['name'] == 'Rudolf'
