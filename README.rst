Flask-Genshi
------------

`Flask-Genshi`_ is an extension to `Flask`_ that allows you to easily
use `Genshi`_ for templating. Easily switch between HTML5 and XHTML
and have the mimetype set automatically for you.

::

    from flask import Flask
    from flaskext.genshi import Genshi, render_response

    app = Flask(__name__)
    genshi = Genshi(app)

    @app.route('/')
    def index():
        title = 'Genshi + Flask, a match made in heaven!'
        return render_response('index.html', dict(title=title))

You can install the `development version`_ from `GitHub`_
with ``easy_install Flask-Genshi==dev`` but you probably want the
latest stable release::

    sudo easy_install Flask-Genshi

.. _Flask-Genshi: http://packages.python.org/Flask-Genshi/
.. _Flask: http://flask.pocoo.org/
.. _Genshi: http://genshi.edgewall.org/
.. _development version: http://github.com/dag/flask-genshi/zipball/master#egg=Flask-Genshi-dev
.. _GitHub: http://github.com/dag/flask-genshi
