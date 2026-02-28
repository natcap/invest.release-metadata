# TODO: Add link checking to all of the hyperlinks - ensure files exist.

import argparse
import datetime
import json
import logging
import os
import subprocess
import sys

import jinja2

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(os.path.basename(__file__))
CWD = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(CWD, 'templates')
RELEASES_DIR = os.path.join(CWD, 'invest-releases')
HTML_DIR = os.path.join(CWD, 'html')


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


def main(args=None):
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Create all files for a DOI release from templates.",
    )
    parser.add_argument(
        'version', help="The new version being released")
    parser.add_argument(
        'date', help='The release date, in the form YYYY-MM-DD')
    parser.add_argument(
        '--no-add', action='store_true', help=('Do not add new files to git'))
    parser.add_argument(
        '--no-commit', action='store_true', help="Do not commit new files to git")

    args = parser.parse_args(args)

    version = args.version.strip()
    publication_date = args.date.strip()
    add_to_git = not args.no_add
    commit_files = not args.no_commit

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
    doi = f'10.60793/natcap-invest-{version}'
    template_data = {
        'versions': get_versions_and_dates(),
        'version': version,
        'year': str(date.year),
        'date': date.strftime('%Y-%m-%d'),
        'doi': doi,
        'doi_url': f'https://doi.org/{doi}',
    }

    # don't re-add a version to the list that is already in the list.
    if version not in set(d['version'] for d in template_data['versions']):
        template_data['versions'] += [
            {'version': version, 'date': publication_date}]

    # always sort the versions
    template_data['versions'] = sorted(
        template_data['versions'], key=lambda d: d['version'])

    # tuples are (template_filename, target_filepath)
    files_to_process = [
            ('datacite.json.template', target_datacite),
            ('index.html.template', target_index_html),
            ('release.html.template', target_release_html),
    ]
    for template_file, target_file in files_to_process:
        LOGGER.info(f'Rendering template to {target_file}')
        template_file = os.path.join(TEMPLATES_DIR, template_file)

        try:
            with open(target_file, 'w') as target_fp:
                target_fp.write(render_jinja(template_file, template_data))
        except jinja2.exceptions.UndefinedError as undefined_var:
            LOGGER.exception(f"Could not find variable {undefined_var} in "
                             f"{target_file}")
            raise

        if add_to_git:
            subprocess.run(["git", "add", target_file])

        if commit_files:
            commit_msg = (
                f"[Auto] adding files for the {version} ({publication_date}) "
                "InVEST release.")
            subprocess.run(["git", "commit", "-m", commit_msg])


if __name__ == '__main__':
    main(sys.argv[1:])
