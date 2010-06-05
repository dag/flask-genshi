# -*- coding: utf-8 -*-
"""
    flaskext.genshi
    ~~~~~~~~~~~~~~~

    An extension to Flask for easy Genshi templating.

    :copyright: (c) 2010 by Dag Odenhall <dag.odenhall@gmail.com>.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

from functools import wraps
from collections import defaultdict
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
            'txt': 'text',
            'js': 'js',
            'css': 'css'
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
            },
            'js': {
                'serializer': 'text',
                'mimetype': 'application/javascript',
                'class': NewTextTemplate
            },
            'css': {
                'serializer': 'text',
                'mimetype': 'text/css',
                'class': NewTextTemplate
            }
        }

        #: Filter functions to be applied to templates.
        #:
        #: .. versionadded:: 0.3
        self.filters = defaultdict(list)

    @cached_property
    def template_loader(self):
        """A :class:`genshi.template.TemplateLoader` that loads templates
        from the same place as Flask.

        """
        path = loader.package(self.app.import_name, 'templates')
        return TemplateLoader(path, auto_reload=self.app.debug)

    def filter(self, *methods):
        """Decorator that adds a function to apply filters
        to templates by rendering method.

        Example::

            from genshi.filters import Transformer

            @genshi.filter('html')
            def prepend_title(template):
                return template | Transformer('head/title').prepend('MySite - ')

        See the `Genshi documentation
        <http://genshi.edgewall.org/wiki/Documentation/0.6.x/filters.html>`_
        for more filters you can use.

        .. versionadded:: 0.3

        """
        def decorator(function):
            for method in methods:
                self.filters[method].append(function)
            return function
        return decorator


def select_method(template, method=None):
    """Selects a method from :attr:`Genshi.methods`
    based on the file extension of ``template``
    and :attr:`Genshi.extensions`, or based on ``method``.

    """
    if method is None:
        genshi = current_app.genshi_instance
        ext = splitext(template)[1][1:]
        return genshi.extensions[ext]
    return method


def generate_template(template, context=None, method=None):
    """Creates a Genshi template stream that you can
    run filters and transformations on.

    """
    method = select_method(template, method)
    genshi = current_app.genshi_instance
    class_ = genshi.methods[method].get('class')
    context = context or {}
    for key, value in current_app.jinja_env.globals.iteritems():
        context.setdefault(key, value)
    context.setdefault('filters', current_app.jinja_env.filters)
    context.setdefault('tests', current_app.jinja_env.tests)
    template = genshi.template_loader.load(template, cls=class_)
    template = template.generate(**context)
    for filter in genshi.filters[method]:
        template = filter(template)
    return template


def render_template(template, context=None, method=None):
    """Renders a template to a string."""
    method = select_method(template, method)
    template = generate_template(template, context, method)
    genshi = current_app.genshi_instance
    render_args = dict(method=genshi.methods[method]['serializer'])
    if 'doctype' in genshi.methods[method]:
        render_args['doctype'] = genshi.methods[method]['doctype']
    return template.render(**render_args)


def render_response(template, context=None, method=None):
    """Renders a template and wraps it in a :attr:`~flask.Flask.response_class`
    with mimetype set according to the rendering method.

    """
    method = select_method(template, method)
    genshi = current_app.genshi_instance
    mimetype = genshi.methods[method].get('mimetype', 'text/html')
    template = render_template(template, context, method)
    return current_app.response_class(template, mimetype=mimetype)

