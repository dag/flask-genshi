
from __future__ import absolute_import

from flaskext.genshi import render_template

from .utils import test


@test
def provides_jinja_tests_and_filters():
    """Jinja tests and filters should be provided as context dictionaries."""

    rendered = render_template('jinja_tests_and_filters.html')
    expected_data = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                     '"http://www.w3.org/TR/html4/strict.dtd">\n'
                     '<p class="odd">\n'
                     '    Hello ...\n'
                     '</p>')

    assert rendered == expected_data
