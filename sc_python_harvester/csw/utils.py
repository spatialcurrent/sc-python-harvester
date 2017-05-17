# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 Spatial Current, Inc.
#
#########################################################################
import hashlib
import requests

try:
    from flask import json
except ImportError:
    import json

from sc_python_harvester.xml.utils import find_deep, findall_deep, find_float, find_text


def find_bbox(node, ns, fallback=None):
    bbox = None
    element = find_deep(node, "gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox", ns)
    if element is not None:
        west = find_float(element, "gmd:westBoundLongitude/gco:Decimal", ns, fallback=-180.0)
        south = find_float(element, "gmd:southBoundLatitude/gco:Decimal", ns, fallback=-90.0)
        east = find_float(element, "gmd:eastBoundLongitude/gco:Decimal", ns, fallback=180.0)
        north = find_float(element, "gmd:northBoundLatitude/gco:Decimal", ns, fallback=90.0)
        return [west, south, east, north]
    else:
        return fallback;


def sniff_detail_url(node, ns):
    detail_url = None
    for element in findall_deep(node, 'gmd:CI_OnlineResource', ns):
        protocol = find_text(element, 'gmd:protocol/gco:CharacterString', ns)
        if protocol == "WWW:LINK-1.0-http--link":
            detail_url = find_text(element, 'gmd:linkage/gmd:URL', ns)
            if detail_url is not None:
                break

    return detail_url


def csw_collect_records(url, ns=None, maxRecords=1000, maxNumberOfRequests=1000, memcached_client=None, cache=0, verbose=False):
    records = []

    default_params = {
        "request": "GetRecords",
        "service": "CSW",
        "version": "2.0.2",
        "resultType": "results",
        "maxRecords": maxRecords,
        "elementsetname": "full",
        "typenames": "csw:Record",
        "outputschema": "http://www.opengis.net/cat/csw/2.0.2"
    }

    numberOfRequests = 0
    startposition = 1
    while True:

        numberOfRequests = numberOfRequests + 1
        if numberOfRequests > maxNumberOfRequests:
            break

        params = {}
        params.update(default_params)
        params.update({"startposition": startposition})
        if verbose:
            print "Request: ", numberOfRequests

        memcached_key = None
        response_catalog_text = None
        if cache and (memcached_client is not None):
            memcached_key = hashlib.md5(url+"/"+str(startposition)).hexdigest()
            response_catalog_text = memcached_client.get(memcached_key)

        if response_catalog_text is None:
            response_catalog = requests.get(url, params=params)
            if response_catalog.status_code == 200:
                try:
                    response_catalog_text = response_catalog.text.encode('utf-8')
                except Exception as err:
                    response_catalog_text = None
                    print err
                    print "Response Text:", response_catalog.text
                    break
            else:
                print "Status Code:", response_catalog.status_code
                break

            if response_catalog_text:
                if cache and (memcached_client is not None):
                    memcached_client.set(memcached_key, response_catalog_text)

        if response_catalog_text:
            root = None
            try:
                root = et.fromstring(response_catalog_text)
            except Exception as err:
                print err
                print "Response Text:", response_catalog.text
                root = None

            if root is not None:
                searchResults = find_deep(root, "csw:SearchResults", ns)
                if searchResults is not None:
                    startposition = int(searchResults.attrib.get("nextRecord", 0))
                    records = records + findall_deep(searchResults, 'csw:Record', ns)
                    if startposition == 0:
                        break
                else:
                    break
            else:
                break

        else:
            break

    return records
