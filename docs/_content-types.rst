Content Types
=============

Flask-Genshi has a concept of "content types" that control how Genshi will
parse and serialize a template, and which |DOCTYPE| to use for |HTML| and
|XML| documents.

Content types are configured by Internet Media Types, commonly known as
|MIME| types.  The type is guessed from the filename extension of the
template.  It is possible to use glob-style pattern matching in type
configurations, with exact matches taking the highest precedence and the
catch-all :mimetype:`*/*` taking the lowest.  These configurations are
included by default:


.. list-table::
  :header-rows: 1

  * - |MIME| type
    - Serializer
    - |DOCTYPE|
    - Dialect

  * - :mimetype:`*/\*`
    - |XMLSerializer|
    -
    - |MarkupTemplate|

  * - :mimetype:`text/html`
    - |HTMLSerializer|
    - |HTML| 5
    - |MarkupTemplate|

  * - :mimetype:`application/xhtml+xml` [#]_
    - |XMLSerializer|
    - |XHTML| 1.1
    - |MarkupTemplate|

  * - :mimetype:`text/\*`
    - |TextSerializer|
    -
    - |TextTemplate| [#]_


.. admonition:: Notes

  .. [#] It's unlikely you want to send |XHTML| -- you don't get any of the
         new |HTML| 5 features and Internet Explorer doesn't support it at
         all.  With Genshi you also get many of the perceived benefits of
         XHTML server-side without forcing it on clients.

         Sometimes people send XHTML as :mimetype:`text/html` with
         HTML compatible markup but this is a hack that causes the browser
         to parse XHTML according to HTML rules!  The default XHTML
         configuration in Flask-Genshi doesn't pretend to be HTML and uses
         the correct |MIME| type.

  .. [#] Text templates are configured for completeness sake, but Jinja is
         a much more capable engine for text templating and is always
         configured in Flask anyway.
