def find_deep(node, selector, ns):
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
    results = node.findall(selector, ns) if ns else node.findall(selector)
    if maxDepth == -1 or (depth < maxDepth):
        children = list(node)
        if children and len(children) > 0:
            for child in children:
                results = results + findall_deep(child, selector, ns, depth+1, maxDepth)
    return results


def find_text(node, selector, ns, encoding=None, fallback=None):
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
    elements = findall_deep(node, selector, ns)
    if len(elements) > 0:
        return [x.text for x in elements]
    else:
        return fallback
