API
===

.. module:: flaskext.genshi


.. autoclass:: Genshi
    :members:

.. data:: template_generated

   Signal emitted when a template stream has been successfully generated,
   passing `template` and `context` via the app as sender.

   .. versionadded:: 0.5

.. autofunction:: generate_template

.. autofunction:: render_template

.. autofunction:: render_response
