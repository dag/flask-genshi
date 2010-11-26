from __future__ import with_statement

from attest import Assert
from flaskext.genshi import render_template

from tests.utils import flask_tests


modules = flask_tests()


@modules.test
def loads_module_templates(context):
    """Templates can be loaded from module packages"""

    rendered = Assert(render_template('package_mod/module-template.txt',
                                      context))

    assert rendered == 'Hello modular Rudolf\n'


@modules.test
def overrides_module_templates(context):
    """Module templates can be overridden with application templates"""

    rendered = Assert(render_template('package_mod/nonmodule-template.txt',
                                      context))

    assert rendered == 'Hello nonmodular Rudolf\n'
