Integration with Flask
======================

.. currentmodule:: flask_genshi


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


Signal support
--------------

Flask-Genshi supports a signal similar to :data:`flask.template_rendered`
called :data:`template_generated`. It is sent the template object and the
context that was used to generate the template stream, when one is
successfully generated.

.. versionadded:: 0.5
