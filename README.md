# docs
microPlatform documentation source for https://docs.foundries.io

## Requirements

In order to build documentation at a minimum we require that both python3 and
pip for python3 are installed.  All of the required python modules are
described in the requirements.txt file in this directory and can be installed
with the command ```pip install -r requirements.txt```.

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

### Using `virtualenv` to provide requirements

The recommended way to build documentation, in order to avoid messing with
the global system-wide package storage, is to use `virtualenv` to set up 
the necessary environment for sphinx packages:

```bash
$ sudo apt-get install python3 python3-virtualenv
$ virtualenv -p /usr/bin/python3 venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt
```

## Build the docs

To build html docs from rst files just run:

```bash
$ make html
```

And open with `build/html/index.html` in your browser.
