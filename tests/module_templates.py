
from __future__ import absolute_import

from flaskext.genshi import render_template
from flask import g

from .utils import test


@test
def loads_module_templates():
    """Templates can be loaded from module packages"""

    rendered = render_template('package_mod/module-template.txt', g.context)

    assert rendered == 'Hello modular Rudolf\n'


@test
def overrides_module_templates():
    """Module templates can be overridden with application templates"""

    rendered = render_template('package_mod/nonmodule-template.txt', g.context)

    assert rendered == 'Hello nonmodular Rudolf\n'
