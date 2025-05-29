import json
import sys

import clean_json  # from local file
import requests
import requests.exceptions

TEST = '--test' in sys.argv
PUBLISH = '--publish' in sys.argv
AUTH_DATA = json.load(open('.env.json'))

def register(datacite_json_path):
    datacite_json = clean_json.clean(json.load(open(datacite_json_path)))

    if TEST:
        endpoint = 'https://api.test.datacite.org'
        user = AUTH_DATA['datacite_test_user']
        prefix = "10.80394"
    else:
        endpoint = 'https://api.datacite.org'
        user = AUTH_DATA['datacite_user']
        prefix = "10.60793"

    # there are different prefixes associated with prod and test accounts, so
    # set it appropriately here.
    try:
        doi = datacite_json['data']['attributes']['doi']
        old_prefix, *suffixes = doi.split('/')

        # replace the prefix with our new prefix.
        datacite_json['data']['attributes']['doi'] = (
            f'{prefix}/{"/".join(suffixes)}')
        print(datacite_json['data']['attributes']['doi'])
    except KeyError:
        datacite_json['data']['attributes']['prefix'] = prefix

    if PUBLISH:
        datacite_json['data']['attributes']['event'] = "publish"

    print(json.dumps(datacite_json, indent=4, sort_keys=True))

    resp = requests.post(
        f'{endpoint}/dois',
        headers={
            'accept': 'application/vnd.api+json',
            "Content-Type": "application/json",
        },
        data=datacite_json,
        auth=tuple(user.split(':')),  # Huh, requests VERY MUCH wants a tuple
    )
    print(resp)
    try:
        resp.raise_for_status()
    except:
        print(resp.text)
        raise

    try:
        print(resp.json())
    except requests.exceptions.JSONDecodeError:
        with open('resp.html', 'w') as html:
            html.write(resp.text)


if __name__ == '__main__':
    register(sys.argv[1])
