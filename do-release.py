import datetime
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
HTML_DIR = os.path.join(CWD, 'html')


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

    version = '3.17.0'
    publication_date = '2025-08-09'
    overwrite = True

    # Fails if the date format isn't in ISO
    date = datetime.date.fromisoformat(publication_date)

    version = version.strip()  # to remove any whitespace.

    release_dir = os.path.join(RELEASES_DIR, version)
    if not os.path.exists(release_dir):
        os.makedirs(release_dir)

    target_datacite = os.path.join(release_dir, 'datacite.json')
    target_index_html = os.path.join(HTML_DIR, 'index.html')
    target_release_html = os.path.join(HTML_DIR, f'{version}.html')

    # we have the same kinds of variable names across files and it's not a
    # problem to have keys here that aren't used by a given template.
    template_data = {
        'versions': get_versions_and_dates() + [
            {'version': version, 'date': publication_date}],
        'version': version,
        'year': str(date.year),
        'date': date.strftime('%Y-%m-%d'),
    }

    # template, target
    files_to_process = [
            ('datacite.json.template', target_datacite),
            ('index.html.template', target_index_html),
            ('release.html.template', target_release_html),
    ]
    for template_file, target_file in files_to_process:
        LOGGER.info(f'Rendering template to {target_file}')
        template_file = os.path.join(TEMPLATES_DIR, template_file)
        with open(target_file, 'w') as target_fp:
            target_fp.write(render_jinja(template_file, template_data))


if __name__ == '__main__':
    main(sys.argv)
