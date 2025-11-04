import argparse
import json
import os

import requests
import requests.exceptions

HEADERS = {
    'accept': 'application/vnd.api+json',
    "content-type": "application/json",
}


def clean(data: dict):
    """Strip out JSON keys that start with _.

    Args:
        data (dict): A dict loaded from a JSON file.

    Returns:
        A dict with any keys that start with ``'_'`` removed.
    """
    if isinstance(data, (str, int, float)):
        return data
    elif isinstance(data, list):
        return [clean(item) for item in data]
    elif isinstance(data, dict):
        return dict(
            (k, clean(v)) for (k, v) in data.items()
            if not k.startswith('_'))
    else:
        raise ValueError(
            f"Don't know how to sanitize {type(data)}")


def register(datacite_json_path, endpoint, auth_string, prefix, publish):
    with open(datacite_json_path) as datacite_json_fp:
        datacite_json = clean(json.load(datacite_json_fp))

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

    # Per the datacite docs, if "event": "publish" is not included, a draft
    # record will be created.  This could be updated to a findable DOI with a
    # second update to update the DOI state.  Docs link:
    # https://support.datacite.org/docs/api-create-dois#create-a-findable-doi-or-a-draft-record
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


def main(args=None):
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
            'A published DOI cannot be deleted. If this flag is not provided, '
            'a "draft" DOI (which is not findable and can be deleted) is '
            ' created. See '
            'https://support.datacite.org/docs/doi-states for information '
            "about DataCite's DOI states."
        )
    )
    parser.add_argument(
        '--auth', default=".secrets.json", help=(
            "The filepath to a json file containing usernames and passwords "
            "for authenticating into the Fabrican instance.  The JSON object "
            "in this file must have the key 'datacite_user' if accessing the "
            "production instance, and 'datacite_test_user' if accessing the "
            "test instance.  In both cases, the key must map to a value that "
            "has the form 'username:password'. If the value passed is 'ENV', "
            "the environment variables 'DATACITE_USER_PASS' and "
            "'DATACITE_TEST_USER_PASS' must be provided for access to the "
            "production and test datacite Fabrica instances, respectively. "
            "These environment variables must have the form "
            "'username:password'. Defaults to '.secrets.json'"))

    args = parser.parse_args(args)

    if args.auth == 'ENV':
        auth_data = {
            "datacite_user": os.environ.get('DATACITE_USER_PASS', ''),
            "datacite_test_user": os.environ.get(
                'DATACITE_TEST_USER_PASS', '')
        }
    else:
        with open(args.auth) as auth_json_file:
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
