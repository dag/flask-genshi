
from __future__ import absolute_import

from genshi.filters import Transformer
from flaskext.genshi import render_template
from flatland.out.genshi import flatland_filter
from flatland import Form, String

from .utils import test
from .flask_genshi_testapp.extensions import genshi


class TestForm(Form):

    username = String


@genshi.filter('html')
def prepend_title(template):
    return template | Transformer('head/title').prepend('Flask-Genshi - ')


@genshi.filter('html')
def inject_flatland(template, context):
    return flatland_filter(template, context)


@test
def applies_filters():
    """Filters are applied for generated and rendered templates"""

    rendered = render_template('filter.html')
    expected = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                '"http://www.w3.org/TR/html4/strict.dtd">\n'
                '<html><head><title>Flask-Genshi - Hi!</title></head></html>')

    assert rendered == expected


@test
def works_with_flatland():
    """Filters can take the context and support flatland"""

    context = dict(form=TestForm({'username': 'dag'}))
    rendered = render_template('flatland.html', context)
    expected = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                '"http://www.w3.org/TR/html4/strict.dtd">\n'
                '<input type="text" name="username" value="dag">')

    assert rendered == expected
