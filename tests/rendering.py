from __future__ import with_statement
from attest import Assert
from flaskext.genshi import render_response, render
from tests.utils import flask_tests


rendering = flask_tests()


@rendering.test
def renders_html(context):
    """A html extension results in an HTML doctype and mimetype"""

    rendered = Assert(render_response('test.html', context))
    expected_data = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                     '"http://www.w3.org/TR/html4/strict.dtd">\n'
                     '<body>Hi Rudolf</body>')

    assert rendered.mimetype == 'text/html'
    assert rendered.data == expected_data


@rendering.test
def renders_text(context):
    """A txt extension results in no doctype and a text/plain mimetype"""

    rendered = Assert(render_response('test.txt', context))

    assert rendered.mimetype == 'text/plain'
    assert rendered.data == 'Hi Rudolf\n'


@rendering.test
def renders_xml(context):
    """An xml extension results in no doctype and a application/xml mimetype"""

    rendered = Assert(render_response('test.xml', context))
    assert rendered.mimetype == 'application/xml'
    assert rendered.data == '<name>Rudolf</name>'

    rendered = Assert(render('test.xml', **context))
    assert rendered.mimetype == 'application/xml'
    assert rendered.data == '<name>Rudolf</name>'


@rendering.test
def renders_js(context):
    """A js extension results in no doctype
    and a application/javascript mimetype

    """

    rendered = Assert(render_response('test.js', context))

    assert rendered.mimetype == 'application/javascript'
    assert rendered.data == 'alert("Rudolf");\n'


@rendering.test
def renders_css(context):
    """A css extension results in no doctype and a text/css mimetype"""

    rendered = Assert(render_response('test.css', context))

    assert rendered.mimetype == 'text/css'
    assert rendered.data == 'h1:after { content: " Rudolf"; }\n'


@rendering.test
def renders_svg(context):
    """An svg extension results in an SVG doctype and mimetype"""

    rendered = Assert(render_response('test.svg', context))
    expected_data = ('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" '
                     '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
                     '<svg viewBox="0 0 1000 300">\n'
                     '<text x="250" y="150" font-size="55">Hi Rudolf</text>\n'
                     '</svg>')

    assert rendered.mimetype == 'image/svg+xml'
    assert rendered.data == expected_data
