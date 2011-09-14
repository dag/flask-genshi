# encoding=utf-8
from unittest import TestCase
from flaskext.genshi import render, render_template
from genshi.filters import Transformer
from testapp import app, genshi


HTML_OUTPUT = u"""\
<!DOCTYPE html>
<html>
  <body>
    <p>¡HOLA, WORLD!</p>
    <p>WELCOME TO LOCALHOST.</p>
    <p>LOREM ...</p>
    <hr>
  </body>
</html>"""


XHTML_OUTPUT = u"""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\
 "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html>
  <body>
    <p>Hello, World!</p>
    <p>Welcome to localhost.</p>
    <hr/>
  </body>
</html>"""


XML_OUTPUT = u"""\
<html>
  <body>
    <p>Hello, World!</p>
    <p>Welcome to localhost.</p>
    <hr/>
  </body>
</html>"""


FILTERED_XML_OUTPUT = u"""\
<html>
  <body>
    <hr/>
  </body>
</html>"""


TXT_OUTPUT = u"""\
Hello, World!
Welcome to localhost.
"""


class FlaskTestCase(TestCase):

    def setUp(self):
        self.ctx = app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()


class TestRendering(FlaskTestCase):

    def test_render_html(self):
        response = render('test.html', name='World')
        assert response.mimetype == 'text/html'
        assert response.data == HTML_OUTPUT.encode('utf-8')
        assert render_template('test.html', name='World') == HTML_OUTPUT

    def test_render_xhtml(self):
        response = render('test.xhtml', name='World')
        assert response.mimetype == 'application/xhtml+xml'
        assert response.data == XHTML_OUTPUT.encode('utf-8')
        assert render_template('test.xhtml', name='World') == XHTML_OUTPUT

    def test_render_xml(self):
        response = render('test.xml', name='World')
        assert response.mimetype == 'application/xml'
        assert response.data == XML_OUTPUT.encode('utf-8')
        assert render_template('test.xml', name='World') == XML_OUTPUT

    def test_render_txt(self):
        response = render('test.txt', name='World')
        assert response.mimetype == 'text/plain'
        assert response.data == TXT_OUTPUT.encode('utf-8')
        assert render_template('test.txt', name='World') == TXT_OUTPUT


class TestBlueprints(FlaskTestCase):

    def test_blueprint_templates(self):
        assert render_template('blueprint.txt') == u'Hello from Blueprint!\n'


class TestFiltering(FlaskTestCase):

    def test_single_template_filter(self):
        template = genshi['test.xml'] | Transformer('//p').remove()
        assert template.render(name='World') == FILTERED_XML_OUTPUT
