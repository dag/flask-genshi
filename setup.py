"""
Flask-Genshi
------------

An extension to Flask for easy Genshi templating.

Links
`````

* `documentation <http://packages.python.org/Flask-Genshi>`_
* `development version
  <http://bitbucket.org/dag/flask-genshi/get/tip.gz#egg=Flask-Genshi-dev>`_


"""
from setuptools import setup


setup(
    name='Flask-Genshi',
    version='0.3',
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
