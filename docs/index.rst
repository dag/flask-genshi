Flask-Genshi
============

.. module:: flaskext.genshi

Flask-Genshi is an extension to `Flask`_ that allows you to easily
use `Genshi`_ for templating.

Features:

* Integrates fully with Flask and works with Flask-Babel for
  internationalization and flatland for form processing (that is, the
  special support flatland has for Genshi). Other extensions such as
  Flask-WTF and Flask-Creole should work fine too.
* Selects configurable rendering methods from the template filename, taking
  care of the mimetype, doctype and XML serialization, i.e., how to close
  tags et cetera.

Not yet:

* Flask-Theme probably does not work with Genshi templates.
* `Chameleon`_, not sure if it should be a separate extension or not.


Why Genshi?
-----------

Genshi is one of the slower templating toolkits, the idea of writing XML for
templating seem horrifying and Jinja is a very nice text-based template
engine. Why would Genshi possibly be interesting?

* Templates are rarely the culprit in application performance. If Genshi does
  become a culprit you can render your templates with `Chameleon`_ which
  performs very well.

* XML lends itself naturally to templating HTML. Genshi templates are usually
  much more terse and readable because Python constructs can be terminated by
  the XML end tags and translation strings can be extracted directly from
  the content of text elements.

  We can also operate programmatically on template streams and run filters
  and transformations. We can have a layout template extract a subtitle from
  a page template's title tag. Many possibilities.

  Take this Jinja template:

  .. code-block:: html+jinja

      <title>{% block title %}Page Title{% endblock %}</title>
      {% if show_paragraph %}
        <p>{% trans %}Example paragraph with {{ variable }} content{% endtrans %}
      {% endif %}

  Compare with the Genshi version:

  .. code-block:: html+genshi

      <title>Page Title</title>
      <p py:if="show_paragraph">Example paragraph with $variable content</p>

* For better or worse, Python in Genshi templates is really Python. The only
  difference is that, like with Jinja, attribute access falls back on item
  access and vice versa. You need only know some basic Python and XML to write
  Genshi templates, and you can use existing XML tools such as support in editors.

* Because invalid XML results in template errors, valid output is enforced without
  a need to use HTML validators. You get the benefits of XHTML with browser-friendly
  output, and you can swap the output format on-the-fly. You're also writing actual
  XML so no need for those pesky spaces in self-closing tags: ``<hr/>`` will render
  to HTML as ``<hr>`` and to XHTML as ``<hr />``.


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


Using Jinja filters and tests
-----------------------------

Flask-Genshi supports tests and filters from Jinja. Filters are exposed in
the top-level namespace as-is, tests with ``is`` prepended to their name.
Both are also accessible unchanged under the ``filters`` and ``tests``
namespaces.

.. code-block:: html+genshi

    <p class="${'even' if iseven(1) else 'odd'}">
      ${truncate('Hello World', 10)}
    </p>

Same thing:

.. code-block:: html+genshi

    <p class="${'even' if tests.even(1) else 'odd'}">
      ${filters.truncate('Hello World', 10)}
    </p>

Result:

.. code-block:: html

    <p class="odd">
      Hello ...
    </p>

.. versionchanged:: 0.6 Top-level access.


Module templates
----------------

Flask can load templates specific to a :class:`flask.Module` and
Flask-Genshi also supports this. It works just like in Flask::

    render_response('modname/template.html')

This will first look for, e.g. ``app/templates/modname/template.html``,
and if not found, e.g. ``app/mods/modname/templates/template.html``.
This lets you override module templates in your application.

.. versionadded:: 0.4


Context processors
------------------

Context processors work as expected.

::

    @app.context_processor
    def add_site_name():
        return dict(site_name=app.config['SITE_NAME'])

This lets you use ``site_name`` in templates without including it in every
render call.

.. code-block:: html+genshi

    <title>$site_name</title>

.. versionadded:: 0.4


Render from strings
-------------------

Like :func:`flask.render_template_string`, Flask-Genshi lets you render
strings as templates::

    render_response(string='Hello $name', context={'name': 'World'}, method='text')

The same pattern applies to all functions.

.. versionadded:: 0.4


Using with flatland
-------------------

First, add the flatland filter::

    from flatland.out.genshi import flatland_filter

    @genshi.filter('html')
    def inject_flatland(template, context):
        return flatland_filter(template, context)

Don't forget the form namespace:

.. code-block:: html+genshi

    <html xmlns:form="http://ns.discorporate.us/flatland/genshi">
      <input type="text" form:bind="form.username"/>
    </html>

.. versionadded:: 0.5


Using with Flask-Babel
----------------------

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


Signal support
--------------

Flask-Genshi supports a signal similar to :data:`flask.template_rendered`
called :data:`template_generated`. It is sent the template object and the
context that was used to generate the template stream, when one is
successfully generated.

.. versionadded:: 0.5


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


API Reference
-------------

.. autoclass:: Genshi
    :members:

.. data:: template_generated

   Signal emitted when a template stream has been successfully generated,
   passing `template` and `context` via the app as sender.

   .. versionadded:: 0.5

.. autofunction:: generate_template

.. autofunction:: render_template

.. autofunction:: render_response


.. _Flask: http://flask.pocoo.org/
.. _Genshi: http://genshi.edgewall.org/
.. _Flask-Babel: http://packages.python.org/Flask-Babel/
.. _Chameleon: http://chameleon.repoze.org/docs/latest/genshi.html
.. _Internationalization and Localization:
    http://genshi.edgewall.org/wiki/Documentation/0.6.x/i18n.html
