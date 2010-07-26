"""
Flask-Genshi
------------

`Flask-Genshi`_ is an extension to `Flask`_ that allows you to easily
use `Genshi`_ for templating. Easily switch between HTML5 and XHTML
and have the mimetype set automatically for you.

::

    from flaskext.genshi import Genshi, render_response
    
    app = Flask(__name__)
    genshi = Genshi(app)

    @app.route('/')
    def index():
        title = 'Genshi + Flask, a match made in heaven!'
        return render_response('index.html', dict(title=title))

You can install the `development version`_ from `Bitbucket`_
with ``easy_install Flask-Genshi==dev`` but you probably want the
latest stable release::

    sudo easy_install Flask-Genshi

.. _Flask-Genshi: http://packages.python.org/Flask-Genshi/
.. _Flask: http://flask.pocoo.org/
.. _Genshi: http://genshi.edgewall.org/
.. _development version: http://bitbucket.org/dag/flask-genshi/get/tip.gz#egg=Flask-Genshi-dev
.. _Bitbucket: http://bitbucket.org/dag/flask-genshi
"""
from setuptools import setup


setup(
    name='Flask-Genshi',
    version='0.3.1',
    url='http://packages.python.org/Flask-Genshi',
    license='BSD',
    author='Dag Odenhall',
    author_email='dag.odenhall@gmail.com',
    description='An extension to Flask for easy Genshi templating.',
    long_description=__doc__,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires=[
        'Flask',
        'Genshi'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML'
    ]
)
