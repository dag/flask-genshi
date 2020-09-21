API
===

.. module:: flask_genshi


Rendering functions
-------------------

.. autofunction:: render

.. autofunction:: render_response

.. autofunction:: render_template



Extension Object
----------------

.. autoclass:: Genshi
    :members:


Signals
-------

.. data:: template_generated

   Signal emitted when a template stream has been successfully generated,
   passing `template` and `context` via the app as sender.

   .. versionadded:: 0.5


Lesser utilities
----------------

.. autofunction:: generate_template
