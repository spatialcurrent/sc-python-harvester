pyextract / Getting Started!
============================

Welcome to the documentation for pyextract.  This repo contains a nullsafe-like function for Python that can be used to extract data from dicts, lists, etc.  This function is useful when parsing complex schemas, such as those used by GeoDash_, while limiting the need for verbosity.  To install, follow the `installation`_ instructions.

.. _geodash: http://geodash.io
.. _installation: installation.html

What does it do?
----------------

pyextract provides an easy way to go multiple levels deep into a dict and extract data, in a nullsafe way with a fallback value.  With this functionality, it is straight-forward to have complex fallback logic for schemas, rather than explicitly defining every scenario.  This functionality is used heavily throughout `GeoDash`_-enabled servers.  For example.

.. _geodash: http://geodash.io

.. code-block:: python

    from pyextract.extract import extract

    zoom = (
        extract(["view", "zoom"], state, None) or
        extract(["view", "zoom"], config, None) or
        extract(["view", "minZoom"], config, None) or
        default_zoom or
        3
    )

pyextract can also be used for returning the important data from a JSON API response.

.. code-block:: python

    from pyextract.extract import extract

    users = extract(["result", "users"], json.loads(response_users_text), None)

API
---------------------

See the api documentation for extract_.

.. _extract: api.html
