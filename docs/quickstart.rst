Quickstart
==========

.. currentmodule:: flask_genshi


Installation
------------

Just grab it from PyPI with `easy_install` or `pip`, for example::

    $ easy_install Flask-Genshi

If you're starting a new project you don't need to explicitly
install Flask as Flask-Genshi depends on it already.


How to Use
----------

You need to construct a :class:`Genshi` with your
:class:`~flask.Flask` instance.

::

    from flask_genshi import Genshi

    app = Flask(__name__)
    genshi = Genshi(app)

The best way to render templates is to use :func:`render_response`.
This ensures that the proper mimetype is sent if you render XHTML, XML or text,
and sets the right doctype for you.

Use it like so::

    from flask_genshi import render_response

    @app.route('/')
    def index():
        title = 'Genshi + Flask, a match made in heaven!'
        return render_response('index.html', dict(title=title))


Using Methods
-------------

Methods control things such as the doctype and how end tags are rendered,
and with :func:`render_response` also the mimetype.
Unless overridden the method used is decided
by the template's filename extension.

By default HTML renders as strict HTML 4.01. This is how you
change it to HTML5::

    genshi.extensions['html'] = 'html5'

`I recommend against this
<http://webkit.org/blog/68/understanding-html-xml-and-xhtml/>`_
but of course you can also change it to XHTML::

    genshi.extensions['html'] = 'xhtml'

You can also override the default with a parameter
to the templating functions::

    render_response('video.html', method='html5')

You can add and edit any methods and extensions you like,
here are the defaults:

=========== ========= ================= ==================================
Method      Extension Template Language Output
=========== ========= ================= ==================================
``'html'``  `.html`   `XML based`_      HTML 4.01 Strict
``'html5'``           `XML based`_      HTML 5
``'xhtml'``           `XML based`_      XHTML 1.0 Strict
``'xml'``   `.xml`    `XML based`_      :mimetype:`application/xml`
``'svg'``   `.svg`    `XML based`_      SVG 1.1
``'text'``  `.txt`    `Text based`_     :mimetype:`text/plain`
``'js'``    `.js`     `Text based`_     :mimetype:`application/javascript`
``'css'``   `.css`    `Text based`_     :mimetype:`text/css`
=========== ========= ================= ==================================

.. _XML based: http://genshi.edgewall.org/wiki/Documentation/0.6.x/xml-templates.html
.. _Text based: http://genshi.edgewall.org/wiki/Documentation/0.6.x/text-templates.html


Filtering template streams
--------------------------

You can apply filters to templates that you render globally per rendering
method::

    from genshi.filters import Transformer

    @genshi.filter('html')
    def prepend_title(template):
        return template | Transformer('head/title').prepend('MySite - ')

Alternatively, since version 0.5, you can apply a filter for a template as
you render it, more repetitive but with more control::

    render_response('index.html', filter=prepend_title)

See the `Genshi documentation
<http://genshi.edgewall.org/wiki/Documentation/0.6.x/filters.html>`_
for more filters you can use.

.. versionadded:: 0.3

.. versionchanged:: 0.5 Filters can now optionally take a second argument for the context.

.. versionchanged:: 0.5 You can now apply filters on a per-render basis.
