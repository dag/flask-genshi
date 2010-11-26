from __future__ import with_statement

from attest import Assert
from flaskext.genshi import render_response

from tests.utils import flask_tests


strings = flask_tests()


@strings.test
def renders_strings(context):
    """Strings can be rendered as templates directly"""

    rendered = Assert(render_response(string='The name is $name',
                                      context=context, method='text'))

    assert rendered.data == 'The name is Rudolf'


@strings.test
def fails_without_template_or_string(context):
    """A template or string must be provided to render"""

    with Assert.raises(RuntimeError):
        render_response(context=context, method='text')
