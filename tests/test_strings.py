import pytest
from flask_genshi import render_response


def test_renders_strings(app, context):
    """Strings can be rendered as templates directly"""
    with app.test_request_context():
        rendered = render_response(
            string="The name is $name", context=context, method="text"
        )

        assert rendered.data == "The name is Rudolf"


def test_fails_without_template_or_string(app, context):
    """A template or string must be provided to render"""
    with app.test_request_context():
        with pytest.raises(RuntimeError):
            render_response(context=context, method="text")
