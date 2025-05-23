"""Render a release json file given a context.

To install dependencies:
    $ pip install -r requirements.txt

Example usage:
    $ python render_json.py invest-releases/3.15.1/metadata.json context.json
"""


import json
import sys

from jinja2 import Template


def render_with_context(source_json, context_json):
    """Render a source json file given a context.

    The rendered file is printed to stdout.

    Args:
        source_json (str): The filepath to a json file that has jinja2 template
            strings given keys in the context file.
        context_json (str): The filepath to a json file that has the context
            needed to be able to render the source_json file.

    Returns:
        ``None``
    """
    with open(context_json) as context_file:
        context = json.load(context_file)


    with open(source_json) as source_file:
        template = Template(source_file.read())
        print(template.render(context))


if __name__ == '__main__':
    render_with_context(sys.argv[1], sys.argv[2])
