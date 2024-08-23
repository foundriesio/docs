# Docs

This repo contains the documentation source for: <https://docs.foundries.io>

## About

Currently the docs are written in
[reStucturedText](https://docutils.sourceforge.io/rst.html) with
[Sphinx](https://www.sphinx-doc.org/en/master/) serving as the site generator.

## Requirements

Before beginning any work, review the [contributing section](#contributing).

To build the documentation, python3 and `pip3` are required.
All required python modules are listed in `requirements.txt`.
Install them with `pip3 install -r requirements.txt`.

📌 **NOTE:** After run `pip3 install -r requirements.txt`, restart your terminal or use source to ensure Sphinx is set up.

### Using Virtualenv to Provide Requirements

To avoid messing with your system-wide package storage, use `virtualenv`.
This will set up the necessary environment for sphinx packages and place them here:

```bash

$ sudo apt-get install graphviz python3 python3-virtualenv
$ virtualenv -p /usr/bin/python3 venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt

```

## Building the Docs Locally

To build the html from rst files, from the top directory run:

```bash

$ make html

```

📌 **NOTE:** When you fork this project, make sure to disable the option that allows forking of only the main branch. 
If you overlook this step, you may encounter issues when executing the make html command, as you will be required to 
specify the value via the environment variables `MP_UPDATE_VERSION`.

You can then open `build/html/index.html` in your browser to view the
documentation.

## Contributing

### Before Working on Documentation

While optional, before you begin working:

- [ ] Check Jira

> See if someone is working on it.
If there is no open issue, should there be?
If the fix is going to take more than 30 minutes, consider opening one.

- [ ] Check the default branch to see the if the issue is still relevant.

> The published pages reflect the documentation as of the latest release.
The change may exist and will show up in the next release.

You **must** use a fork rather than working on a `foundriesio/docs` branch.
Branch names should be descriptive and in the imperative (what you *will* do):

```bash
git checkout -b spell-check-everything
```

### Working on Documentation

For new pages, first look for an appropriate template under `templates/`

Use spelling and grammar checks and ask a technical writer if you have questions.
Consult the [style guide](https://foundriesio.atlassian.net/wiki/spaces/ID/pages/2392067/Foundries.io+Style+and+Communication+Guide).

You can also "lint" the document, though this will also be done as a GitHub action upon opening a Pull Request (PR).
[Install vale](https://vale.sh/docs/vale-cli/installation/), and from this directory run:

```bash
vale sync
vale <PATH/FILE>
```

:exclamation: make sure you are using Vale 2.16.0 or greater

Before pushing, check locally:

- links; `make linkcheck`
- html; `make html`
- lint: `vale <path_to_file(s)>`

When opening a PR, add "documentation team" for your reviewer.
For any changes that reflect changes to how the FoundriesFactory™ Platform is used/interacted with—the majority—please add the Customer Success team.
Someone from the documentation team will merge it once reviews are in and suggestions considered.
The [PR template](.github/pull_request_template.md) has additional steps that can speed up the process.

