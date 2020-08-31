from __future__ import with_statement

from attest import Assert
from flask import current_app
from genshi.filters import Translator
from flaskext.genshi import render_template

from tests.utils import flask_tests


i18n = flask_tests()


@i18n.test
def does_translations():
    """Callback interface is able to inject Translator filter"""

    genshi = current_app.extensions['genshi']
    @genshi.template_parsed
    def callback(template):
        Translator(lambda s: s.upper()).setup(template)

    rendered = Assert(render_template('i18n.html'))
    expected = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                '"http://www.w3.org/TR/html4/strict.dtd">\n'
                '<p>HELLO!</p>')

    assert rendered == expected
