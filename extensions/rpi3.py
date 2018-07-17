"""OSF directives related to the RPi3."""

from docutils import nodes
from docutils.parsers.rst import directives

from core import OsfDirective
from core import linux_artifact


class OsfRPi3LinksDirective(OsfDirective):
    '''Directive class for generating links to versioned artifacts.
    '''

    def run(self):
        self.state.document.settings.env.note_dependency(__file__)
        config = self.get_config()

        version = config.osf_subscriber_version
        if version.startswith('git-'):
            version = 'latest'

        def art_ref(artifact):
            path = 'supported-raspberrypi3-64/{}'.format(artifact)
            url = linux_artifact(version, path)
            return self.build_link(url, url)

        # Paragraph linking to the release.
        links_para = nodes.paragraph()

        # Link to file to get for the release.
        link = art_ref('lmp-gateway-image-raspberrypi3-64.img.gz')
        links_para += link

        return [links_para]


class OsfRPi3OSTreeDirective(OsfDirective):
    '''Directive class for generating a link to the OSTree tarball
    '''

    def run(self):
        self.state.document.settings.env.note_dependency(__file__)
        config = self.get_config()
        version = config.osf_subscriber_version
        if version.startswith('git-'):
            version = 'latest'

        def art_ref(artifact):
            path = 'supported-raspberrypi3-64/{}'.format(artifact)
            url = linux_artifact(version, path)
            return self.build_link(url, url)

        # Paragraph linking to the release.
        links_para = nodes.paragraph()

        # Link to file to get for the release.
        link = art_ref('other/raspberrypi3-64-ostree_repo.tar.bz2')
        links_para += link

        return [links_para]
