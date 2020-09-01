from __future__ import unicode_literals

from inspect import cleandoc

from genshi.filters import Translator
from flask_genshi import render_template


def test_does_translations(app):
    """Callback interface is able to inject Translator filter"""
    with app.test_request_context():

        genshi = app.extensions["genshi"]

        @genshi.template_parsed
        def callback(template):
            Translator(lambda s: s.upper()).setup(template)

        rendered = render_template("i18n.html")
        expected = cleandoc(
            """
            <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
            <p>HELLO!</p>
            """
        )

        assert rendered == expected
