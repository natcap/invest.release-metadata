import json
import logging
import os

import jinja2

LOGGER = logging.getLogger(__name__)

CWD = os.path.dirname(__file__)
RELEASES_DIR = os.path.join(CWD, 'invest-releases')

def get_versions_and_dates():
    version_data = []
    for release_dir in os.listdir(RELEASES_DIR):
        datacite_file = os.path.join(
            RELEASES_DIR, release_dir, 'datacite.json')
        LOGGER.info(f"Trying to process datacite file {datacite_file}")
        try:
            with open(datacite_file) as datacite_fp:
                datacite_json = json.load(datacite_fp)['data']['attributes']
        except FileNotFoundError:
            LOGGER.info(f"Didn't find {datacite_file} inside {release_dir}; skipping")
            continue

        data = {}
        try:
            data['version'] = datacite_json['version']
        except KeyError:
            LOGGER.warning(
                f'version attribute missing from {release_dir}/datacite.json')
            data['version'] = release_dir

        data['date'] = datacite_json['dates']['date']
        data['year'] = datacite_json['publicationYear']
        data['doi'] = datacite_json['doi']
        data['doi_url'] = f'https://doi.org/{data["doi"]}'

        version_data.append(data)
    return version_data


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
    environment = jinja2.Environment(undefined=jinja2.StrictUndefined)
    with open(source_file) as source_fp:
        template = environment.from_string(source_fp.read())
    rendered_text = template.render(context)
    return rendered_text
