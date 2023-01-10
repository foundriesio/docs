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
Install them with `pip install -r requirements.txt`.

### Using Virtualenv to Provide Requirements

To avoid messing with your system-wide package storage, use `virtualenv`. 
This will set up the necessary environment for sphinx packages and place them here:

```bash

$ sudo apt-get install python3 python3-virtualenv
$ virtualenv -p /usr/bin/python3 venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt

```

## Building the Docs Locally

To build the html from rst files, from the top directory run:

```bash

$ make html

```

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

Try to use a fork rather than working on a `foundriesio/docs` branch.
If on a direct branch, include your username.
Branch names should be descriptive and in the imperative (what you *will* do):

```bash
# If working on a branch of foundriesio/docs:
`git checkout -b kprosise/update-contributing-doc

# or for a fork:
git checkout -b spell-check-everything
```

### Working on Documentation

For new pages, templates for tutorials, user guides, and reference manual pages are in `templates/`

Use spelling and grammar checks and ask a technical writer if you have questions.
Consult the [style guide](https://foundriesio.atlassian.net/wiki/spaces/ID/pages/2392067/Foundries.io+Style+and+Communication+Guide).

You can also "lint" the document.
[Install vale](https://vale.sh/docs/vale-cli/installation/), and from this directory run:

```bash
vale sync
vale <PATH/FILE>
```

Alternatively, after installing vale, you can use make.
To check all docs, run `make lint-all`.
To check files changed since the last commit, use `make lint-diff`.

Before pushing, check locally:

* links; `make linkcheck` 
* html; `make html`
* style; `make lint-diff`

When opening a PR, tag a technical writer.
They will merge it once reviews are in and suggestions considered.
The [PR template](.github/pull_request_template.md) has additional steps. 

