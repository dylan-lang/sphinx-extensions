**************************
  Dylan Domain Reference
**************************

.. contents::


`Dylan Reference Manual`:t: links
=================================


Roles
-----

``:dylan:drm:``
^^^^^^^^^^^^^^^

   Reference to a page or exported name in the `Dylan Reference Manual`:t:.

   :Syntax 1:  ``:dylan:drm:`LINKNAME```
   :Syntax 2:  ``:dylan:drm:`DISPLAYED TEXT <LINKNAME>```

   *LINKNAME* is an exported name or the last part of the URL of a page or
   section. Exported names are converted into partial URLs per the file
   configured by `dylan_drm_index`_. The partial URL is appended to the base URL
   configured by the `dylan_drm_url`_.
   
   
Configurables
-------------

``dylan_drm_url``
^^^^^^^^^^^^^^^^^

   The base URL of the `Dylan Reference Manual`:t:. Defaults to the base URL of
   the copy at `<http://opendylan.org>`_.

``dylan_drm_index``
^^^^^^^^^^^^^^^^^^^

   A file listing Dylan names and the corresponding `Dylan Reference Manual`:t:
   partial URLs. Each line is a correspondance. The first word is the Dylan
   name, followed by whitespace, then the remainder is the partial URL. Defaults
   to partial URLs corresponding to the copy of the `Dylan Reference Manual`:t:
   at `<http://opendylan.org>`_.


Library, module, and binding documentation
==========================================

The Dylan domain generates an API index in a file called
``dylan-apiindex.html``. Unfortunately, you have to link to it by filename, e.g.
::

  * `API Index <dylan-apiindex.html>`_


Directives with content
-----------------------

``dylan:library::``
^^^^^^^^^^^^^^^^^^^

   A library. You can document the modules exported by the library inside or
   after this directive, or elsewhere via `dylan:current-library::`_.
   
   :Syntax:       ``.. dylan:library:: NAME``
   :Arguments:    None
   :Doc Fields:   None
   :Reference:    `:dylan:lib:`_

``dylan:module::``
^^^^^^^^^^^^^^^^^^

   A module. You can document the names exported by the module inside or after
   this directive, or elsewhere via `dylan:current-module::`_.
   
   :Syntax:       ``.. dylan:module:: NAME``
   :Arguments:    `:library:`_
   :Doc Fields:   None
   :Reference:    `:dylan:mod:`_

``dylan:class::``
^^^^^^^^^^^^^^^^^

   A class.

   :Syntax:       ``.. dylan:class:: NAME``
   :Arguments:    `:open:`_, `:sealed:`_, `:primary:`_, `:free:`_, `:abstract:`_,
                  `:concrete:`_, `:library:`_, `:module:`_
   :Doc Fields:   `:supers:`_, `:keyword:`_, `:slot:`_
   :Reference:    `:dylan:class:`_

   Example::
   
      .. class:: <vector>
         :open:
      
         :supers: `<array>`:class
         :keyword size:  An instance of `<integer>`:class: specifying the size
                         of the vector. The default value is ``0``.
         :keyword fill:
             An instance of `<object>`:class: specifying the initial value for
             each element of the vector. The default value is ``#f``.

``dylan:generic-function::``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   A generic function.
   
   :Syntax:       ``.. dylan:generic-function:: NAME``
   :Arguments:    `:open:`_, `:sealed:`_, `:library:`_, `:module:`_
   :Doc Fields:   `:param:`_, `:value: (1)`_
   :Reference:    `:dylan:gf:`_
   
   Example::
   
      .. generic-function:: member?
         :sealed:
      
         :param value:        An instance of `<object>`:class:.
         :param collection:   An instance of `<collection>`:class:.
         :param #key test:    An instance of `<function>`:class:. The default is
                              `==`:gf:.
         :value bool:         An instance of `<boolean>`:class:.
      
      .. method::
         :specializer: <object>, <range>

``dylan:method::``
^^^^^^^^^^^^^^^^^^

   A method of a generic function.
   
   :Syntax:       ``.. dylan:method:: NAME``
   :Arguments:    `:specializer:`_, `:library:`_, `:module:`_
   :Doc Fields:   `:param:`_, `:value: (1)`_
   :Reference:    `:dylan:meth:`_
   
   After a generic function, *NAME* and all doc fields may be omitted. The name
   and arguments of the generic function will be used. See
   `dylan:generic-function::`_ for an example of this.
   
   References to a method must be disambiguated by enclosing *SPECIALIZER* in
   parentheses, as shown by the reference to ``type-for-copy`` in the following
   example. The specializer is author-defined and does not necessarily have to
   reflect all the parameters of the method.
   
   Example::
      
      .. method:: copy-sequence
         :specializer: <range>
         
         :param source:       An instance of `<range>`:class:.
         :param #key start:   An instance of `<integer>`:class. The default is
                              ``0``.
         :param #key end:     An instance of `<integer>`:class. The default is
                              the size of *source*.
         :value new-range:    A freshly allocated instance of `<range>`:class:.
         
         *new-range* will be a `<range>`:class: even though the return value of
         `type-for-copy(<range>)`:meth: is a `<list>`:class:.

