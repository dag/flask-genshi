from contextlib import contextmanager

from flask_genshi import template_generated, render_template


@contextmanager
def captured_templates(app):
    recorded = []

    def record(_app, template, context):
        recorded.append((template, context))

    template_generated.connect(record, app)
    try:
        yield recorded
    finally:
        template_generated.disconnect(record, app)


def test_signals_are_emitted(app, context):
    """Signal is emitted when templates are generated"""
    with app.test_request_context():

        with captured_templates(app) as templates:
            render_template("test.html", context)

        assert templates.__len__() == 1
        assert templates[0][0].filename == "test.html"
        assert templates[0][1]["name"] == "Rudolf"
