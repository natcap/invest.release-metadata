import json
import logging
import os
import sys

from jinja2 import Template

logging.basicConfig(level=logging.WARNING)
LOGGER = logging.getLogger(level=logging.INFO)
CWD = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(CWD, 'templates')
RELEASES_DIR = os.path.join(CWD, 'invest-releases')


def get_versions_and_dates():
    version_data = []
    for release_dir in os.listdir(RELEASES_DIR):
        datacite_file = os.path.join(
            RELEASES_DIR, release_dir, 'datacite.json')
        with open(datacite_file) as datacite_fp:
            datacite_json = json.load(datacite_fp)['data']['attributes']

        data = {}
        try:
            data['version'] = datacite_json['version']
        except KeyError:
            LOGGER.warning(
                f'version attribute missing from {release_dir}/datacite.json')
            data['version'] = release_dir

        data['date'] = datacite_json['dates']['date']

        version_data.append(data)


def render_jinja(source_file: str, context: dict):
    """Render a templated Jinja file given a dictionary.

    The rendered file is printed to stdout.

    Args:
        source_file (str): The filepath to a file that includes jinja2 template
            strings.
        context (dict): A dictionary of keys mapping to values, where the keys
            are used in the source file template.

    Returns:
        ``rendered_text``, a string.
    """
    with open(source_file) as source_fp:
        template = Template(source_fp.read())
    rendered_text = template.render(context)
    return rendered_text


def main(args=None):
    # Args: version
    # Args: publication date (ISO)
    # Args: --overwrite

    # Write new datacite file
    # Write new index file
    # Write new release html file

    pass


if __name__ == '__main__':
    main(sys.argv)
