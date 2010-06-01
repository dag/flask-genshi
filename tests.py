
from flask import Flask
from nose.tools import istest as test, \
                       assert_equal as same, \
                       assert_not_equal as differ

from flaskext.genshi import *


app = Flask(__name__)
genshi = Genshi(app)
context = dict(name='Rudolf')


@test
def renders_html():
    """A html extension results in a HTML doctype and mimetype"""
    with app.test_request_context():
        rendered = render_response('test.html', context)
    same(rendered.mimetype, 'text/html')
    same(rendered.data, '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                        '"http://www.w3.org/TR/html4/strict.dtd">\n'
                        '<body>Hi Rudolf</body>')

@test
def renders_text():
    """A txt extension results in no doctype and a text/plain mimetype"""
    with app.test_request_context():
        rendered = render_response('test.txt', context)
    same(rendered.mimetype, 'text/plain')
    same(rendered.data, 'Hi Rudolf\n')


@test
def renders_xml():
    """A xml extension results in no doctype and a application/xml mimetype"""
    with app.test_request_context():
        rendered = render_response('test.xml', context)
    same(rendered.mimetype, 'application/xml')
    same(rendered.data, '<name>Rudolf</name>')


@test
def renders_js():
    """A js extension results in no doctype
    and a application/javascript mimetype"""
    with app.test_request_context():
        rendered = render_response('test.js', context)
    same(rendered.mimetype, 'application/javascript')
    same(rendered.data, 'alert("Rudolf");\n')


@test
def renders_css():
    """A css extension results in no doctype and a text/css mimetype"""
    with app.test_request_context():
        rendered = render_response('test.css', context)
    same(rendered.mimetype, 'text/css')
    same(rendered.data, 'h1:after { content: " Rudolf"; }\n')

