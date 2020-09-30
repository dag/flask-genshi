# -*- coding: utf-8 -*-
"""
    flask_genshi
    ~~~~~~~~~~~~

    An extension to Flask for easy Genshi templating.

    :copyright: (c) 2010 by Dag Odenhall <dag.odenhall@gmail.com>.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

from collections import defaultdict
import os.path
from warnings import warn
try:
    # PY3
    from inspect import getfullargspec
except ImportError:
    # PY2
    from inspect import getargspec as getfullargspec  # getargspec is deprecated >=3.0

from genshi.template import (NewTextTemplate, MarkupTemplate,
                             loader, TemplateLoader)
from werkzeug.utils import cached_property
from flask import current_app

try:
    from flask import signals_available
except ImportError:
    signals_available = False
else:
    from flask.signals import Namespace
    signals = Namespace()
    template_generated = signals.signal('template-generated')


# there's more to Jinja context than just environment, but apparently
# the only thing jinja filters currently care about is this (and also
# whether autoescaping is on), hence these shims.
#
# NOTE: this does not take custom jinja filters into account, although I
# don't expect Genshi-minded users of @jinja2.contextfilter any time
# soon.
# Taken from https://github.com/vthriller/flask-genshi
class FakeJinjaContext:
    def __init__(self, env):
        self.environment = env


class FakeJinjaEvalContext:
    def __init__(self, env):
        self.environment = env
        # Flask set this one explicitly
        self.autoescape = env.autoescape


class Genshi(object):
    """Initialize extension.

    ::

        app = Flask(__name__)
        genshi = Genshi(app)

    .. versionchanged:: 0.4
        You can now initialize your application later with :meth:`init_app`.

    .. deprecated:: 0.4
        ``app.genshi_instance`` in favor of ``app.extensions['genshi']``.

    """

    def __init__(self, app=None):

        if app is not None:
            self.init_app(app)

        #: A callable for Genshi's callback interface, called when a template
        #: is loaded, with the template as the only argument.
        #:
        #: :meth:`template_parsed` is a decorator for setting this.
        #:
        #: .. versionadded:: 0.5
        self.callback = None

        #: What method is used for an extension.
        self.extensions = {
            'html': 'html',
            'xml': 'xml',
            'txt': 'text',
            'js': 'js',
            'css': 'css',
            'svg': 'svg'
        }

        #: Render methods.
        #:
        #: .. versionchanged:: 0.3 Support for Javascript and CSS.
        #: .. versionchanged:: 0.4 Support for SVG.
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
            },
            'svg': {
                'serializer': 'xml',
                'doctype': 'svg',
                'mimetype': 'image/svg+xml'
            }
        }

        #: Filter functions to be applied to templates.
        #:
        #: .. versionadded:: 0.3
        self.filters = defaultdict(list)

    def init_app(self, app):
        """Initialize a :class:`~flask.Flask` application
        for use with this extension. Useful for the factory pattern but
        not needed if you passed your application to the :class:`Genshi`
        constructor.

        ::

            genshi = Genshi()

            app = Flask(__name__)
            genshi.init_app(app)

        .. versionadded:: 0.4

        """
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['genshi'] = self
        app.genshi_instance = self
        self.app = app

    def template_parsed(self, callback):
        """Set up a calback to be called with a template when it is first
        loaded and parsed. This is the correct way to set up the
        :class:`~genshi.filters.Translator` filter.

        .. versionadded:: 0.5

        """
        self.callback = callback
        return callback

    @cached_property
    def template_loader(self):
        """A :class:`genshi.template.TemplateLoader` that loads templates
        from the same places as Flask.

        .. versionchanged:: 0.6
            Removed support for flask modules and enabled support for blueprints
        """
        path = loader.directory(
            os.path.join(self.app.root_path, self.app.template_folder or 'templates')
        )
        blueprint_paths = {}
        blueprints = getattr(self.app, 'blueprints', {})
        for name, blueprint in blueprints.items():
            blueprint_path = os.path.join(
                blueprint.root_path, blueprint.template_folder or 'templates'
            )
            if os.path.isdir(blueprint_path):
                blueprint_paths[name] = loader.directory(blueprint_path)
        return TemplateLoader([path, loader.prefixed(**blueprint_paths)],
                              auto_reload=self.app.debug,
                              callback=self.callback)

    def filter(self, *methods):
        """Decorator that adds a function to apply filters
        to templates by rendering method.

        .. versionadded:: 0.3

        .. versionchanged:: 0.5
            Filters can now optionally take a second argument for the context.

        """
        def decorator(function):
            for method in methods:
                self.filters[method].append(function)
            return function
        return decorator

    def _method_for(self, template, method=None):
        """Selects a method from :attr:`Genshi.methods`
        based on the file extension of ``template``
        and :attr:`Genshi.extensions`, or based on ``method``.

        """
        if method is None:
            ext = os.path.splitext(template)[1][1:]
            return self.extensions[ext]
        return method


def select_method(template, method=None):
    """Same as :meth:`Genshi._method_for`.

    .. deprecated:: 0.4

    """
    warn('select_method to be dropped in future releases',
         DeprecationWarning, stacklevel=2)
    return current_app.extensions['genshi']._method_for(template, method)


def generate_template(template=None, context=None,
                      method=None, string=None, filter=None):
    """Creates a Genshi template stream that you can
    run filters and transformations on.

    """
    genshi = current_app.extensions['genshi']
    method = genshi._method_for(template, method)
    class_ = genshi.methods[method].get('class', MarkupTemplate)

    filters = current_app.jinja_env.filters.copy()
    for name, f in filters.items():
        if getattr(f, "environmentfilter", False):
            filters[name] = (
                lambda f: lambda *args, **kw: f(current_app.jinja_env, *args, **kw)
            )(f)
        elif getattr(f, "contextfilter", False):
            filters[name] = (
                lambda f: lambda *args, **kw: f(
                    FakeJinjaContext(current_app.jinja_env), *args, **kw
                )
            )(f)
        elif getattr(f, "evalcontextfilter", False):
            filters[name] = (
                lambda f: lambda *args, **kw: f(
                    FakeJinjaEvalContext(current_app.jinja_env), *args, **kw
                )
            )(f)

    context = context or {}
    for key, value in current_app.jinja_env.globals.items():
        context.setdefault(key, value)
    context.setdefault('filters', filters)
    context.setdefault('tests', current_app.jinja_env.tests)
    current_app.update_template_context(context)

    if template is not None:
        template = genshi.template_loader.load(template, cls=class_)
    elif string is not None:
        template = class_(string)
    else:
        raise RuntimeError('Need a template or string')

    stream = template.generate(**context)

    if signals_available:
        template_generated.send(current_app._get_current_object(),
                                template=template, context=context)

    for func in genshi.filters[method]:
        if len(getfullargspec(func)[0]) == 2:  # Filter takes context?
            stream = func(stream, context)
        else:
            stream = func(stream)

    if filter:
        if len(getfullargspec(filter)[0]) == 2:  # Filter takes context?
            stream = filter(stream, context)
        else:
            stream = filter(stream)

    return stream


def render_template(template=None, context=None,
                    method=None, string=None, filter=None):
    """Renders a template to a string."""
    genshi = current_app.extensions['genshi']
    method = genshi._method_for(template, method)
    template = generate_template(template, context, method, string, filter)
    render_args = dict(method=genshi.methods[method]['serializer'])
    if 'doctype' in genshi.methods[method]:
        render_args['doctype'] = genshi.methods[method]['doctype']
    return template.render(**render_args)


def render_response(template=None, context=None,
                    method=None, string=None, filter=None):
    """Renders a template and wraps it in a :attr:`~flask.Flask.response_class`
    with mimetype set according to the rendering method.

    """
    genshi = current_app.extensions['genshi']
    method = genshi._method_for(template, method)
    mimetype = genshi.methods[method].get('mimetype', 'text/html')
    template = render_template(template, context, method, string, filter)
    return current_app.response_class(template, mimetype=mimetype)


def render(template, **context):
    """Render a template to a response object, passing the context as
    keyword arguments. Shorthand for
    ``render_response(template, dict(**context))``.

    .. versionadded:: 0.6

    """
    return render_response(template, context)
