
from __future__ import with_statement

from nose.tools import istest as test, with_setup, assert_equal, raises
from flaskext.genshi import render_response, render_template
from genshi.filters import Transformer

from flask_genshi_testapp import app, genshi

context = dict(name='Rudolf')


def setup():
    global request_context
    request_context = app.test_request_context()
    request_context.push()

def teardown():
    request_context.pop()


@test
@with_setup(setup, teardown)
def renders_html():
    """A html extension results in an HTML doctype and mimetype"""
    rendered = render_response('test.html', context)
    assert_equal(rendered.mimetype, 'text/html')
    assert_equal(rendered.data,
        '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
        '"http://www.w3.org/TR/html4/strict.dtd">\n'
        '<body>Hi Rudolf</body>')

@test
@with_setup(setup, teardown)
def renders_text():
    """A txt extension results in no doctype and a text/plain mimetype"""
    rendered = render_response('test.txt', context)
    assert_equal(rendered.mimetype, 'text/plain')
    assert_equal(rendered.data, 'Hi Rudolf\n')


@test
@with_setup(setup, teardown)
def renders_xml():
    """An xml extension results in no doctype and a application/xml mimetype"""
    rendered = render_response('test.xml', context)
    assert_equal(rendered.mimetype, 'application/xml')
    assert_equal(rendered.data, '<name>Rudolf</name>')


@test
@with_setup(setup, teardown)
def renders_js():
    """A js extension results in no doctype
    and a application/javascript mimetype"""
    rendered = render_response('test.js', context)
    assert_equal(rendered.mimetype, 'application/javascript')
    assert_equal(rendered.data, 'alert("Rudolf");\n')


@test
@with_setup(setup, teardown)
def renders_css():
    """A css extension results in no doctype and a text/css mimetype"""
    rendered = render_response('test.css', context)
    assert_equal(rendered.mimetype, 'text/css')
    assert_equal(rendered.data, 'h1:after { content: " Rudolf"; }\n')


@test
@with_setup(setup, teardown)
def renders_svg():
    """An svg extension results in an SVG doctype and mimetype"""
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
@with_setup(setup, teardown)
def applies_filters():
    """Filters are applied for generated and rendered templates"""
    rendered = render_template('filter.html')
    assert_equal(rendered,
        '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
        '"http://www.w3.org/TR/html4/strict.dtd">\n'
        '<html><head><title>Flask-Genshi - Hi!</title></head></html>')


@app.context_processor
def inject_rudolf():
    return dict(rudolf='The red-nosed reindeer')

@test
@with_setup(setup, teardown)
def updates_context():
    """Render calls update the template context with context processors"""
    rendered = render_response('context.html')


@test
@with_setup(setup, teardown)
def renders_strings():
    """Strings can be rendered as templates directly"""
    rendered = render_response(string='The name is $name',
                               context=context, method='text')
    assert_equal(rendered.data, 'The name is Rudolf')

@test
@with_setup(setup, teardown)
@raises(RuntimeError)
def fails_without_template_or_string():
    """A template or string must be provided to render"""
    render_response(context=context, method='text')


@test
@with_setup(setup, teardown)
def loads_module_templates():
    """Templates can be loaded from module packages"""
    rendered = render_template('package_mod/module-template.txt', context)
    assert_equal(rendered, 'Hello modular Rudolf\n')

@test
@with_setup(setup, teardown)
def overrides_module_templates():
    """Module templates can be overridden with application templates"""
    rendered = render_template('package_mod/nonmodule-template.txt', context)
    assert_equal(rendered, 'Hello nonmodular Rudolf\n')

