"""Render a release json file given a context.

To install dependencies:
    $ pip install -r requirements.txt

Example usage:
    $ python render_json.py invest-releases/3.15.1/metadata.json
"""


import json
import sys

from jinja2 import Template

with open('context.json') as context_file:
    context = json.load(context_file)


with open(sys.argv[1]) as source_file:
    template = Template(source_file.read())
    print(template.render(context))
