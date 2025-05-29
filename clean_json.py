import json
import pprint
import sys


def clean(data):
    if isinstance(data, (str, int, float)):
        return data
    elif isinstance(data, list):
        return [clean(item) for item in data]
    elif isinstance(data, dict):
        return dict(
            (k, clean(v)) for (k, v) in data.items()
            if not k.startswith('_'))
    else:
        raise ValueError(
            f"Don't know how to sanitize {type(data)}")


if __name__ == '__main__':
    with open(sys.argv[1]) as dirty_json_file:
        dirty_json = json.load(dirty_json_file)
        pprint.pprint(clean(dirty_json))
