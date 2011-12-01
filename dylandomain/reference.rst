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

   :Syntax 1:  ``:dylan:drm:`linkname```
   :Syntax 2:  ``:dylan:drm:`displayed text <linkname>```

   *linkname* is an exported name or the last part of the URL of a page or
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


Directives with content
-----------------------

``dylan:library::``
^^^^^^^^^^^^^^^^^^^

   A library. You can document the modules exported by the library inside or
   after this directive, or elsewhere via `dylan:current-library::`_.
   
   :Syntax:       ``.. dylan:library:: name``
   :Arguments:    None
   :Reference:    `:dylan:lib:`_

``dylan:module::``
^^^^^^^^^^^^^^^^^^

   A module. You can document the names exported by the module inside or after
   this directive, or elsewhere via `dylan:current-module::`_.
   
   :Syntax:       ``.. dylan:module:: name``
   :Arguments:    None
   :Reference:    `:dylan:mod:`_

``dylan:class::``
^^^^^^^^^^^^^^^^^

   A class.

   :Syntax:       ``.. dylan:class:: name``
   :Arguments:    `:super:`_, `:keyword:`_, `:signal:`_, `:open:`_, `:primary:`_,
                  `:abstract:`_
   :Reference:    `:dylan:class:`_

   Example::
   
      .. class:: <vector>
         :super: <array>
         :keyword: size: An instance of `<integer>`:class: specifying the size
                         of the vector. The default value is ``0``.
         :keyword: fill:
             An instance of `<object>`:class: specifying the initial value for
             each element of the vector. The default value is ``#f``.

``dylan:generic-function::``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   A generic function.
   
   :Syntax:       ``.. dylan:generic-function:: name``
   :Arguments:    `:param:`_, `:retval:`_, `:signal:`_, `:sealed:`_
   :Reference:    `:dylan:gf:`_
   
   Example::
   
      .. generic-function:: member?
         :param:  value       An instance of `<object>`:class:.
         :param:  collection  An instance of `<collection>`:class:.
         :param:  test:       An instance of `<function>`:class:. The default is
                              `==`:gf:.
         :retval: boolean     An instance of `<boolean>`:class:.
      
      .. method::
         :signature: <object>, <range>

``dylan:method::``
^^^^^^^^^^^^^^^^^^

   A method of a generic function.
   
   :Syntax:       ``.. dylan:method:: name``
   :Arguments:    `:signature:`_, `:param:`_, `:retval:`_, `:signal:`_
   :Reference:    `:dylan:meth:`_
   
   After a generic function, *name* and all arguments other than *signature* may
   be omitted. The arguments of the generic function will be used. See
   `dylan:generic-function::`_ for an example of this.
   
   References to a method must be disambiguated by enclosing the signature in
   parentheses, as shown by the reference to ``type-for-copy`` in the following
   example.
   
   Example::
      
      .. method:: copy-sequence
         :signature: <range>
         :param:  source   An instance of `<range>`:class:.
         :param:  start:   An instance of `<integer>`:class. The default is
                           ``0``.
         :param:  end:     An instance of `<integer>`:class. The default is the
                           size of *source*.
         :retval: new-range   A freshly allocated instance of `<range>`:class:.
         
         *new-range* will be a `<range>`:class: even though the return value of
         `type-for-copy(<range>)`:meth: is a `<list>`:class:.


``dylan:function::``
^^^^^^^^^^^^^^^^^^^^

   A function that does not belong to a generic function.
   
   :Syntax:       ``.. dylan:function:: name``
   :Arguments:    `:param:`_, `:retval:`_, `:signal:`_
   :Reference:    `:dylan:func:`_

``dylan:constant::``
^^^^^^^^^^^^^^^^^^^^

   A constant.
   
   :Syntax:       ``.. dylan:constant:: name``
   :Arguments:    `:type:`_, `:value:`_
   :Reference:    `:dylan:const:`_

``dylan:variable::``
^^^^^^^^^^^^^^^^^^^^

   A variable.
   
   :Syntax:       ``.. dylan:variable:: name``
   :Arguments:    `:type:`_, `:value:`_
   :Reference:    `:dylan:var:`_

``dylan:macro::``
^^^^^^^^^^^^^^^^^

   A macro.
   
   :Syntax:       ``.. dylan:macro:: name``
   :Arguments:    `:param:`_, `:retval:`_, `:signal:`_
   :Reference:    `:dylan:macro:`_

``dylan:unbound-name::``
^^^^^^^^^^^^^^^^^^^^^^^^

   A name that was exported but not bound, as by a module's ``create`` clause.
   
   :Syntax:       ``.. dylan:unbound-name:: name``
   :Arguments:    None
   :Reference:    `:dylan:name:`_


Directives without content
--------------------------

``dylan:current-library::``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Sets the library currently being documented when the actual library
   documentation is elsewhere. You can document the modules exported by the
   library after this directive.
   
   :Syntax:    ``.. dylan:current-library:: name``
   :Arguments: None

``dylan:current-module::``
^^^^^^^^^^^^^^^^^^^^^^^^^^

   Sets the module currently being documented when the actual module
   documentation is elsewhere. You can document the names exported by the module
   after this directive.

   :Syntax:    ``.. dylan:current-module:: name``
   :Arguments: None
   
