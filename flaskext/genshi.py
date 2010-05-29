# -*- coding: utf-8 -*-
"""
    flaskext.genshi
    ~~~~~~~~~~~~~~~

    An extension to Flask for easy Genshi templating.

    :copyright: (c) 2010 by Dag Odenhall <dag.odenhall@gmail.com>.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

from copy import deepcopy

from flask import Config, current_app
from genshi.template import TemplateLoader, loader


GENSHI_LOADER = {'auto_reload': True}

GENSHI_TEMPLATES_PATH = 'templates'

GENSHI_RENDER_ARGS = {
    'method': 'html',
    'doctype': 'html',
    'encoding': 'UTF-8'
}

GENSHI_DEFAULT_TYPE='html'

GENSHI_TYPES= {
    'html': {
        'method': 'html',
        'doctype': 'html',
        'mimetype': 'text/html'},
    'html5': {
        'method': 'html',
        'doctype': 'html5',
        'mimetype':
        'text/html'},
    'xhtml': {
        'method': 'xhtml',
        'doctype': 'xhtml',
        'mimetype': 'application/xhtml+xml'},
    'xml': {
        'method': 'xml',
        'mimetype': 'application/xml'},
    'text': {
        'method': 'text',
        'mimetype': 'text/plain'}
}


def init_genshi(app):
    """Configure a Flask application for Genshi."""
    cfg = Config(app.root_path, app.default_config)
    cfg.from_object(__name__)
    for key, value in cfg.iteritems():
        app.config.setdefault(key, deepcopy(value))
    return app


def render_template(template, context=None, **render_args):
    """Render a Genshi template under ``GENSHI_TEMPLATES_PATH``.

    ``render_args`` are passed to the template's :meth:`render` method
    and can include the following:

    ============ ===========================================================
    ``method``   How the template stream is seralized. This controls things
                 such as end tags. Valid values are ``'xml'``, ``'xhtml'``,
                 ``'html'`` and ``'text'``.
    ``doctype``  Valid values are ``'html'``,  ``'html-transitional'``,
                 ``'xhtml'``, ``'xhtml-transitional'`` and ``'html5'``.
    ``encoding`` The output encoding.
    ============ ===========================================================
    """
    if not hasattr(current_app, 'genshi_loader'):
        path = loader.package(current_app.import_name,
                              current_app.config['GENSHI_TEMPLATES_PATH'])
        current_app.genshi_loader = \
            TemplateLoader(path, **current_app.config['GENSHI_LOADER'])

    if context is None:
        context = {}

    for key, value in current_app.jinja_env.globals.iteritems():
        context.setdefault(key, value)
    context.setdefault('filters', current_app.jinja_env.filters)
    context.setdefault('tests', current_app.jinja_env.tests)

    if not render_args:
        render_args = current_app.config['GENSHI_RENDER_ARGS']

    template = current_app.genshi_loader.load(template)
    return template.generate(**context).render(**render_args)


def render_response(template, context=None, type=None):
    """Render to a :class:`~flask.Response` with correct mimetype.
    
    ``type`` is a key in ``GENSHI_TYPES``.
    """
    config = current_app.config
    if type is None:
        type = config['GENSHI_TYPES'][config['GENSHI_DEFAULT_TYPE']]
    else:
        type = config['GENSHI_TYPES'][type]

    render_args = dict(method=type['method'])
    if 'doctype' in type:
        render_args['doctype'] = type['doctype']

    body = render_template(template, context, **render_args)
    return current_app.response_class(body, mimetype=type['mimetype'])

