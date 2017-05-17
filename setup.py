#!/usr/bin/env python

from setuptools import setup

setup(
    name='sc_python_harvester',
    version='0.0.1',
    install_requires=[],
    author='Spatial Current Developers',
    author_email='opensource@spatialcurrent.io',
    license='BSD License',
    url='https://github.com/spatialcurrent/sc_python_harvester/',
    keywords='python gis wfs csw ogc',
    description='Python library of utility functions for harvesting metadata from open sources, e.g., GeoNode and CKAN.',
    long_description=open('README.rst').read(),
    download_url="https://github.com/spatialcurrent/sc_python_harvester/zipball/master",
    packages=[
        "sc_python_harvester",
        "sc_python_harvester.ckan",
        "sc_python_harvester.csw",
        "sc_python_harvester.geonode",
        "sc_python_harvester.wfs",
        "sc_python_harvester.xml"],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
