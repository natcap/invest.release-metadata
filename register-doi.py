import json
import sys

import clean_json  # from local file
import requests
import requests.exceptions

TEST = '--test' in sys.argv
PUBLISH = '--publish' in sys.argv
AUTH_DATA = json.load(open('.env.json'))
HEADERS = {
    'accept': 'application/vnd.api+json',
    "content-type": "application/json",
}

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

    auth = tuple(user.split(':'))  # Hub, requests DEMANDS a tuple

    # there are different prefixes associated with prod and test accounts, so
    # set it appropriately here.
    update = False
    try:
        doi = datacite_json['data']['attributes']['doi']

        # replace the prefix with our new prefix.
        old_prefix, *suffixes = doi.split('/')
        doi = f'{prefix}/{"/".join(suffixes)}'
        datacite_json['data']['attributes']['doi'] = doi
        print(doi)

        # check to see if the DOI already exists; update if so
        if requests.get(f'{endpoint}/dois/{doi}', headers=HEADERS, auth=auth):
            print(f'DOI already exists: {doi}')
            update = True
    except KeyError:
        datacite_json['data']['attributes']['prefix'] = prefix

    if PUBLISH:
        datacite_json['data']['attributes']['event'] = "publish"

    print(json.dumps(datacite_json, indent=4, sort_keys=True))

    if update:
        request_method = requests.put
        endpoint = f'{endpoint}/dois/{doi}'
    else:
        request_method = requests.post
        endpoint = f'{endpoint}/dois'

    print(request_method)
    resp = request_method(
        endpoint,
        headers=HEADERS,
        json=datacite_json,
        auth=auth,
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
