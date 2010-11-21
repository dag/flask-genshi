#!/usr/bin/env python
from __future__ import with_statement
from setuptools import setup


with open('README.rst') as file:
    readme = file.read()


setup(
    name='Flask-Genshi',
    version='0.5',
    url='http://packages.python.org/Flask-Genshi',
    license='BSD',
    author='Dag Odenhall',
    author_email='dag.odenhall@gmail.com',
    description='An extension to Flask for easy Genshi templating.',
    long_description=readme,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    test_suite='nose.collector',
    tests_require=['nose', 'flatland', 'blinker'],
    install_requires=[
        'Flask',
        'Genshi>=0.5'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML'
    ]
)
