"""Render a release json file given a context.

To install dependencies:
    $ pip install -r requirements.txt

Example usage:
    $ python render_json.py invest-releases/3.15.1/datacite.json context.json
"""

import argparse
import json
import os

from jinja2 import Template


def render_jinja(source_file: str, context: dict):
    """Render a templated Jinja file given a dictionary.

    The rendered file is printed to stdout.

    Args:
        source_file (str): The filepath to a file that includes jinja2 template
            strings.
        context (dict): A dictionary of keys mapping to values, where the keys
            are used in the source file template.

    Returns:
        ``None``
    """
    with open(source_file) as source_fp:
        template = Template(source_fp.read())
        print(template.render(context))


def main(args=None):
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Render a templated file based on defined attributes."
    )
    parser.add_argument('--variable', nargs='*', help=(
        'A variable name and its value to be passed in to the template. '
        'This can be provided multiple times. '
        'For example, "--variable key:value year:2025" '
        'No parsing is performed on the variable values.'
    ))
    parser.add_argument('--variable-json', nargs='?', help=(
        'The path to a JSON file representing a dict.  Top-level keys '
        'will be read as the variable names mapping to their values. '
    ))
    parser.add_argument('--template-file', required=True, help=(
        'The path to the Jinja2 template file to use.'))

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

    return args.template_file, variables


if __name__ == '__main__':
    template_file, variables = main()
    render_jinja(template_file, variables)
