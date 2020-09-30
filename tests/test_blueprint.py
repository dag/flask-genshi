from __future__ import unicode_literals

from flask_genshi import render_template


def test_blueprint_templates(app, context):
    """Templates can be loaded from blueprint packages"""
    with app.test_request_context():
        rendered = render_template("test_blueprint/blueprint-template.txt", context)
        assert rendered == "Hello blueprint Rudolf\n"

        rendered = render_template("test_blueprint/prefix-blueprint-template.txt", context)
        assert rendered == "Hello blueprint Rudolf\n"

        rendered = render_template("prefix-blueprint-template.txt", context)
        assert rendered == "Hello no-prefix-blueprint Rudolf\n"
