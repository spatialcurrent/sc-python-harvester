# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 Spatial Current, Inc.
#
#########################################################################
"""
Contains utility functions for GeoNode
"""


import hashlib
import requests

try:
    from flask import json
except ImportError:
    import json

from pyextract.extract import extract


def geonode_collect_profiles(url, memcached_client=None, cache=0):
    """
    collect list of user profiles from a GeoNode instance

    :param url: the url to the profiles API, e.g., .../api/profiles
    :param memcached_client: pymemcache client for caching http response
    :param cache: cache results
    :return: a list of dicts representing user profiles
    """
    profiles = None

    memcached_key = None
    response_profiles_json = None
    if cache and (memcached_client is not None):
        memcached_key = hashlib.md5(url).hexdigest()
        response_profiles_json = memcached_client.get(memcached_key)

    if response_profiles_json is None:
        response_catalog = requests.get(url, params=None)
        if response_catalog.status_code == 200:
            try:
                response_profiles_json = response_catalog.json()
            except Exception as err:
                response_profiles_json = None
                print err
                print "Response Text:", response_catalog.text
        else:
            print "Error: Could not retrieve pacakge list from ",
            print "Status Code:", response_catalog.status_code

        if response_profiles_json is not None:
            if cache and (memcached_client is not None):
                try:
                    memcached_client.set(memcached_key, response_profiles_json)
                except:
                    print "Error: Could not cache response_text for url ", url

    if response_profiles_json is not None:
        profiles = extract(["objects"], response_profiles_json, None)

    return profiles


def geonode_collect_resourcebase(url, memcached_client=None, cache=0):
    """
    collect resource bases from a GeoNode instance

    :param url: the url to the resource base API, e.g., .../api/base
    :param memcached_client: pymemcache client for caching http response
    :param cache: cache results
    :return: a list of dicts representing resource bases
    """
    resourcebases = None

    memcached_key = None
    response_text = None
    if cache and (memcached_client is not None):
        memcached_key = hashlib.md5(url).hexdigest()
        response_text = memcached_client.get(memcached_key)

    if response_text is None:
        response_catalog = requests.get(url, params=None)
        if response_catalog.status_code == 200:
            try:
                response_text = response_catalog.text.encode('utf-8')
            except Exception as err:
                response_text = None
                print err
                print "Response Text:", response_catalog.text
        else:
            print "Error: Could not retrieve pacakge list from ",
            print "Status Code:", response_catalog.status_code

        if response_text is not None:
            if cache and (memcached_client is not None):
                try:
                    memcached_client.set(memcached_key, response_text)
                except:
                    print "Error: Could not cache response_text for url ", url

    if response_text is not None:
        resourcebases = extract(["objects"], json.loads(response_text), None)

    return resourcebases
