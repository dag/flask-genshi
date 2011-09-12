from __future__ import absolute_import

import fnmatch
import functools
import mimetypes
import os.path

from flask import current_app
from flask.signals import Namespace
from werkzeug.local import LocalProxy
from werkzeug.utils import cached_property

from genshi.output import (DocType, XMLSerializer, XHTMLSerializer,
                           HTMLSerializer, TextSerializer, encode)
from genshi.template import (TemplateLoader, Context, MarkupTemplate,
                             NewTextTemplate as TextTemplate)


_signals = Namespace()
_current = LocalProxy(lambda: current_app.extensions['genshi'])


template_parsed = _signals.signal('template-parsed')
template_loaded = _signals.signal('template-loaded')
stream_generated = _signals.signal('stream-generated')


def render(template_name, **context):
    """Render a template to a response object."""
    return _current.genshi[template_name](**context)


def render_template(template_name, **context):
    """Render a template to a unicode string."""
    return _current.genshi[template_name].render(**context)


class Genshi(object):
    """Extension object.  Holds configuration for the Flask-Genshi
    extension."""

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Configure a Flask application for using this extension."""
        app.extensions['genshi'] = _GenshiState(self, app)

    def filter(self, *mimetypes):
        """Register a filter function on the content types configured for
        each of the *mimetypes*."""
        def decorator(func):
            for type in mimetypes:
                content_type = self.content_types[type]
                content_type.add_filter(func)
            return func
        return decorator

    def __getitem__(self, name):
        return Template(name)

    @cached_property
    def mime_db(self):
        """A `~mimetypes.MimeTypes` instance used to look up the
        `ContentType` configured for a template."""
        return mimetypes.MimeTypes()

    @cached_property
    def content_types(self):
        """Maps |MIME| types to `ContentType` instances."""
        return {
            '*/*':
                ContentType(),
            'text/html':
                ContentType(HTMLSerializer(DocType.HTML5)),
            'application/xhtml+xml':
                ContentType(XMLSerializer(DocType.XHTML11)),
            'text/*':
                ContentType(TextSerializer(), TextTemplate),
        }

    def get_content_type(self, filename):
        """Select the `ContentType` configured for the mimetype of
        *filename*."""
        mimetype = self.mime_db.guess_type(filename)[0]
        try:
            return self.content_types[mimetype]
        except KeyError:
            for key, value in self.content_types.iteritems():
                if key != '*/*' and fnmatch.fnmatch(mimetype, key):
                    return value
        return self.content_types['*/*']

    def create_context(self, base):
        """Create a `~genshi.template.base.Context` for rendering templates
        in, including at least the items in *base*."""
        env = current_app.jinja_env
        context = Context()
        context.push(dict((key, value)
            for key, value in env.globals.iteritems()
            if key not in __builtins__
            and not _is_jinja_specific(value)
        ))
        context.push(dict((key, Pipe(value))
            for key, value in env.filters.iteritems()
            if not _is_jinja_specific(value)
        ))
        context.push(dict(('is' + key, value)
            for key, value in env.tests.iteritems()
            if not _is_jinja_specific(value)
        ))
        context.push(base)
        return context

    def create_loader(self, app):
        """Create a template loader for Genshi based on the template
        folders configured for *app* and its blueprints."""
        folders = [os.path.join(app.root_path, app.template_folder)]
        for blueprint in app.blueprints.itervalues():
            if blueprint.template_folder is not None:
                folders.append(os.path.join(blueprint.root_path,
                                            blueprint.template_folder))
        return TemplateLoader(folders, auto_reload=app.debug,
                              callback=self.loader_callback)

    def loader_callback(self, template):
        """Called by template loaders when a template is parsed, but not
        when it is returned from the cache."""
        template_parsed.send(self, template=template)


class ContentType(object):
    """Configuration for how Genshi should parse and render a template."""

    def __init__(self, serializer=XMLSerializer(),
                 template_class=MarkupTemplate):
        self.serializer = serializer
        self.template_class = template_class
        self.filters = []

    def add_filter(self, func):
        """Register *func* as a stream filter that will be applied when
        rendering templates of this content type."""
        self.filters.append(func)

    def load(self, name, loader):
        """Load the template named *name* from the *loader*."""
        template = loader.load(name, cls=self.template_class)
        template_loaded.send(self, template=template)
        return template

    def generate(self, template, context, filters):
        """Generate a stream from the *template* rendered in the *context*
        with the additional *filters* applied."""
        filters = filters + self.filters
        stream = template.generate(context)
        stream = reduce(lambda s, f: f(s), [stream] + filters)
        stream_generated.send(self, stream=stream,
                              context=context, filters=filters)
        return stream

    def render(self, stream):
        """Render a *stream* to a unicode string."""
        return encode(self.serializer(stream), encoding=None)


class Template(object):

    def __init__(self, name, filters=None):
        self.name = name
        self.filters = [] if filters is None else filters

    def __or__(self, other):
        return type(self)(self.name, self.filters + [other])

    @property
    def content_type(self):
        return _current.genshi.get_content_type(self.name)

    @property
    def template(self):
        return self.content_type.load(self.name, _current.loader)

    def render(self, **context):
        current_app.update_template_context(context)
        newctx = _current.genshi.create_context(context)
        content_type = self.content_type
        stream = content_type.generate(self.template, newctx, self.filters)
        return content_type.render(stream)

    def __call__(self, **context):
        rendering = self.render(**context)
        mimetype = _current.genshi.mime_db.guess_type(self.name)[0]
        return current_app.response_class(rendering, mimetype=mimetype)


class Pipe(object):

    def __init__(self, func, *args, **kwargs):
        functools.update_wrapper(self, func)
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return type(self)(self.func, *args, **kwargs)

    def __ror__(self, other):
        return self.func(other, *self.args, **self.kwargs)


class _GenshiState(object):

    def __init__(self, genshi, app):
        self.genshi = genshi
        self.app = app

    @cached_property
    def loader(self):
        return self.genshi.create_loader(self.app)


def _is_jinja_specific(filter):
    return any(getattr(filter, attr, False)
               for attr in ['contextfilter',
                            'evalcontextfilter',
                            'environmentfilter',
                            'contextfunction',
                            'evalcontextfunction',
                            'environmentfunction'])
