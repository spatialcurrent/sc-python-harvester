# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 Spatial Current, Inc.
#
#########################################################################
"""
Contains utility functions for CKAN
"""


import hashlib
import requests

try:
    from flask import json
except ImportError:
    import json

from pyextract.extract import extract

from sc_python_harvester.ckan.enumerations import INFINITY_VALUES


def ckan_collect_packages(url, memcached_client=None, cache=0):
    """
    collect CKAN packages

    :param url: the CKAN url, e.g., .../api/3/action/package_list
    :param memcached_client: pymemcache client for caching http response
    :param cache: cache results
    :return: a list of CKAN packages
    """
    packages = None

    memcached_key = None
    response_catalog_json = None
    if cache and (memcached_client is not None):
        memcached_key = hashlib.md5(url).hexdigest()
        response_catalog_json = memcached_client.get(memcached_key)

    if response_catalog_json is None:
        response_catalog = requests.get(url, params=None)
        if response_catalog.status_code == 200:
            try:
                response_catalog_json = response_catalog.json()
            except Exception as err:
                response_catalog_json = None
                print err
                print "Response Text:", response_catalog.text
        else:
            print "Error: Could not retrieve pacakge list from ",
            print "Status Code:", response_catalog.status_code

        if response_catalog_json is not None:
            if cache and (memcached_client is not None):
                memcached_client.set(memcached_key, response_catalog_json)

    if response_catalog_json is not None:
        packages = extract(["result"], response_catalog_json, None)

    return packages


def ckan_collect_users(url, memcached_client=None, cache=0):
    """
    collect CKAN users

    :param url: the CKAN url, e.g., .../api/3/action/package_list
    :param memcached_client: pymemcache client for caching http response
    :param cache: cache results
    :return: a list of CKAN users
    """
    users = None

    memcached_key = None
    response_users_text = None
    if cache and (memcached_client is not None):
        memcached_key = hashlib.md5(url).hexdigest()
        response_users_text = memcached_client.get(memcached_key)

    if response_users_text is None:
        response_users = requests.get(url, params=None)
        if response_users.status_code == 200:
            try:
                response_users_text = response_users.text.encode("utf-8")
            except Exception as err:
                response_users_text = None
                print err
                print "Response Text:", response_users.text
        else:
            print "Error: Could not retrieve user list from ",
            print "Status Code:", response_users.status_code

        if response_users_text is not None:
            if cache and (memcached_client is not None):
                memcached_client.set(memcached_key, response_users_text)

    if response_users_text is not None:
        users = extract(["result"], json.loads(response_users_text), None)

    return users


def find_bbox(r):
    """
    find bbox from CKAN resource

    :param r: the CKAN resource, e.g., .../api/3/action/package_list
    :return: bounding box as a list [west, south, east, north], or None if not found
    """
    bbox = None

    r_shape_info = extract(["shape_info"], r, None)
    if r_shape_info is not None:
        r_bbox_text = json.loads(r_shape_info).get("bounding_box")
        if (r_bbox_text is not None) and (len(r_bbox_text) > 0):
            ll_ur = r_bbox_text[4:len(r_bbox_text)-1].split(",")
            if ll_ur:
                ll_ur = [xy.split(" ") for xy in ll_ur]
                ll = [float(n) for n in ll_ur[0]]
                ur = [float(n) for n in ll_ur[1]]
                bbox = [ll[0], ll[1], ur[0], ur[1]]
                if len(INFINITY_VALUES.intersection(bbox)) > 0:
                    bbox = None

    return bbox
