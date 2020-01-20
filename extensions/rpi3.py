"""reST directives related to Foundries.io + RPi3."""

from docutils import nodes

import core
from core import linux_github_artifact, linux_subscriber_artifact


class LmpRPi3LinksDirective(core.Directive):
    '''Directive class for generating links to versioned artifacts.
    '''

    def run(self):
        self.state.document.settings.env.note_dependency(__file__)
        config = self.get_config()

        def art_ref(artifact):
            if config.mp_version.startswith('git-'):
                return self.build_link('(dev docs build; use app.foundries.io)',
                                       'https://app.foundries.io')
            else:
                url = linux_github_artifact(config.mp_version, artifact)
                return self.build_link(url, url)

        # Paragraph linking to the release.
        links_para = nodes.paragraph()

        # Link to file to get for the release.
        link = art_ref('lmp-gateway-image-raspberrypi3-64.wic.gz')
        links_para += link

        return [links_para]


class LmpRPi3OSTreeDirective(core.Directive):
    '''Directive class for generating a link to the OSTree tarball
    '''

    def run(self):
        self.state.document.settings.env.note_dependency(__file__)
        config = self.get_config()

        def art_ref(artifact):
            path = 'supported-raspberrypi3-64/{}'.format(artifact)
            url = linux_subscriber_artifact(config.lmp_build, path)
            return self.build_link(url, url)

        # Paragraph linking to the release.
        links_para = nodes.paragraph()

        # Link to file to get for the release.
        link = art_ref('other/raspberrypi3-64-ostree_repo.tar.bz2')
        links_para += link

        return [links_para]
