import json
import os
import pprint

import staticjinja

if __name__ == '__main__':
    global_context = json.load(open('context.json'))
    version_pages = [
        ('index.html', global_context),
    ]
    for version in os.listdir('invest-releases'):
        version_data = json.load(open(os.path.join(
            'invest-releases', version, 'metadata.json')))
        version_pages.append(('3\.[0-9]+\.[0-9]+\.html', version_data))

    pprint.pprint(version_pages)

    site = staticjinja.Site.make_site(
        env_globals=global_context,
        contexts=version_pages,
        outpath='build',
    )
    site.render(use_reloader=True)
