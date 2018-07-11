'''Core classes and utilities for OSF Sphinx extensions.'''

from docutils import nodes
from docutils.parsers.rst import Directive

ZEPHYR_RELEASE_URL_FMT = 'https://app.foundries.io/mp/zmp/{}'
ZEPHYR_RELEASE_ARTIFACTS_URL_FMT = 'https://app.foundries.io/mp/zmp/{}/artifacts'
LINUX_RELEASE_URL_FMT = 'https://app.foundries.io/mp/lmp/{}'
LINUX_RELEASE_ARTIFACTS_URL_FMT = 'https://app.foundries.io/mp/lmp/{}/artifacts'


def linux_release(version):
    '''Get URL of a Linux microPlatform release.'''
    return LINUX_RELEASE_URL_FMT.format(version)


def linux_artifacts(version):
    '''Get URL of a Linux microPlatform release's artifacts page.'''
    return LINUX_RELEASE_ARTIFACTS_URL_FMT.format(version)


def linux_artifact(version, artifact_path):
    '''Get URL of a Linux microPlatform release's artifact.'''
    return linux_artifacts(version) + '/' + artifact_path


def zephyr_release(version):
    '''Get URL of a Zephyr microPlatform release.'''
    return ZEPHYR_RELEASE_URL_FMT.format(version)


def zephyr_artifacts(version):
    '''Get URL of a Zephyr microPlatform release's artifacts page.'''
    return ZEPHYR_RELEASE_ARTIFACTS_URL_FMT.format(version)


def zephyr_artifact(version, artifact_path):
    '''Get URL of a Zephyr microPlatform release's artifact.'''
    return zephyr_artifacts(version) + '/' + artifact_path


class OsfDirective(Directive):
    '''Convenience superclass for other Directives.

    This hides the mess of the Sphinx/docutils state backend.'''

    def get_env(self):
        '''Get the current sphinx.environment.BuildEnvironment.'''
        return self.state.document.settings.env

    def get_config(self, value=None):
        '''Get the current sphinx.config.Config.'''
        cfg = self.state.document.settings.env.config
        if value is None:
            return cfg
        else:
            return getattr(cfg, value)

    def get_app(self):
        '''Get the current sphinx.application.Sphinx.'''
        return self.state.document.settings.env.app

    def get_builder(self):
        '''Get the current sphinx.builders.Builder.'''
        return self.state.document.settings.env.app.builder

    def build_paragraph(self, node, items):
        for item in items:
            if isinstance(item, nodes.Node):
                node += item
            else:
                node += nodes.Text(item)

    def build_bullet_list(self, node, items):
        for item in items:
            li = nodes.list_item()
            li_body = nodes.paragraph()
            if isinstance(item, nodes.Node):
                li_body += item
            else:
                li_body += nodes.Text(item)
            li += li_body
            node += li

    def build_link(self, text, uri):
        ref = nodes.reference(text=text)
        ref['refuri'] = uri
        return ref
