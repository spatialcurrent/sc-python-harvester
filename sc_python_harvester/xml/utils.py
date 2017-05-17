# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 Spatial Current, Inc.
#
#########################################################################
"""
Contains utility functions for XML
"""


def find_deep(node, selector, ns):
    """
    recursively find node matching the xpath selector

    :param node: the input node
    :param selector: the xpath selector
    :param ns: a dict of namespaces
    :return: the matching node
    """
    result = node.find(selector, ns) if ns else node.find(selector)
    if result is not None:
        return result
    else:
        children = list(node)
        if children and len(children) > 0:
            for child in children:
                result = find_deep(child, selector, ns)
                if result is not None:
                    break
        return result


def findall_deep(node, selector, ns, depth=0, maxDepth=-1):
    """
    recursively find all nodes matching the xpath selector

    :param node: the input etree node
    :param selector: the xpath selector
    :param ns: a dict of namespaces
    :param depth: the current depth
    :param maxDepth: the maximum number of levels to navigate
    :return: a list of matching nodes
    """
    results = node.findall(selector, ns) if ns else node.findall(selector)
    if maxDepth == -1 or (depth < maxDepth):
        children = list(node)
        if children and len(children) > 0:
            for child in children:
                results = results + findall_deep(child, selector, ns, depth+1, maxDepth)
    return results


def find_text(node, selector, ns, encoding=None, fallback=None):
    """
    returns the text content of the node recursively matching the xpath selector

    :param node: the input etree node
    :param selector: the xpath selector
    :param ns: a dict of namespaces
    :param encoding: if match found, then encode with encoding
    :param fallback: if no match found, then return fallback
    :return: the text of the matching node
    """
    element = find_deep(node, selector, ns)
    if element is not None:
        text = element.text
        if text is not None:
            text = text.strip()
            if encoding is not None:
                return text.encode(encoding)  # 'utf-8'
            else:
                return text
        else:
            return text
    else:
        return fallback


def find_float(node, selector, ns, fallback=None):
    """
    returns float representation of the text content of the node recursively matching the xpath selector

    :param node: the input etree node
    :param selector: the xpath selector
    :param ns: a dict of namespaces
    :param fallback: if no match found, then return fallback
    :return: the float representation of the matching node
    """
    element = find_deep(node, selector, ns)
    if element is not None:

        value = None

        try:
            value = float(element.text)
        except:
            value = None

        if value:
            return value
        else:
            return fallback

    else:
        return fallback


def find_array(node, selector, ns=None, fallback=None):
    """
    returns list of text contents of the nodes recursively matching the xpath selector

    :param node: the input etree node
    :param selector: the xpath selector
    :param ns: a dict of namespaces
    :param fallback: if no matches found, then return fallback
    :return: the list of text contents of the matching nodes
    """
    elements = findall_deep(node, selector, ns)
    if len(elements) > 0:
        return [x.text for x in elements]
    else:
        return fallback
