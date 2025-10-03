import argparse
import json
import os
import sys

import clean_json  # from local file
import requests
import requests.exceptions

HEADERS = {
    'accept': 'application/vnd.api+json',
    "content-type": "application/json",
}


def register(datacite_json_path, endpoint, auth_string, prefix, publish):
    datacite_json = clean_json.clean(json.load(open(datacite_json_path)))

    auth = tuple(auth_string.split(':'))  # Hub, requests DEMANDS a tuple

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

    if publish:
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


def main():
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Create, update and/or publish a DOI",
    )
    parser.add_argument(
        'datacite_json', help="The filepath of a datacite JSON file.")
    parser.add_argument(
        '--test', action='store_true', help=(
            'Whether to create/update the DOI on the Fabrica test instance. '
            'If omitted, the production Fabrica instance will be used.'))
    parser.add_argument(
        '--publish', action='store_true', help=(
            'Whether to publish the DOI on the target datacite instance. '
            'Using --publish will make the DOI findable and permanent. '
            'A published DOI cannot be deleted.  See '
            'https://support.datacite.org/docs/doi-states for information '
            "about DataCite's DOI states."
        )
    )
    parser.add_argument(
        '--auth-json', default=".env.json", help=(
            "The filepath to a json file containing usernames and passwords "
            "for authenticating into the Fabrican instance.  The JSON object "
            "in this file must have the key 'datacite_user' if accessing the "
            "production instance, and 'datacite_test_user' if accessing the "
            "test instance.  In both cases, the key must map to a value that "
            "has the form 'username:password'. Defaults to '.env.json'"))

    args = parser.parse_args()

    with open(args.auth_json) as auth_json_file:
        auth_data = json.load(auth_json_file)

    if args.test:
        endpoint = 'https://api.test.datacite.org'
        auth_string = auth_data['datacite_test_user']
        prefix = "10.80394"
    else:
        endpoint = 'https://api.datacite.org'
        auth_string = auth_data['datacite_user']
        prefix = "10.60793"

    return (args.datacite_json, endpoint, auth_string, prefix, args.publish)


if __name__ == '__main__':
    datacite_json, endpoint, user, prefix, publish = main()
    register(datacite_json, endpoint, user, prefix, publish)
