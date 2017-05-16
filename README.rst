Spatial Current Python Harvester (sc-python-harvester)
==============

.. image:: https://travis-ci.org/spatialcurrent/sc-python-harvester.png
    :target: https://travis-ci.org/spatialcurrent/sc-python-harvester

.. image:: https://img.shields.io/pypi/v/sc-python-harvester.svg
    :target: https://pypi.python.org/pypi/sc-python-harvester

.. image:: https://readthedocs.org/projects/sc-python-harvester/badge/?version=master
        :target: http://sc-python-harvester.readthedocs.org/en/latest/
        :alt: Master Documentation Status

Description
-----------------

This repo contains Python utility functions for harvesting metadata from open-standard sources, e.g., `GeoNode`_ and `CKAN`_.

.. _GeoNode: http://geonode.org
.. _CKAN: https://ckan.org


Installation
-----------------

Install directly from GitHub with:

.. code-block:: bash

    pip install git+git://github.com/spatialcurrent/sc-python-harvester.git@master

Usage
-----------------

Simply import the enumerations and functions as needed.

.. code:: python

   from sc_python_harvester.wfs.utils import wfs_describe_layer
   from sc_python_harvester.wfs.enumerations import WFS_DEFAULT_NAMESPACES

   attributes, geometry_type = wfs_describe_layer(wfs_url, typename, ns=WFS_DEFAULT_NAMESPACES)

Contributing
-----------------

`Spatial Current, Inc.`_ is currently accepting pull requests for this repository.  We'd love to have your contributions!  Please see `Contributing.rst`_ for how to get started.

.. _`Spatial Current, Inc.`: https://spatialcurrent.io
.. _Contributing.rst: https://github.com/spatialcurrent/sc-python-harvester/blob/master/CONTRIBUTING.rst

License
-----------------

This work is distributed under the **MIT License**.  See **LICENSE** file.
