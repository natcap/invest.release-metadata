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

## How to Create DOIs with This Tooling

### Option 1: Use GHA

Visit https://github.com/natcap/invest.release-metadata/actions/workflows/invest-release.yml
and run the `workflow_dispatch` trigger.

### Option 2: Use These Local Files

Both scripts have `argparse` interfaces, so feel free to use `--help` to better
understand the CLI options available to you.
```shell
python do-release.py <version> <release-date>
python register-doi.py <version>


# Overall Idea

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


## Notes w/r/t the DataCite Metadata Properties

For all InVEST versions, we assume the following information (expanded to meet
the necessary specificity needed for actual DataCite submission):

    * Required Properties:
      * Identifier: this is the DataCite DOI
      * Creator: the Natural Capital Project (the legal partner institutions, if needed)
      * Title: "InVEST: Integrated Valuation of Ecosystem Services and Tradeoffs"
      * Publisher: GitHub (probably)
      * PublicationYear: <year of publication>
      * ResourceType: software (or appropriate equivalent)
    * Recommended and Optional Properties:
      * Subject: Ecosystem Services or some other phrase(s)/classifications, etc. describing InVEST and linking to other schemes
      * Contributor: A list of contributors to this version of InVEST
      * Date: The release date of the software.  Additional dates related to the release can also be described, but are probably not needed for InVEST.
      * Language: EN until we added ES and ZH support.
        * NOTE: only 1 language is allowed (primary language)
        * Unclear how to add additional languages at this time.
      * AlternateIdentifier: unused until we have something to put here.
      * RelatedIdentifier: unused until we have DOIs of related resources to link to.  Maybe papers that describe models?
      * Size: unused unless this is the only place we can define the size of items.
      * Format: The MIME type of different binaries for the release
      * Version: The version number for the release
      * Rights: The license string summarizing the license
      * Description: Any additional information that doesn't fit into any other categories.

An example of the DataCite API object is here: https://api.datacite.org/dois/10.5438/0014

And exmaple that uses the json api and that is in the datacite api docs:
https://datacite-metadata-schema.readthedocs.io/en/4.5/guidance/related-item-guide/#example-journal-article-in-a-journal-with-an-issn
