# -*- coding: utf-8 -*-
"""
    flaskext.genshi
    ~~~~~~~~~~~~~~~

    An extension to Flask for easy Genshi templating.

    :copyright: (c) 2010 by Dag Odenhall <dag.odenhall@gmail.com>.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

from os.path import splitext

from genshi.template import NewTextTemplate, loader, TemplateLoader
from werkzeug import cached_property
from flask import current_app


class Genshi(object):

    def __init__(self, app):

        app.genshi_instance = self

        self.app = app

        #: What method is used for an extension.
        self.extensions = {
            'html': 'html',
            'xml': 'xml',
            'txt': 'text'
        }

        #: Render methods.
        self.methods = {
            'html': {
                'serializer': 'html',
                'doctype': 'html',
            },
            'html5': {
                'serializer': 'html',
                'doctype': 'html5',
            },
            'xhtml': {
                'serializer': 'xhtml',
                'doctype': 'xhtml',
                'mimetype': 'application/xhtml+xml'
            },
            'xml': {
                'serializer': 'xml',
                'mimetype': 'application/xml'
            },
            'text': {
                'serializer': 'text',
                'mimetype': 'text/plain',
                'class': NewTextTemplate
            }
        }

    @cached_property
    def template_loader(self):
        """A :class:`genshi.template.TemplateLoader` that loads templates
        from the same place as Flask.

        """
        path = loader.package(self.app.import_name, 'templates')
        return TemplateLoader(path, auto_reload=self.app.debug)


def select_method(template, method=None):
    """Selects a method from :attr:`Genshi.methods`
    based on the file extension of ``template``
    and :attr:`Genshi.extensions`, or based on ``method``.

    """
    genshi = current_app.genshi_instance
    if method is None:
        ext = splitext(template)[1][1:]
        return genshi.methods[genshi.extensions[ext]]
    return genshi.methods[method]


def generate_template(template, context=None, method=None):
    """Creates a Genshi template stream that you can
    run filters and transformations on.

    """
    class_ = select_method(template, method).get('class')
    context = context or {}
    for key, value in current_app.jinja_env.globals.iteritems():
        context.setdefault(key, value)
    context.setdefault('filters', current_app.jinja_env.filters)
    context.setdefault('tests', current_app.jinja_env.tests)
    genshi = current_app.genshi_instance
    template = genshi.template_loader.load(template, cls=class_)
    return template.generate(**context)


def render_template(template, context=None, method=None):
    """Renders a template to a string."""
    template_name = template
    template = generate_template(template, context, method)
    method = select_method(template_name, method)
    render_args = dict(method=method['serializer'])
    if 'doctype' in method:
        render_args['doctype'] = method['doctype']
    return template.render(**render_args)


def render_response(template, context=None, method=None):
    """Renders a template and wraps it in a :attr:`~flask.Flask.response_class`
    with mimetype set according to the rendering method.

    """
    mimetype = select_method(template, method).get('mimetype', 'text/html')
    template = render_template(template, context, method)
    return current_app.response_class(template, mimetype=mimetype)

