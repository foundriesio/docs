'''Sphinx extensions for managing release artifacts.'''

from docutils import nodes

from core import linux_artifact, linux_artifacts, linux_release
from core import OsfDirective


class OsfArtifactsDirective(OsfDirective):
    '''Directive class for generating links to versioned artifacts.

    The single required argument is the type of artifacts to generate
    links to. Valid values are:

    - lmp-prebuilts: direct links to reference board release
      artifacts, as well as a link to the release downloads page for
      other boards. This is generated for the current subscriber and
      public releases.
    '''
    required_arguments = 1

    def run(self):
        config = self.get_config()
        subscriber = config.osf_subscriber_version
        public = config.osf_public_version
        type = self.arguments[0]

        try:
            handler = getattr(self, type.replace('-', '_'))
        except AttributeError:
            raise self.error('{}: unknown artifact type {}'.format(self.name,
                                                                   type))

        return handler(config, subscriber, public)

    def lmp_prebuilts(self, config, subscriber, public):
        board = config.osf_lmp_reference_board
        board_full = config.osf_lmp_reference_board_full

        def art_ref(version, artifact):
            path = 'build-{}/{}'.format(board, artifact)
            return self.build_link(artifact, linux_artifact(version, path))

        def release_paragraph(release_who, version):
            arts_node = self.build_link('{} artifacts page'.format(version),
                                        linux_artifacts(version))

            ret = nodes.section()
            ret += nodes.title('', release_who.capitalize())
            self.state.document.set_id(ret)

            # para = nodes.paragraph()
            # self.build_paragraph(para, ['Paragraph 1'])
            # ret += para
            # return ret

            # Paragraph linking to the release.
            links_para = nodes.paragraph()
            rel_ref = self.build_link(version, linux_release(version))
            if release_who == 'subscribers':
                login_msg = ' (you need to provide a subscriber log-in)'
            else:
                login_msg = ''
            self.build_paragraph(
                links_para,
                ['The current release is ', rel_ref, '. ',
                 'Files for ', board_full,
                 ' are available at the following links' + login_msg,
                 ':'])

            # Bullet list of files to get for the release.
            links = nodes.bullet_list()
            b = 'build-{}/'.format(board)
            boot = b + 'boot-XXX.uefi.img'
            root = 'lmp-gateway-image-{}-YYYY.rootfs.img'.format(board)
            root_gz = b + root + '.gz'
            boot_node = nodes.literal(text=boot)
            root_node = nodes.literal(text=root)
            root_gz_node = nodes.literal(text=root_gz)
            boot_root_para = nodes.paragraph()
            self.build_paragraph(boot_root_para,
                                 ['the ', boot_node, ' and ', root_gz_node,
                                  ' files from the ', arts_node])
            self.build_bullet_list(
                links,
                [art_ref(version, art) for art in ['bootloader/hisi-idt.py',
                                                   'bootloader/l-loader.bin',
                                                   'bootloader/fip.bin',
                                                   'bootloader/nvme.img']] +
                [boot_root_para])
            links_para += links
            ret += links_para

            # Instructions to unzip the zipped rootfs.
            unzip = nodes.paragraph()
            self.build_paragraph(unzip,
                                 ['Uncompress ', root_gz_node,
                                  ', obtaining ', root_node, '.'])
            ret += unzip

            # Information about other boards.
            others = nodes.paragraph()
            self.build_paragraph(
                others,
                ["If you can't use a {}".format(board_full),
                 ', builds for other boards are also available from the ',
                 arts_node, ', but these may not be functional.'])
            ret += others

            return ret

        return [release_paragraph('subscribers', subscriber),
                release_paragraph('public', public)]
