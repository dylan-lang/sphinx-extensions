Reference
=========

The Dylan domain adds the following things.

.. role:: dylan:drm

   Reference to a page or exported name in the :cite:`Dylan Reference Manual`.

   Syntax is similar to other links::

	:dylan:drm:`linkname`
	:dylan:drm:`displayed text <linkname>`

   A link name is an exported name or the last part of the URL of a page or
   section. Exported names are converted into partial URLs per the file configured
   by :confval:`dylan_drm_index`. The partial URL is appended to the base URL
   configured by :confval:`dylan_drm_url`.

.. confval:: dylan_drm_url

   The base URL of the :cite:`Dylan Reference Manual`. Defaults to the copy at
   http://opendylan.org.

.. confval:: dylan_drm_index

   A file listing Dylan names and the corresponding :cite:`Dylan Reference Manual`
   partial URLs. Each line is a correspondance. The first word is the Dylan name,
   followed by whitespace, then the remainder is the partial URL. Defaults to
   partial URLs corresponding to the copy of the :cite:`Dylan Reference Manual`
   at http://opendylan.org.
