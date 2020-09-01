import inspect

from flask_genshi import render_response


def test_updates_context(app):
    """Render calls update the template context with context processors"""
    with app.test_request_context():

        @app.context_processor
        def inject_rudolf():
            return dict(rudolf="The red-nosed reindeer")

        rendered = render_response("context.html")

        expected_data = inspect.cleandoc(
            """
            <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
            <pre>rudolf = The red-nosed reindeer</pre>
            """
        )

        assert rendered.mimetype == "text/html"
        assert rendered.data == expected_data
