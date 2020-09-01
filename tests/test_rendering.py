from __future__ import unicode_literals

from inspect import cleandoc

from flask_genshi import render_response, render


def test_renders_html(app, context):
    """A html extension results in an HTML doctype and mimetype"""
    with app.test_request_context():
        rendered = render_response("test.html", context)
        expected_data = cleandoc(
            """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
            <body>Hi Rudolf</body>
            """
        ).encode("UTF-8")

        assert rendered.mimetype == "text/html"
        assert rendered.data == expected_data


def test_renders_text(app, context):
    """A txt extension results in no doctype and a text/plain mimetype"""
    with app.test_request_context():
        rendered = render_response("test.txt", context)

        assert rendered.mimetype == "text/plain"
        assert rendered.data == b"Hi Rudolf\n"


def test_renders_xml(app, context):
    """An xml extension results in no doctype and a application/xml mimetype"""
    with app.test_request_context():
        rendered = render_response("test.xml", context)
        assert rendered.mimetype == "application/xml"
        assert rendered.data == b"<name>Rudolf</name>"

        rendered = render("test.xml", **context)
        assert rendered.mimetype == "application/xml"
        assert rendered.data == b"<name>Rudolf</name>"


def test_renders_js(app, context):
    """
    A js extension results in no doctype and a application/javascript mimetype
    """
    with app.test_request_context():
        rendered = render_response("test.js", context)

        assert rendered.mimetype == "application/javascript"
        assert rendered.data == b'alert("Rudolf");\n'


def test_renders_css(app, context):
    """A css extension results in no doctype and a text/css mimetype"""
    with app.test_request_context():
        rendered = render_response("test.css", context)

        assert rendered.mimetype == "text/css"
        assert rendered.data == b'h1:after { content: " Rudolf"; }\n'


def test_renders_svg(app, context):
    """An svg extension results in an SVG doctype and mimetype"""
    with app.test_request_context():
        rendered = render_response("test.svg", context)
        expected_data = cleandoc(
            """
            <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
            <svg viewBox="0 0 1000 300">
            <text x="250" y="150" font-size="55">Hi Rudolf</text>
            </svg>
            """
        ).encode("UTF-8")

        assert rendered.mimetype == "image/svg+xml"
        assert rendered.data == expected_data
