Flask Integration
=================

* Templates are looked up in the same places as for Jinja templates,
  including support for blueprints.
* Context processors are supported, including the default Flask context of
  request, session and g etc.
* Template filters are supported provided they're not using Jinja specific
  features.
* Response objects use the class configured for the Flask application, when
  rendering responses with a |MIME| type.  This can be used to set an
  output encoding other than the |UTF8| default.
* Various signals are emitted in a similar fashion to the
  `~flask.template_rendered` signal in Flask.


Jinja Integration
=================

Any globals, tests and filters in the `~flask.Flask.jinja_env` that are not
using Jinja-specific features such as the "evalcontext" are exported to
Genshi templates as well, with some modifications:

* Globals mimicking builtins are not exported -- Genshi already exports the
  native builtins.
* Tests get "is" prepended to them.
* Filters are wrapped in `Pipe`.

As a result Jinja templates translate more easily to Genshi.  Take this
Jinja example:

.. sourcecode:: html+jinja

  <p class="{{ 'even' if 1 is even else 'odd' }}">
    {{ lipsum(html=False) | truncate }}
  </p>

With Flask-Genshi you can write this as such:

.. sourcecode:: html+genshi

  <p class="${ 'even' if iseven(1) else 'odd' }">
    ${ lipsum(html=False) | truncate }
  </p>
