Flask-Genshi
============

.. module:: flaskext.genshi

Flask-Genshi is an extension to `Flask`_ that allows you to easily
use `Genshi`_ for templating. It uses Flask's :class:`~flask.Config` and can
create :class:`~flask.Response` objects with mimetype
set based on how you render templates.

Source code and issue tracking at `Bitbucket`_.


Installation
------------

Just grab it from PyPI with `easy_install` or `pip`, for example::

    $ easy_install Flask-Genshi

If you're starting a new project you don't need to explicitly
install Flask as Flask-Genshi depends on it already.


How to Use
----------

You need to run :func:`init_genshi` on your :class:`~flask.Flask` instance.

::

    from flaskext.genshi import init_genshi
    
    app = Flask(__name__)
    init_genshi(app)

The best way to render templates is to use :func:`render_response`.
This ensures that the proper mimetype is sent if you render XHTML or text,
and sets the right doctype for you.

Use it like so::

    from flaskext.genshi import render_response
    
    @app.route('/')
    def index():
        title = 'Genshi + Flask, a match made in heaven!'
        return render_response('index.html', locals())

You should disable template autoreloading in production::

    DEBUG = False
    GENSHI_LOADER = dict(auto_reload=DEBUG)


Configuration Values
--------------------

========================== =================================================
``GENSHI_LOADER``          Arguments to the template loader.
                           Defaults to ``{'auto_reload': True}``.
``GENSHI_TEMPLATES_PATH``  Path under ``app.root_path`` to templates.
                           Defaults to ``templates``.
``GENSHI_DEFAULT_DOCTYPE`` For :func:`render_template`. One of ``html``, 
                           ``html-transitional``, ``xhtml``,
                           ``xhtml-transitional`` and ``html5``.
                           Defaults to ``html``.
``GENSHI_DEFAULT_METHOD``  For :func:`render_template`. One of ``xml``,
                           ``xhtml``, ``html`` and ``text``.
                           Defaults to ``html``.
``GENSHI_DEFAULT_TYPE``    For :func:`render_response`. One of ``xml``,
                           ``xhtml``, ``html`` ``html5`` and ``text``.
                           Defaults to ``html``.
``GENSHI_TYPES``           Maps types for :func:`render_response`
                           to their mimetype, method and doctype.
========================== =================================================


API Reference
-------------

.. autofunction:: init_genshi

.. autofunction:: render_template

.. autofunction:: render_response


.. _Flask: http://flask.pocoo.org/
.. _Genshi: http://genshi.edgewall.org/
.. _Bitbucket: http://bitbucket.org/dag/flask-genshi
