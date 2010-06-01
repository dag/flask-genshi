Flask-Genshi
============

.. module:: flaskext.genshi

Flask-Genshi is an extension to `Flask`_ that allows you to easily
use `Genshi`_ for templating. It knows how to render a template based on the
file extension and can create :class:`~flask.Response` objects with mimetype
set accordingly.

Source code and issue tracking at `Bitbucket`_.


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

    from flaskext.genshi import Genshi
    
    app = Flask(__name__)
    genshi = Genshi(app)

The best way to render templates is to use :func:`render_response`.
This ensures that the proper mimetype is sent if you render XHTML, XML or text,
and sets the right doctype for you.

Use it like so::

    from flaskext.genshi import render_response
    
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

The extensions `html`, `xml`, `txt`, `js` and `css` are recognized,
but you can add any extension and method you like. Note that `txt`, `js`
and `css` templates are rendered with :class:`genshi.template.NewTextTemplate`
which is not XML-based. Rendering javascript with templates gives you tools
like :func:`flask.url_for` and rendering CSS with templates gives you
dynamic stylesheets with things like variables.


API Reference
-------------

.. autoclass:: Genshi
    :members:

.. autofunction:: select_method

.. autofunction:: generate_template

.. autofunction:: render_template

.. autofunction:: render_response


.. _Flask: http://flask.pocoo.org/
.. _Genshi: http://genshi.edgewall.org/
.. _Bitbucket: http://bitbucket.org/dag/flask-genshi