``dylan:function::``
^^^^^^^^^^^^^^^^^^^^

   A function that does not belong to a generic function.
   
   :Syntax:       ``.. dylan:function:: NAME``
   :Arguments:    `:library:`_, `:module:`_
   :Doc Fields:   `:param:`_, `:value: (1)`_
   :Reference:    `:dylan:func:`_

``dylan:constant::``
^^^^^^^^^^^^^^^^^^^^

   A constant.
   
   :Syntax:       ``.. dylan:constant:: NAME``
   :Arguments:    `:library:`_, `:module:`_
   :Doc Fields:   `:type:`_, `:value: (2)`_
   :Reference:    `:dylan:const:`_

``dylan:variable::``
^^^^^^^^^^^^^^^^^^^^

   A variable.
   
   :Syntax:       ``.. dylan:variable:: NAME``
   :Arguments:    `:library:`_, `:module:`_
   :Doc Fields:   `:type:`_, `:value: (2)`_
   :Reference:    `:dylan:var:`_

``dylan:macro::``
^^^^^^^^^^^^^^^^^

   A macro.
   
   :Syntax:       ``.. dylan:macro:: NAME``
   :Arguments:    `:library:`_, `:module:`_
   :Doc Fields:   `:param:`_, `:value: (1)`_
   :Reference:    `:dylan:macro:`_


Directives without content
--------------------------

``dylan:current-library::``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Sets the library currently being documented when the actual library
   documentation is elsewhere. You can document the modules exported by the
   library after this directive.
   
   :Syntax:    ``.. dylan:current-library:: LIBRARY``
   :Arguments: None

``dylan:current-module::``
^^^^^^^^^^^^^^^^^^^^^^^^^^

   Sets the module currently being documented when the actual module
   documentation is elsewhere. You can document the names exported by the module
   after this directive.

   :Syntax:    ``.. dylan:current-module:: MODULE``
   :Arguments: None


Directive doc fields
--------------------

Doc fields appear in the directive's content. Doc fields must be separated from
the directive and any directive arguments by a blank line.

``:supers:``
^^^^^^^^^^^^

   A superclass of a class. This doc field may appear multiple times.
   
   :Syntax:    ``:supers: DESCRIPTION``
   :Synonyms:  ``:superclasses:``, ``:super:``, ``:superclass:``

``:keyword:``
^^^^^^^^^^^^^

   An init-keyword of a class. This doc field may appear multiple times.
   
   :Syntax:    ``:keyword NAME: DESCRIPTION``
   :Synonyms:  ``:init-keyword:``
   
   See `dylan:class::`_ for an example.

``:slot:``
^^^^^^^^^^

   A slot of a class. This doc field may appear multiple times.
   
   :Syntax:    ``:slot NAME: DESCRIPTION``
   :Synonyms:  ``:getter:``

``:param:``
^^^^^^^^^^^

   A parameter of a generic function or method. This doc field may appear
   multiple times.
   
   :Syntax 1:  ``:param NAME: DESCRIPTION``
   :Syntax 2:  ``:param #key NAME: DESCRIPTION``
   :Syntax 3:  ``:param #rest NAME: DESCRIPTION``
   :Synonyms:  ``:parameter:``, ``:argument:``, ``:arg:``
   
   See `dylan:generic-function::`_ and `dylan:method::`_ for examples.
   
``:value:`` (1)
^^^^^^^^^^^^^^^

   A return value of a generic function or method. This doc field may appear
   multiple times.
   
   :Syntax 1:  ``:value NAME: DESCRIPTION``
   :Syntax 2:  ``:value #rest NAME: DESCRIPTION``
   :Synonyms:  ``:return:``, ``:retval:``, ``:val:``
   
   See `dylan:generic-function::`_ and `dylan:method::`_ for examples.

``:type:``
^^^^^^^^^^

   The type of a variable or constant.
   
   :Syntax:    ``:type: EXPRESSION``
   :Synonyms:  None

``:value:`` (2)
^^^^^^^^^^^^^^^

   The initial value of a variable or constant.
   
   :Syntax:    ``:value: EXPRESSION``
   :Synonyms:  ``:val:``


Directive arguments
-------------------

Directive arguments appear immediately after the directive with no intervening
blank lines.

``:library:``
^^^^^^^^^^^^^

   Sets the current library, also affecting documentation following the
   directive. Mostly for automatically-generated documentation; hand-written
   documentation can use `dylan:current-library::`_.
   
   :Syntax: ``:library: NAME``

