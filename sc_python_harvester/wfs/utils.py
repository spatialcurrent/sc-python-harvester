# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 Spatial Current, Inc.
#
#########################################################################
"""
Contains utility functions for WFS
"""


import hashlib
import requests

try:
    from flask import json
except ImportError:
    import json

def wfs_describe_layer(url, typename, ns=None, memcached_client=None, cache=0):
    """
    call DescribeFeatureType on a layer and return attributes and geometry type

    :param url: the WFS url, e.g., .../geoserver/wfs
    :param typename: the layer typename
    :param ns: a dict of namespaces
    :param memcached_client: pymemcache client for caching http response
    :param cache: cache results
    :return: a tulple of (attributes, geometry_type)
    """
    attributes = None
    geometry_type = None

    default_params = {
        "version": "1.0.0",
        "service": "WFS",
        "request": "DescribeFeatureType",
    }

    if url is not None:

        memcached_key = None
        response_text = None
        if cache and (memcached_client is not None):
            memcached_key = hashlib.md5(url+"/DescribeFeatureType/"+typename).hexdigest()
            response_text = memcached_client.get(memcached_key)

        if response_text is None:
            params = {}
            params.update(default_params)
            params.update({"typename": typename})
            response = requests.get(url, params=params)

            if response.status_code == 200:
                try:
                    response_text = response.text.encode('utf-8')
                except Exception as err:
                    response_text = None
                    print err
                    print "Response Text:", response.text

                if response_text:
                    if cache and (memcached_client is not None):
                        memcached_client.set(memcached_key, response_text)
            else:
                print "Status Code:", response.status_code

        if response_text is not None:
            root = None
            try:
                root = et.fromstring(response_text)
            except Exception as err:
                print err
                print "Response Text:", response_text
                root = None

            if root is not None:
                seq = find_deep(root, "xsd:complexType/xsd:complexContent/xsd:extension/xsd:sequence", ns)
                if seq is not None:
                    elements = findall_deep(seq, 'xsd:element', ns)
                    if len(elements) > 0:
                        attributes = []
                        for element in elements:
                            attribute_name = element.attrib.get("name", "")
                            attribute_type = element.attrib.get("type", "")
                            if len(attribute_name) > 0 and len(attribute_type) > 0:
                                if attribute_name in ["geom", "the_geom"]:
                                     m = re.compile("gml[:](.+)PropertyType", flags=re.IGNORECASE).match(attribute_type)
                                     if m is not None:
                                         geometry_type = m.group(1).upper()
                                else:
                                    m = re.compile("xsd[:](.+)", flags=re.IGNORECASE).match(attribute_type)
                                    if m is not None:
                                        attributes.append({"id": attribute_name, "title": attribute_name, "type": m.group(1).lower()})
                                    else:
                                        attributes.append({"id": attribute_name, "title": attribute_name, "type": attribute_type})


    return attributes, geometry_type
