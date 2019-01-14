'''Core classes and utilities for our Sphinx extensions.'''

from docutils import nodes
from docutils.parsers.rst import Directive


def linux_github_artifact(lmp_build, artifact_path):
    '''Get URL of a Linux microPlatform release's artifact.'''
    fmt = 'https://github.com/foundriesio/lmp-manifest/releases/download/' \
          '{build}/{path}'
    return fmt.format(build=lmp_build, path=artifact_path)


def linux_subscriber_artifact(lmp_build, artifact_path):
    '''Get a *subscriber* URL to an LMP artifact.'''

    fmt = 'https://app.foundries.io/mp/lmp/{build}/artifacts/{path}'
    return fmt.format(build=lmp_build, path=artifact_path)


class Directive(Directive):
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
