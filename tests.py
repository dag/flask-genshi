
from __future__ import with_statement

from flask import Flask
from nose.tools import istest as test, assert_equal
from genshi.filters import Transformer

from flaskext.genshi import Genshi, render_response, render_template


app = Flask(__name__)
genshi = Genshi(app)
context = dict(name='Rudolf')


@test
def renders_html():
    """A html extension results in a HTML doctype and mimetype"""
    with app.test_request_context():
        rendered = render_response('test.html', context)
    assert_equal(rendered.mimetype, 'text/html')
    assert_equal(rendered.data,
        '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
        '"http://www.w3.org/TR/html4/strict.dtd">\n'
        '<body>Hi Rudolf</body>')

@test
def renders_text():
    """A txt extension results in no doctype and a text/plain mimetype"""
    with app.test_request_context():
        rendered = render_response('test.txt', context)
    assert_equal(rendered.mimetype, 'text/plain')
    assert_equal(rendered.data, 'Hi Rudolf\n')


@test
def renders_xml():
    """A xml extension results in no doctype and a application/xml mimetype"""
    with app.test_request_context():
        rendered = render_response('test.xml', context)
    assert_equal(rendered.mimetype, 'application/xml')
    assert_equal(rendered.data, '<name>Rudolf</name>')


@test
def renders_js():
    """A js extension results in no doctype
    and a application/javascript mimetype"""
    with app.test_request_context():
        rendered = render_response('test.js', context)
    assert_equal(rendered.mimetype, 'application/javascript')
    assert_equal(rendered.data, 'alert("Rudolf");\n')


@test
def renders_css():
    """A css extension results in no doctype and a text/css mimetype"""
    with app.test_request_context():
        rendered = render_response('test.css', context)
    assert_equal(rendered.mimetype, 'text/css')
    assert_equal(rendered.data, 'h1:after { content: " Rudolf"; }\n')


@genshi.filter('html')
def prepend_title(template):
    return template | Transformer('head/title').prepend('Flask-Genshi - ')

@test
def applies_filters():
    """Filters are applied for generated and rendered templates"""
    with app.test_request_context():
        rendered = render_template('filter.html')
    assert_equal(rendered,
        '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
        '"http://www.w3.org/TR/html4/strict.dtd">\n'
        '<html><head><title>Flask-Genshi - Hi!</title></head></html>')

