Flask-Genshi
============

.. currentmodule:: flask_genshi

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


User's Guide
------------

.. toctree::

    quickstart
    flask
    others


API Reference
-------------

.. toctree::

    api


.. _Flask: http://flask.pocoo.org/
.. _Genshi: http://genshi.edgewall.org/
.. _Flask-Babel: http://packages.python.org/Flask-Babel/
.. _Chameleon: http://chameleon.repoze.org/docs/latest/genshi.html
