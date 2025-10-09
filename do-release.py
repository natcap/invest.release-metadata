import json
import logging
import os

logging.basicConfig(level=logging.WARNING)
LOGGER = logging.getLogger(level=logging.INFO)

# Always write out the non-test DOI prefix.
# Create new datacite file (only overwrite with --overwrite)
# Create new html file from datacite file
# Recreate index file based on datacite files

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
