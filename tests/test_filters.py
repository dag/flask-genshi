import inspect

from genshi.filters import Transformer
from flaskext.genshi import render_template
from flatland.out.genshi import setup as flatland_setup
from flatland import Form, String


class FlatlandForm(Form):

    username = String


def test_applies_method_filters(app):
    """Method filters are applied for generated and rendered templates"""
    with app.test_request_context():
        genshi = app.extensions["genshi"]

        @genshi.filter("html")
        def prepend_title(template):
            return template | Transformer("head/title").prepend("Flask-Genshi - ")

        rendered = render_template("filter.html")
        expected = inspect.cleandoc(
            """
            <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
            <html><head><title>Flask-Genshi - Hi!</title></head></html>
            """
        )

        assert rendered == expected


def test_filters_per_render(app):
    """Filters can be applied per rendering"""
    with app.test_request_context():

        def prepend_title(template):
            return template | Transformer("head/title").append(" - Flask-Genshi")

        rendered = render_template("filter.html", filter=prepend_title)
        expected = inspect.cleandoc(
            """
            <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
            <html><head><title>Hi! - Flask-Genshi</title></head></html>
            """
        )

        assert rendered == expected


def test_works_with_flatland(app):
    """Filters can take the context and support flatland"""
    with app.test_request_context():

        genshi = app.extensions["genshi"]

        @genshi.template_parsed
        def callback(template):
            flatland_setup(template)

        context = dict(form=FlatlandForm({"username": "dag"}))
        rendered = render_template("flatland.html", context)
        expected = inspect.cleandoc(
            """
            <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
            <input type="text" name="username" value="dag">
            """
        )

        assert rendered == expected
