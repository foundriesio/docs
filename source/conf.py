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
fioctl_version = os.environ.get('fv')
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
    with urlopen('https://api.foundries.io/projects/lmp/builds/latest/?promoted=1') as resp:
        lmp_build = json.loads(resp.read().decode())['data']['build']['build_id']

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
    'sphinx_copybutton',
    'sphinx_toolbox.confval',
    'sphinx-prompt',
    'sphinx_reredirects',
    'sphinx.ext.graphviz',
]

copybutton_prompt_text = "$ "

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
    r'https://github.com/foundriesio/fioctl/releases/download/.*',  # ditto
    'https://mgmt.foundries.io/leshan/#/security',
    'https://github.com/foundriesio/fiotest#testing-specification',
    'https://github.com/foundriesio/jobserv/blob/72935348e902cdf318cfee6ab00acccee1438a7c/jobserv/notify.py#L141-L146',
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
project = 'FoundriesFactory'
copyright = '2017-2024, Foundries.io, Ltd'
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
language = 'en'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['reference-manual/boards/*flashing.rst',
                    'reference-manual/boards/*-prepare.rst',
                    'reference-manual/boards/*note.rst',
                    'reference-manual/security/imx-generic-custom-keys.rst']

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
.. |fioctl_version| replace:: {}
'''.format(docker_tag, git_tag, manifest_tag, fioctl_version)

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.

# Note that for Sphinx-RTD v0.6.0 or newer, 'html_baseurl' is used rather
# than canonical_url
html_theme_options = {
    'logo_only': True,
    'canonical_url': 'https://docs.foundries.io/latest/'
}


# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/logo.png"

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add custom CSS files.
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

# Config for sphinx-reredirects, maps source: target, target path is relative to source.
# TODO: troubleshooting sections redirecting to lmp-customization do not appear to be functional
redirects = {
     "user-guide/cert-rotation": "rotating-cert.html",
     "reference-manual/docker/compose-apps": "../../user-guide/containers-and-docker/compose-apps.html",
     "reference-manual/docker/configure-docker-helper": "../../user-guide/containers-and-docker/configure-docker-helper.html",
     "reference-manual/docker/containers": "../../user-guide/containers-and-docker/containers.html",
     "user-guide/containers-preloading/container-preloading": "../containers-and-docker/container-preloading.html",
     "user-guide/multi-stage-container/multi-stage-container": "../containers-and-docker/multi-stage-container",
     "reference-manual/factory/team-based-access": "../../user-guide/account-management/team-based-access.html",
     "reference-manual/factory/factory-keys": "../../reference-manual/security/factory-keys.html",
     "reference-manual/security/secure-boot": "security.html#secure-boot-hardware-root-of-trust",
     "reference-manual/security/boot-software-updates": "security.html#secure-boot-firmware-updates",
     "reference-manual/security/ota-security": "security.html#secure-over-the-air-updates",
     "reference-manual/security/secure-elements/index": "../security.html#secure-element-as-secrets-storage",
     "reference-manual/troubleshooting/troubleshooting": "../../user-guide/troubleshooting/troubleshooting.html",
     "reference-manual/troubleshooting/troubleshooting#extending-user-groups": "../../user-guide/lmp-customization/lmp-customization.html#extending-user-groups",
     "reference-manual/troubleshooting/troubleshooting#adding-a-new-systemd-startup-service": "../../user-guide/lmp-customization/lmp-customization.html#adding-a-new-systemd-startup-service",
     "reference-manual/troubleshooting/troubleshooting#adding-lmp-users": "../../user-guide/lmp-customization/lmp-customization.html#adding-lmp-users#adding-lmp-users",
     "tutorials/mosquitto": "compose-app/compose-app-mosquitto-broker.html",
     "reference/zephyr": "../index.html",
     "reference/zephyr-branching": "../index.html",
     "user-guide/configure-lmp": "../user-guide/lmp-customization/lmp-customization.html",
     "tutorials/ibm": "../index.html",
     "tutorials/google": "../reference-manual/docker/private-registries.html#configuring-for-ci-google-artifact-registry-gar",
     "tutorials/cloud": "../reference-manual/docker/private-registries.html",
     "tutorials/aws": "../reference-manual/docker/private-registries.html#configuring-ci-for-aws-ecr",
     "tutorial/other-zephyr-boards.html": "../reference-manual/linux/linux-supported.html#ref-linux-supported",
     "tutorial/zephyr-branching": "../tutorials/working-with-tags/working-with-tags.html",
     "reference/vpn": "../reference-manual/remote-access/wireguard.html",
     "reference/secure-element.050.html": "../reference-manual/security/secure-elements/secure-element.050.html",
     "reference/secure-boot": "../reference-manual/security/secure-boot.html",
     "reference/offline-keys": "../reference-manual/security/offline-keys.html",
     "reference/linux": "../reference-manual/linux/linux.html",
     "reference/linux-targets": "../reference-manual/linux/linux-supported.html",
     "reference/linux-repo": "../reference-manual/linux/linux-repo.html",
     "reference/linux-persistent-log": "../reference-manual/linux/linux-persistent-log.html",
     "reference/linux-ota": "../reference-manual/linux/linux-update.html",
     "reference/linux-net-debug": "../reference-manual/linux/linux-net-debug.html",
     "reference/linux-layers": "../reference-manual/linux/linux-layers.html",
     "reference/linux-kernel": "../reference-manual/linux/linux-kernel.html",
     "reference/linux-dev-container": "../reference-manual/linux/linux-dev-container.html",
     "reference/linux-building": "../reference-manual/linux/linux-building.html",
     "reference/linux-bt-joiner": "../reference-manual/linux/linux.html",
     "reference/factory-definition": "../reference-manual/factory/factory-definition.html",
     "reference/docker-apps": "../reference-manual/docker/docker.html",
     "reference/device-testing": "../reference-manual/testing/testing.html",
     "reference/device-tags": "../reference-manual/ota/device-tags.html",
     "reference/containers": "../reference-manual/docker/containers.html",
     "reference/container-secrets": "../reference-manual/docker/container-secrets.html",
     "reference/configuration-management": "../reference-manual/ota/fioconfig.html",
     "reference/compose-apps": "../reference-manual/docker/compose-apps.html",
     "reference/app-conversion": "../reference-manual/docker/compose-apps.html",
     "reference/aktualizr-lite": "../reference-manual/ota/aktualizr-lite.html",
     "reference/advanced-tagging": "../reference-manual/ota/advanced-tagging.html",
     "reference-manual/security/secure-boot-imx6ullevk-sec.html": "secure-machines.html",
     "reference-manual/security/secure-boot-imx": "security.html",
     "reference-manual/linux/linux-targets": "linux.html",
     "reference-manual/boards/stm32mp1": "boards.html",
     "howto/zephyr-mcuboot-keys": "../index.html",
     "howto/linux-net-debug": "../reference-manual/linux/linux-net-debug.html",
     "howto/": "index.html",
     "getting-started/create-compose-app": "../tutorials/compose-app/compose-app.html",
     "customer-factory/writing-images": "../getting-started/flash-device/index.html",
     "customer-factory/updating-the-core": "../reference-manual/linux/linux-update.html",
     "customer-factory/source-code": "../tutorials/customizing-the-platform/customizing-the-platform.html",
     "customer-factory/managing": "../getting-started/register-device/index.html",
     "customer-factory/getting-started": "../getting-started/signup/index.html",
     "customer-factory/first-boot": "../getting-started/flash-device/index.html#booting-and-connecting-to-the-network",
     "customer-factory/extending": "../reference-manual/linux/linux-extending.html",
     "customer-factory/docker-apps": "../tutorials/getting-started-with-docker/getting-started-with-docker.html",
     "customer-factory/containers": "../reference-manual/docker/containers.html",
     "customer-factory/configuring": "../index.html",
     "customer-factory/": "index.html",
     "community-factory/using": "../index.html",
     "community-factory/installation": "../index.html",
     "community-factory/docker-apps": "../tutorials/getting-started-with-docker/getting-started-with-docker.html",
     "community-factory/docker-apps-k3s": "../index.html",
     "community-factory/dependencies": "../index.html",
     "community-factory/create-factory": "../getting-started/signup/index.html",
     "community-factory/": "index.html",
     "getting-started/git-config/index": "../install-fioctl/index.html#configuring-git",
     "reference-manual/linux/linux-building": "../../user-guide/lmp-customization/linux-building.html",
     "reference-manual/linux/linux-extending": "../../user-guide/lmp-customization/linux-extending.html",
      }

# Make external links open in a new tab.
# https://stackoverflow.com/questions/25583581/add-open-in-new-tab-links-in-sphinx-restructuredtext

from sphinx.writers.html import HTMLTranslator
from docutils import nodes
from docutils.nodes import Element

class PatchedHTMLTranslator(HTMLTranslator):

    def visit_reference(self, node: Element) -> None:
        atts = {'class': 'reference'}
        if node.get('internal') or 'refuri' not in node:
            atts['class'] += ' internal'
        else:
            atts['class'] += ' external'
            # ---------------------------------------------------------
            # Customize behavior (open in new tab, secure linking site)
            atts['target'] = '_blank'
            atts['rel'] = 'noopener noreferrer'
            # ---------------------------------------------------------
        if 'refuri' in node:
            atts['href'] = node['refuri'] or '#'
            if self.settings.cloak_email_addresses and atts['href'].startswith('mailto:'):
                atts['href'] = self.cloak_mailto(atts['href'])
                self.in_mailto = True
        else:
            assert 'refid' in node, \
                   'References must have "refuri" or "refid" attribute.'
            atts['href'] = '#' + node['refid']
        if not isinstance(node.parent, nodes.TextElement):
            assert len(node) == 1 and isinstance(node[0], nodes.image)
            atts['class'] += ' image-reference'
        if 'reftitle' in node:
            atts['title'] = node['reftitle']
        if 'target' in node:
            atts['target'] = node['target']
        self.body.append(self.starttag(node, 'a', '', **atts))

        if node.get('secnumber'):
            self.body.append(('%s' + self.secnumber_suffix) %
                             '.'.join(map(str, node['secnumber'])))

def setup(app):
    app.set_translator('html', PatchedHTMLTranslator)

# Enable numref
numfig = True