``:module:``
^^^^^^^^^^^^^

   Sets the current module, also affecting documentation following the
   directive. Mostly for automatically-generated documentation; hand-written
   documentation can use `dylan:current-module::`_.
   
   :Syntax: ``:module: NAME``

``:specializer:``
^^^^^^^^^^^^^^^^^

   A way to distinguish one method from another -- generally a list of the types
   of its required parameters. This argument is required in `dylan:method::`_
   directives.
   
   :Syntax: ``:specializer: EXPRESSION, EXPRESSION, ...``
   
   See `dylan:generic-function::`_ and `dylan:method::`_ for examples.
   
``:open:``
^^^^^^^^^^

   Indicates an open class or generic function.
   
   :Syntax: ``:open:``

``:primary:``
^^^^^^^^^^^^^
   
   Indicates a primary class.
   
   :Syntax: ``:primary:``

``:free:``
^^^^^^^^^^
   
   Indicates a free class.
   
   :Syntax: ``:free:``

``:abstract:``
^^^^^^^^^^^^^^

   Indicates an abstract class.
   
   :Syntax: ``:abstract:``

``:concrete:``
^^^^^^^^^^^^^^
   
   Indicates a concrete class.
   
   :Syntax: ``:concrete:``

``:sealed:``
^^^^^^^^^^^^

   Indicates a sealed generic function or class.
   
   :Syntax: ``:sealed:``


Roles
-----

   All cross-referencing roles except `:dylan:meth:`_ have the same syntax. This
   syntax is similar to the syntax of cross-referencing roles for other
   languages, but if you use the ``!`` or ``~`` marks, you must enclose the
   target in ``< >``.
   
   :Syntax 1: ``:dylan:role:`LIBRARY:MODULE:NAME```
   :Syntax 2: ``:dylan:role:`TEXT <LIBRARY:MODULE:NAME>```
   :Syntax 3: ``:dylan:role:`MARK <LIBRARY:MODULE:NAME>```
   :Syntax 4: ``:dylan:role:`MARK TEXT <LIBRARY:MODULE:NAME>```
   
   - You may omit *LIBRARY* or *MODULE* to use the current library or module.
   - *MARK* may be ``!`` to avoid making a hyperlink, or ``~`` to only show the
     *NAME* part of the identifier, or both.
     
   Examples::
   
      .. current-library:  io
      .. current-module:   streams
      
      Be sure to call `~ <dylan:dylan:copy-sequence>`:gf: to avoid
      unintentionally changing the values of the sequence.
      
      See `the <stream> class <<stream>>`:class: for more information.
      
``:dylan:lib:``
^^^^^^^^^^^^^^^

   Creates a cross-reference to a `dylan:library::`_ directive.

``:dylan:mod:``
^^^^^^^^^^^^^^^

   Creates a cross-reference to a `dylan:module::`_ directive.

``:dylan:class:``
^^^^^^^^^^^^^^^^^

   Creates a cross-reference to a `dylan:class::`_ directive.

``:dylan:gf:``
^^^^^^^^^^^^^^

   Creates a cross-reference to a `dylan:generic-function::`_ directive.

``:dylan:meth:``
^^^^^^^^^^^^^^^^

   Creates a cross-reference to a `dylan:method::`_ directive.
   
   The syntax is similar to other roles.
   
   :Syntax 1: ``:dylan:meth:`LIBRARY:MODULE:NAME(SPECIALIZER)```
   :Syntax 2: ``:dylan:meth:`TEXT <LIBRARY:MODULE:NAME(SPECIALIZER)>```
   :Syntax 3: ``:dylan:meth:`MARK <LIBRARY:MODULE:NAME(SPECIALIZER)>```
   :Syntax 4: ``:dylan:meth:`MARK TEXT <LIBRARY:MODULE:NAME(SPECIALIZER)>```
   
   - The *SPECIALIZER* component matches a method directive's `:specializer:`_
     argument.
   - You may omit *LIBRARY* or *MODULE* to use the current library or module.
   - *MARK* may be ``!`` to avoid making a hyperlink, or ``~`` to only
     show the *NAME* and *SPECIALIZER* parts of the identifier, or both.

.. note:: Syntax 1 does not actually work. But give it a title or mark, and it
   should be okay.

``:dylan:func:``
^^^^^^^^^^^^^^^^

   Creates a cross-reference to a `dylan:function::`_ directive.
   
``:dylan:const:``
^^^^^^^^^^^^^^^^^

   Creates a cross-reference to a `dylan:constant::`_ directive.
   
``:dylan:var:``
^^^^^^^^^^^^^^^

   Creates a cross-reference to a `dylan:variable::`_ directive.
   
``:dylan:macro:``
^^^^^^^^^^^^^^^^^

   Creates a cross-reference to a `dylan:macro::`_ directive.
   