"""OSF directives related to the RPi3."""

from docutils import nodes

from core import OsfDirective
from core import linux_artifact


class OsfRPi3LinksDirective(OsfDirective):
    '''Directive class for generating links to versioned artifacts.

    The single required argument is the type of artifacts to generate
    links to. This currently must be "subscriber".
    '''
    required_arguments = 1

    def run(self):
        config = self.get_config()
        version = config.osf_subscriber_version
        if version.startswith('git-'):
            version = 'latest'
        type = self.arguments[0]

        if type != 'subscriber':
            raise self.error('unsupported type {}'.format(type))

        def art_ref(tag, artifact):
            path = 'build-raspberrypi3/{}'.format(artifact)
            return self.build_link('{} ({})'.format(artifact, tag),
                                   linux_artifact(version, path))

        # Paragraph linking to the release.
        links_para = nodes.paragraph()

        # Bullet list of files to get for the release.
        links = nodes.bullet_list()
        art_refs = [
            art_ref(*tag_art) for tag_art in
            [('.sdcard format', 'lmp-gateway-image.rootfs.sdimg'),
             ('.sdcard.xz format', 'lmp-gateway-image.rootfs.sdimg.xz')]]
        self.build_bullet_list(links, art_refs)
        links_para += links

        return [links_para]
