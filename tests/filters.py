
from __future__ import absolute_import

from genshi.filters import Transformer
from flaskext.genshi import render_template

from .utils import test
from .flask_genshi_testapp import genshi


@genshi.filter('html')
def prepend_title(template):
    return template | Transformer('head/title').prepend('Flask-Genshi - ')


@test
def applies_filters():
    """Filters are applied for generated and rendered templates"""

    rendered = render_template('filter.html')
    expected = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                '"http://www.w3.org/TR/html4/strict.dtd">\n'
                '<html><head><title>Flask-Genshi - Hi!</title></head></html>')

    assert rendered == expected

