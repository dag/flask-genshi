
from __future__ import with_statement

from flask import Flask
from nose.tools import istest as test, assert_equal, raises
from genshi.filters import Transformer

from flaskext.genshi import Genshi, render_response, render_template

import testmodule
import views.test


app = Flask(__name__)
app.register_module(testmodule.mod)
app.register_module(views.test.mod)
genshi = Genshi(app)
context = dict(name='Rudolf')


@test
def renders_html():
    """A html extension results in an HTML doctype and mimetype"""
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
    """An xml extension results in no doctype and a application/xml mimetype"""
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


@test
def renders_svg():
    """An svg extension results in an SVG doctype and mimetype"""
    with app.test_request_context():
        rendered = render_response('test.svg', context)
    assert_equal(rendered.mimetype, 'image/svg+xml')
    assert_equal(rendered.data,
        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" '
        '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
        '<svg viewBox="0 0 1000 300">\n'
        '<text x="250" y="150" font-size="55">Hi Rudolf</text>\n'
        '</svg>')


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


@app.context_processor
def inject_rudolf():
    return dict(rudolf='The red-nosed reindeer')

@test
def updates_context():
    """Render calls update the template context with context processors"""
    with app.test_request_context():
        rendered = render_response('context.html')


@test
def renders_strings():
    """Strings can be rendered as templates directly"""
    with app.test_request_context():
        rendered = render_response(string='The name is $name',
                                   context=context, method='text')
    assert_equal(rendered.data, 'The name is Rudolf')

@test
@raises(RuntimeError)
def fails_without_template_or_string():
    """A template or string must be provided to render"""
    with app.test_request_context():
        render_response(context=context, method='text')


@test
def loads_module_templates():
    """Templates can be loaded from module packages"""
    with app.test_request_context():
        rendered = render_template('testmodule/module-template.txt', context)
    assert_equal(rendered, 'Hello modular Rudolf\n')

@test
def overrides_module_templates():
    """Module templates can be overridden with application templates"""
    with app.test_request_context():
        rendered = render_template('testmodule/nonmodule-template.txt', context)
    assert_equal(rendered, 'Hello nonmodular Rudolf\n')

