
from __future__ import absolute_import

from nose.tools import raises
from flaskext.genshi import render_response
from flask import g

from .utils import test


@test
def renders_strings():
    """Strings can be rendered as templates directly"""

    rendered = render_response(string='The name is $name',
                               context=g.context, method='text')

    assert rendered.data == 'The name is Rudolf'


@test
@raises(RuntimeError)
def fails_without_template_or_string():
    """A template or string must be provided to render"""

    render_response(context=g.context, method='text')
