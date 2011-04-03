from __future__ import with_statement

from attest import Assert
from flaskext.genshi import render_template

from tests.utils import flask_tests


jinja = flask_tests()


@jinja.test
def provides_jinja_tests_and_filters():
    """Jinja tests and filters should be provided as context dictionaries."""

    rendered = Assert(render_template('jinja_tests_and_filters.html'))
    expected_data = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                     '"http://www.w3.org/TR/html4/strict.dtd">\n'
                     '<p class="odd">\n'
                     '    Hello ...\n'
                     '  <span class="even">\n'
                     '      Hello ...\n'
                     '  </span>\n'
                     '</p>')

    assert rendered == expected_data
