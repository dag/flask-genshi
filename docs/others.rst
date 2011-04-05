Use with Other Extensions and Packages
======================================

.. currentmodule:: flaskext.genshi


Form Processing with flatland
-----------------------------

First, set up flatland with the callback interface::

    from flatland.out.genshi import setup

    @genshi.template_parsed
    def callback(template):
        setup(template)

Don't forget the form namespace:

.. code-block:: html+genshi

    <html xmlns:form="http://ns.discorporate.us/flatland/genshi">
      <input type="text" form:bind="form.username"/>
    </html>

.. versionadded:: 0.5


Internationalization with Flask-Babel
-------------------------------------

You can use Flask-Genshi with `Flask-Babel`_ for internationalization.
First, set up the :class:`~genshi.filters.Translator` filter with
the callback interface via :meth:`~Genshi.template_parsed`. The filter
wants a message catalogue and to get the right one for every request you
can use Werkzeug's :class:`~werkzeug.LocalProxy`::

    from werkzeug import LocalProxy
    from genshi.filters import Translator
    from flaskext.babel import get_translations

    current_translations = LocalProxy(get_translations)

    @genshi.template_parsed
    def callback(template):
        Translator(current_translations).setup(template)

You'll want a ``babel.cfg`` similar to this one:

.. code-block:: ini

    [python: **.py]
    [genshi:**/templates/**.html]
    [genshi:**/templates/**.txt]
    template_class = genshi.template.NewTextTemplate

Consult the Genshi documentation on `Internationalization and Localization`_
for details on extracting translation strings from Genshi templates. Beware
of a documentation bug though, the XML namespace should *not* end in a
slash. Here's a working template example:

.. code-block:: html+genshi

    <html xmlns:i18n="http://genshi.edgewall.org/i18n">
      <head>
        <title i18n:msg="subtitle">Legendary Site - $title</title>
      </head>
    </html>

The above will result in the string ``Legendary Site - %(subtitle)s`` in
your message catalogue.


.. versionadded:: 0.5


.. _Flask-Babel: http://packages.python.org/Flask-Babel/
.. _Internationalization and Localization:
    http://genshi.edgewall.org/wiki/Documentation/0.6.x/i18n.html
