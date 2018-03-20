__AUTHOR__ = "Tony"

"""
Example usage:

>>> json_loads_byteified('{"Hello": "World"}')
{'Hello': 'World'}
>>> json_loads_byteified('"I am a top-level string"')
'I am a top-level string'
>>> json_loads_byteified('7')
7
>>> json_loads_byteified('["I am inside a list"]')
['I am inside a list']
>>> json_loads_byteified('[[[[[[[["I am inside a big nest of lists"]]]]]]]]')
[[[[[[[['I am inside a big nest of lists']]]]]]]]
>>> json_loads_byteified('{"foo": "bar", "things": [7, {"qux": "baz", "moo": {"cow": ["milk"]}}]}')
{'things': [7, {'qux': 'baz', 'moo': {'cow': ['milk']}}], 'foo': 'bar'}
>>> json_load_byteified(open('somefile.json'))
{'more json': 'from a file'}

How does this work and why would I use it?

Mark Amery's function is shorter and clearer than these ones, so what's the point of them? Why would you want to use them?

Purely for performance. Mark's answer decodes the JSON text fully first with unicode strings, then recurses through the entire decoded value to convert all strings to byte strings. This has a couple of undesirable effects:

    A copy of the entire decoded structure gets created in memory
    If your JSON object is really deeply nested (500 levels or more) then you'll hit Python's maximum recursion depth

"""

import json


def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )


def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )


def _byteify(data, ignore_dicts=False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data
