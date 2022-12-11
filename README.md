# Docs

This repo contains the documentation source for: <https://docs.foundries.io>

## About

Currently the docs are written in
[reStucturedText](https://docutils.sourceforge.io/rst.html) with
[Sphinx](https://www.sphinx-doc.org/en/master/) serving as the site generator.

## Requirements

Before beginning any work, be sure to review [CONTRIBUTING.md](CONTRIBUTING.md).

In order to build documentation, at minimum both python3 and pip for python3 are
required. All required python modules are described in ```requirements.txt``` in this
directory and can be installed with```pip install -r requirements.txt```.

The following is the list of packages needed (can be incomplete):

| Package                 |
| ----------------------- |
| sphinx                  |
| sphinx-rtd-theme        |
| sphinx-tabs             |
| sphinxemoji             |
| sphinx_copybutton       |
| sphinxcontrib.asciinema |
| sphinxcontrib-contentui |
| sphinx_toolbox          |
| sphinx-prompt           |
| myst-parser             |

### Using virtualenv to Provide Requirements

The recommended way to build documentation (in order to avoid messing with
global system-wide package storage) is to use `virtualenv` to set up the
necessary environment for sphinx packages:

```bash

$ sudo apt-get install python3
$ python -m venv venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt

```

## Building the Docs Locally

To build html from rst files run from the top directory:

```bash

$ make html

```

you can then open `build/html/index.html` in your browser to view the
documentation.
