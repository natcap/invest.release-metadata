# invest.release-metadata
Metadata for InVEST release artifacts, for use in DOIs and artifact repositories.

Per the [DataCite documentation](https://support.datacite.org/docs/landing-pages),
DOIs should resolve to a landing page that contains

1. metadata related to the release (including the DOI itself)
2. links to the various assets related to the release

Furthermore, the DataCite API has a whole lot of information that can be
attached to the DOI (see https://datacite-metadata-schema.readthedocs.io/en/4.6/properties/ for
the full list of properties).  Some of these attributes are required, but many
are not, and there is _so_ much information that would be great to include in
this metadata, including individuals, institutions, funding sources, and how
these are added to over time, including persistent identifiers for as many
entities as possible.  Increasingly, these persistent identifiers are useful
for indexes that link entities, allowing for easier identification of the
impact of NatCap, our software, and our networks.

## So here's the plan

Our first release of DOIs for InVEST will leave binary artifacts where they
are, stored on google cloud.  We will create a landing page for each InVEST release,
served by GitHub Pages, that contains any relevant metadata.  Metadata will be stored
in json files in release-specific directories.  For example, for the 3.15.0 release:

```text
/invest-releases
    /3.15.0
        artifacts.json  # track URIs to the source artifacts on the internet
        metadata.json   # track metadata for consumption by the DataCite API.
                        # This need not be 100% compliant with the DataCite API,
                        # but we will need to translate it to DataCite at some point.
```

All DataCite metadata can be updated after it is created.  That means we can
update attributes and entities as needed, and it also means we can move our
release assets elsewhere (e.g. Zenodo or the Stanford Digital Repository)
and just update the page that the DOI resolves to.

The initial idea is to create initial metadata for the 3.15.0 release and
extend this for the forthcoming InVEST 3.16.0 release.

## Later on

* Build metadata pages for all 150+ InVEST releases and flesh them out with
  appropriate details of people, institutions and grants involved.