``dylan:reexport::``
^^^^^^^^^^^^^^^^^^^^

   A name or module that is simply reexported from elsewhere. This creates a
   cross-reference.
   
   :Syntax:    ``.. dylan:reexport:: name from library:module:name``
   :Arguments: None

   You may omit *library* or *module* to use the current library or module. The
   following ``reexport`` directives are all equivalent::

      .. current-library:: io
      .. current-module::  streams
         
      .. reexport:: close-stream from io:streams:close
      .. reexport:: close-stream from streams:close
      .. reexport:: close-stream from close


Directive arguments
-------------------

``:super:``
^^^^^^^^^^^

   A superclass of a class. This argument may appear multiple times.
   
   :Syntax: ``:super: library:module:name``
   
   You may omit *library* or *module* to use the current library or module.

``:keyword:``
^^^^^^^^^^^^^

   An init-keyword of a class. This argument may appear multiple times.
   
   :Syntax: ``:keyword: name description``
   
   See `dylan:class::`_ for an example.

``:param:``
^^^^^^^^^^^

   A parameter of a generic function or method. This argument may appear
   multiple times.
   
   :Syntax: ``:param: name description``
   
   See `dylan:generic-function::`_ and `dylan:method::`_ for examples.
   
``:retval:``
^^^^^^^^^^^^

   A return value of a generic function or method. This argument may appear
   multiple times.
   
   :Syntax: ``:retval: name description``
   
   See `dylan:generic-function::`_ and `dylan:method::`_ for examples.

``:signature:``
^^^^^^^^^^^^^^^

   The signature of the method -- the types of its required parameters. This
   argument is required in `dylan:method::`_ directives.
   
   :Syntax: ``:signature: expression, expression, ...``
   
   If *expression* is a *library:module:name* expression (*library* and *module*
   optional), it will make a cross-reference.
   
   See `dylan:generic-function::`_ and `dylan:method::`_ for examples.
   
``:type:``
^^^^^^^^^^

   The type of a variable or constant.
   
   :Syntax: ``:type: expression``

   If *expression* is a *library:module:name* expression (*library* and *module*
   optional), it will make a cross-reference.

``:value:``
^^^^^^^^^^^

   The initial value of a variable or constant.
   
   :Syntax: ``:value: expression``
   
``:open:``
^^^^^^^^^^

   Indicates an open class.
   
   :Syntax: ``:open:``

``:primary:``
^^^^^^^^^^^^^
   
   Indicates a primary class.
   
   :Syntax: ``:primary:``

``:abstract:``
^^^^^^^^^^^^^^

   Indicates an abstract class.
   
   :Syntax: ``:abstract:``

``:sealed:``
^^^^^^^^^^^^

   Indicates a sealed generic function.
   
   :Syntax: ``:sealed:``

``:signal:``
^^^^^^^^^^^^

   Describes a condition signaled by the class's ``make`` method or another
   method. This argument may appear multiple times.
   
   :Syntax: ``:signal: description``


Roles
-----

   All cross-referencing roles except `:dylan:meth:`_ have the same syntax. This
   syntax is similar to the syntax of cross-referencing roles for other
   languages, but if you use the ``!`` or ``~`` marks, you must enclose the
   target in ``< >``.
   
   :Syntax 1: ``:dylan:role:`library:module:name```
   :Syntax 2: ``:dylan:role:`text <library:module:name>```
   :Syntax 3: ``:dylan:role:`mark <library:module:name>```
   :Syntax 4: ``:dylan:role:`mark text <library:module:name>```
   
   - You may omit *library* or *module* to use the current library or module.
   - *mark* may be ``!`` to avoid making a hyperlink, or ``~`` to only show the
     *name* part of the identifier, or both.
     
   Examples::
   
      .. current-library:  io
      .. current-module:   streams
      
      Be sure to call `~ <dylan:dylan:copy-sequence>`:gf: to avoid
      unintentionally changing the values of the sequence.
      
      See `the <stream> class <<stream>>`:class: for more information.
      

``:dylan:lib:``
^^^^^^^^^^^^^^^

   See `dylan:library::`_.

``:dylan:mod:``
^^^^^^^^^^^^^^^

   See `dylan:module::`_.

``:dylan:class:``
^^^^^^^^^^^^^^^^^

   See `dylan:class::`_.

``:dylan:gf:``
^^^^^^^^^^^^^^

   See `dylan:generic-function::`_.

``:dylan:meth:``
^^^^^^^^^^^^^^^^

   See `dylan:method::`_.
   
   The syntax is similar to other roles.
   
   :Syntax 1: ``:dylan:meth:`library:module:name(signature)```
   :Syntax 2: ``:dylan:meth:`text <library:module:name(signature)>```
   :Syntax 3: ``:dylan:meth:`mark <library:module:name(signature)>```
   :Syntax 4: ``:dylan:meth:`mark text <library:module:name(signature)>```
   
   - The *signature* component matches a method directive's `:signature:`_
     argument.
   - You may omit *library* or *module* to use the current library or module.
   - *mark* may be ``!`` to avoid making a hyperlink, or ``~`` to only
     show the *name* and *signature* parts of the identifier, or both.


``:dylan:func:``
^^^^^^^^^^^^^^^^

   See `dylan:function::`_.
   
``:dylan:const:``
^^^^^^^^^^^^^^^^^

   See `dylan:constant::`_.
   
``:dylan:var:``
^^^^^^^^^^^^^^^

   See `dylan:variable::`_.
   
``:dylan:macro:``
^^^^^^^^^^^^^^^^^

   See `dylan:macro::`_.
   
``:dylan:name:``
^^^^^^^^^^^^^^^^

   See `dylan:unbound-name::`_.
   