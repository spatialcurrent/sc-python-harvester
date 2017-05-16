import hashlib
import requests

try:
    from flask import json
except ImportError:
    import json

def geonode_collect_profiles(url, memcached_client=None, cache=0):
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
                #response_catalog_text = response_catalog.text.encode('utf-8')
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
                #response_catalogtext = response_catalog.text.encode('utf-8')
                #response_text = response_catalog.json()
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
