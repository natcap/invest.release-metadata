"""Rerender all HTML DOI landing pages."""

import argparse
import os

import rendering_utils

HTML_DIR = os.path.join(rendering_utils.CWD, 'html')
TEMPLATES_DIR = os.path.join(rendering_utils.CWD, 'templates')


def main():
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Rerender all html landing pages.",
    )

    _ = parser.parse_args()

    source_template = os.path.join(TEMPLATES_DIR, 'release.html.template')
    for version_data in rendering_utils.get_versions_and_dates():
        version = version_data['version']
        target_filepath = os.path.join(HTML_DIR, f'{version}.html')
        print(f"Writing HTML file {target_filepath}")
        with open(target_filepath, 'w') as target_html_file:
            target_html_file.write(
                rendering_utils.render_jinja(
                    source_template, version_data))


if __name__ == '__main__':
    main()
