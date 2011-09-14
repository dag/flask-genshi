API Reference
=============

Primary User API
----------------

.. autofunction:: render

  The rendered result is encoded according to the default charset of the
  `~flask.Flask.response_class` and the |MIME| type of the response is set
  to that of the rendered template.

  This function requires a Flask request context belonging to an
  application configured with a `Genshi` instance.


.. autofunction:: render_template

  Like `render` but returns an unencoded unicode string.  Primarily useful
  for purposes other than rendering responses to |HTTP| requests, such as
  e-mail templating.  Similar to the function of the same name in Flask.


.. autoclass:: Genshi

  ::

    app = Flask(__name__)
    genshi = Genshi(app)

  You can subscript the instance to get a `Template` by name, allowing you
  to apply stream filters with more control.

  ::

    template = genshi['index.html'] \
             | Transformer('//title').replace('Fabulous Ltd.')

  :param app: Short for calling `init_app`.

  .. automethod:: init_app

  .. decoratormethod:: filter(\*mimetypes)

    Register a filter function on the content types configured for
    each of the *mimetypes*.

    ::

      @genshi.filter('text/html')
      def hijack_title(stream):
          return stream | Transformer('//title').replace('Fabulous Ltd.')

  .. autoattribute:: mime_db

  .. autoattribute:: content_types

  .. automethod:: get_content_type

  .. automethod:: create_context

  .. automethod:: create_loader

  .. automethod:: loader_callback

    The default emits the `template_parsed` signal.


Additional Utilities
--------------------

.. autoclass:: ContentType(serializer=XMLSerializer(), template_class=MarkupTemplate)
  :members:


.. autoclass:: Template

  The bitwise *or* operator can be used to create new instances with
  additional filters.  These do the same::

    Template('index.html') | Transformer('//title').replace('Fabulous Ltd.')
    Template('index.html', [Transformer('//title').replace('Fabulous Ltd.')])

  The *mimetype* parameter can be used to override which `ContentType` to
  render with.  For example to render an XHTML template as HTML 5::

    return Template('index.xhtml', mimetype='text/html').render_to_response()

  :param name: Filename of the template.
  :param filters: List of functions to filter the stream with.
  :param mimetype: Used to select the `ContentType` and set on rendered
    response objects.  Guessed from the *name* parameter if set to None.

  .. automethod:: render

  .. automethod:: render_to_response

    The call interface of this class is an alias of this method.


.. autoclass:: Pipe

  Calling the pipe object as a callable yields a new `Pipe` with fixed
  arguments.

  This class can be used to mimic Jinja's "filters":

  >>> length = Pipe(len)
  >>> take = Pipe(lambda x, n: x[:n])
  >>> [1, 2, 3] | length
  3
  >>> range(10) | take(5)
  [0, 1, 2, 3, 4]


Signals
-------

.. data:: template_parsed(template)


.. data:: template_loaded(template)


.. data:: stream_generated(stream, context, filters)
