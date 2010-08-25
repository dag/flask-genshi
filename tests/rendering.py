
from __future__ import absolute_import

from flaskext.genshi import render_response
from flask import g

from .utils import test


@test
def renders_html():
    """A html extension results in an HTML doctype and mimetype"""

    rendered = render_response('test.html', g.context)
    expected_data = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                     '"http://www.w3.org/TR/html4/strict.dtd">\n'
                     '<body>Hi Rudolf</body>')

    assert rendered.mimetype == 'text/html'
    assert rendered.data == expected_data


@test
def renders_text():
    """A txt extension results in no doctype and a text/plain mimetype"""

    rendered = render_response('test.txt', g.context)

    assert rendered.mimetype == 'text/plain'
    assert rendered.data == 'Hi Rudolf\n'


@test
def renders_xml():
    """An xml extension results in no doctype and a application/xml mimetype"""

    rendered = render_response('test.xml', g.context)

    assert rendered.mimetype == 'application/xml'
    assert rendered.data == '<name>Rudolf</name>'


@test
def renders_js():
    """A js extension results in no doctype
    and a application/javascript mimetype

    """

    rendered = render_response('test.js', g.context)

    assert rendered.mimetype == 'application/javascript'
    assert rendered.data == 'alert("Rudolf");\n'


@test
def renders_css():
    """A css extension results in no doctype and a text/css mimetype"""

    rendered = render_response('test.css', g.context)

    assert rendered.mimetype == 'text/css'
    assert rendered.data == 'h1:after { content: " Rudolf"; }\n'


@test
def renders_svg():
    """An svg extension results in an SVG doctype and mimetype"""

    rendered = render_response('test.svg', g.context)
    expected_data = ('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" '
                     '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
                     '<svg viewBox="0 0 1000 300">\n'
                     '<text x="250" y="150" font-size="55">Hi Rudolf</text>\n'
                     '</svg>')

    assert rendered.mimetype == 'image/svg+xml'
    assert rendered.data == expected_data
