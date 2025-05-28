import json
import pprint
import sys


def _clean(data):
    if isinstance(data, str):
        return data
    elif isinstance(data, list):
        return [_clean(item) for item in data]
    elif isinstance(data, dict):
        return dict(
            (k, _clean(v)) for (k, v) in data.items()
            if not k.startswith('_'))
    else:
        raise ValueError(
            f"Don't know how to sanitize {type(data)}")

with open(sys.argv[1]) as dirty_json_file:
    dirty_json = json.load(dirty_json_file)
    pprint.pprint(_clean(dirty_json))
