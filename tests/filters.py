
from __future__ import absolute_import

from genshi.filters import Transformer
from flask import current_app
from flaskext.genshi import render_template
from flatland.out.genshi import flatland_filter
from flatland import Form, String

from .utils import test


class TestForm(Form):

    username = String


@test
def applies_method_filters():
    """Method filters are applied for generated and rendered templates"""

    genshi = current_app.extensions['genshi']
    @genshi.filter('html')
    def prepend_title(template):
        return template | Transformer('head/title').prepend('Flask-Genshi - ')

    rendered = render_template('filter.html')
    expected = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                '"http://www.w3.org/TR/html4/strict.dtd">\n'
                '<html><head><title>Flask-Genshi - Hi!</title></head></html>')

    assert rendered == expected


@test
def filters_per_render():
    """Filters can be applied per rendering"""

    def prepend_title(template):
        return template | Transformer('head/title').append(' - Flask-Genshi')

    rendered = render_template('filter.html', filter=prepend_title)
    expected = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                '"http://www.w3.org/TR/html4/strict.dtd">\n'
                '<html><head><title>Hi! - Flask-Genshi</title></head></html>')

    assert rendered == expected


@test
def works_with_flatland():
    """Filters can take the context and support flatland"""

    genshi = current_app.extensions['genshi']
    @genshi.filter('html')
    def inject_flatland(template, context):
        return flatland_filter(template, context)

    context = dict(form=TestForm({'username': 'dag'}))
    rendered = render_template('flatland.html', context)
    expected = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                '"http://www.w3.org/TR/html4/strict.dtd">\n'
                '<input type="text" name="username" value="dag">')

    assert rendered == expected
