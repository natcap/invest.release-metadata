"""Render a release json file given a context.

To install dependencies:
    $ pip install -r requirements.txt

Example usage:
    $ python render_json.py invest-releases/3.15.1/datacite.json context.json
"""

import argparse
import json
import os
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


# Need way to provide extra context attributes
# --context=year:2025
# --context=version:3.16.3
# --context=prefix:10.2139487o3241

def main(args=None):
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Render a templated file based on defined attributes."
    )
    parser.add_argument('--variable', nargs='*', help=(
        'A variable name and its value to be passed in to the template. '
        'This can be provided multiple times. '
        'For example, --variable=key:value --variable=year:2025. '
        'No parsing is performed on the variable values.'
    ))
    parser.add_argument('--variable-json', nargs='?', help=(
        'The path to a JSON file representing a dict.  Top-level keys '
        'will be read as the variable names mapping to their values. '
    ))

    args = parser.parse_args(args)

    variables = {}
    if args.variable_json is not None:
        with open(args.variable_json) as variable_json:
            json_data = json.load(variable_json)
        if not isinstance(json_data, dict):
            raise ValueError(
                f'The variable JSON file at {args.variable_json} must be a '
                f'dict, not {type(json_data)}')
        variables.update(json_data)

    for variable in args.variable:
        var_name, var_value = variable.split(':')
        if var_name in variables:
            raise ValueError(
                f'The variable {var_name} is defined twice between CLI args '
                'and the JSON file (if provided).')
        variables[var_name] = var_value



if __name__ == '__main__':
    render_with_context(sys.argv[1], sys.argv[2])

# templated datacite JSON --> rendered datacite JSON --> rendered HTML
#                             (needed by itself)
#
# Templated datacite would have variables:
#   * version
#   * year
#   * DOI prefix
#
# My hope is to use this script here to render a JINJA templated file given a
# JSON file, including any nesting needed.
