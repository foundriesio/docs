#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Documentation build configuration file, created by
# sphinx-quickstart on Fri Feb  3 17:13:51 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# Configuration values that are commented out serve to show the
# default.

import json
import os
import subprocess
import sys

from os.path import abspath, dirname, join
from urllib.request import urlopen

# -- Foundries.io configuration -------------------------------------------

# The next-to-be released subscriber version number.
#
# WARNING: you must run a clean build if you change this variable!
#
# sphinx-build cannot detect the dependency change, and using its -D
# option to override would only take effect after this file is
# loaded. That's too late to have any effect on |version| and |release|.
mp_version = os.environ.get('MP_UPDATE_VERSION')
lmp_build = os.environ.get('LMP_BUILD')
if mp_version is None:
    try:
        git_version = subprocess.check_output(['git', 'describe', '--tags'])
    except subprocess.CalledProcessError:
        print('Error: no MP_UPDATE_VERSION and not in git.',
              file=sys.stderr)
        print('Refusing to guess the subscriber version.',
              file=sys.stderr)
        sys.exit(1)
    enc = sys.getdefaultencoding()
    try:
        mp_version = 'git-' + git_version.decode(enc).strip()
    except UnicodeDecodeError:
        print("Error: Can't decode git version", git_version, 'with encoding',
              enc, file=sys.stderr)
        sys.exit(1)

if lmp_build is None:
    with urlopen('https://api.foundries.io/updates/') as resp:
        latest = json.loads(resp.read().decode())['data'][0]
        for product in latest['products']:
            if product['name'] == 'lmp':
                lmp_build = product['build']
                break
        else:
            sys.exit('Unable to find latest ZMP and LMP builds')

print('LMP build number is %s' % lmp_build)

# Tags to append to the subscriber version (alpha, beta, etc.), if any.
# (This doesn't affect links to artifacts.)
mp_tags = ''

# -- General configuration ------------------------------------------------

# Derive the subscriber tags to use for this build from the
# corresponding version information.
if mp_version.startswith('git-'):
    docker_tag = 'latest'
else:
    docker_tag = mp_version

# Provide Git tags for the same information. (This can produce
# somewhat strange command lines for development builds, like cloning
# a repository and checking out master, but it works for subscriber
# updates.)
if mp_version.startswith('git-'):
    git_tag = 'master'
else:
    git_tag = 'mp-' + mp_version + mp_tags

# And likewise for repo and west manifests (which have a different tag
# namespace than the project tags, that happens to mostly match the
# docker tags.)
manifest_tag = ('refs/tags/' + docker_tag if docker_tag != 'latest'
                else 'refs/heads/master')

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
parent_dir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, join(parent_dir, 'extensions'))

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.ifconfig',
    'sphinx.ext.todo',
    'sphinxcontrib.contentui',
    'lmp_sphinx_ext',
    'sphinxemoji.sphinxemoji',
    'sphinx_tabs.tabs',
]

sphinx_tabs_valid_builders = ['linkcheck']

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'


# Links that shouldn't get checked for validity
linkcheck_ignore = [
    r'http://localhost:\d+/?',
    'http://YOUR_DEVICE_IP:8080',
    'http://YOUR_WORKSTATION_IP:8000',
    'http://.*[.]local',
    'http://your-device-ip-address/',
    'https://app.atsgarage.com/#/.*',        # requires login
    # This site is causing false negatives:
    r'https://elinux.org/.*',
    r'https://blogs.msdn.microsoft.com/.*',  # temporary blacklist
    r'https://www.tcpdump.org/.*',           # ditto
    r'https://www.wireshark.org/.*',         # ddos protection
    r'https://redbear.cc/product/ble-nano-kit-2.html',  # before deprecating
    r'https://mgmt.foundries.io/leshan/#/clients',  # I have no idea, it works
    r'https://github.com/foundriesio/lmp-manifest/releases/download/.*',  # Release artifacts done show up until *after* this runs
    'https://mgmt.foundries.io/leshan/#/security',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'FoundriesFactory<sup>&#174;</sup>'
copyright = '2017-2020, Foundries.io, Ltd'
author = 'Foundries.io, Ltd.'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = mp_version
# The full version, including alpha/beta/rc tags.
release = mp_version + mp_tags

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# Standard epilog to be included in all files.
rst_epilog = '''
.. |docker_tag| replace:: {}
.. |git_tag| replace:: {}
.. |manifest_tag| replace:: {}
'''.format(docker_tag, git_tag, manifest_tag)

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

#def setup(app):
#    app.add_stylesheet('theme_overrides.css')
html_css_files = [
    'theme_overrides.css'
] 

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'h', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'r', 'sv', 'tr'
#html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
#html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
#html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = 'fiodoc'

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}
