Contributing to Spatial Current Python Harvester (sc-python-harvester)
==============

Contributor License Agreement
-----------------

Thank you for your interest in contributing.  You will first need to agree to the license.  Simply post the following paragraph, with "your name" and "your github account" substituted as needed, to the first issue `#1`_.  Otherwise, you can email us `here`_.

.. _#1: https://github.com/spatialcurrent/sc-python-harvester/issues/1
.. _here: mailto:opensource@spatialcurrent.io

I, **< YOUR NAME > (< YOUR GITHUB ACCOUNT >)**, agree to the license terms.  My contributions to this repo are granted to **Spatial Current, Inc.** under a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable license and/or copyright is transferred.

Versioning
-----------------

This repo is for accessing metadata via public APIs from other projects, so it will be kept in sync with the latest stable releases of those projects.  If there are large backwards incompatible changes in those projects, then a new branch in this repo will be created.  However, semantic versioning will not be implemented until it makes sense given the burden and releases cycles.

Authors
-----------------

See `AUTHORS`_ for a list of contributors.

.. _AUTHORS: https://github.com/spatialcurrent/sc-python-harvester/blob/master/AUTHORS

Documentation
-----------------

To build documentation first install sphinx via PyPI_ with:

.. _PyPI: https://pypi.python.org/pypi

.. code-block:: bash

    pip install sphinx sphinx_rtd_theme

Change directory to the **docs** directory then build with:

.. code-block:: bash

    ./make-docs.sh

Tests
-----------------

Run tests with:

.. code-block:: bash

    python -m unittest pyextract.test
