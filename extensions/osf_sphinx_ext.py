"""Open Source Foundries Sphinx extensions"""

from artifacts import OsfArtifactsDirective


def setup(app):
    app.add_config_value('osf_subscriber_version', None, 'env')
    '''Latest released version for subscribers, YY.MM.x'''

    app.add_config_value('osf_public_version', None, 'env')
    '''Latest released version to the public, YY.MM.x'''

    app.add_config_value('osf_lmp_reference_board', None, 'env')
    '''Build name for reference board getting special treatment, e.g. hikey'''

    app.add_config_value('osf_lmp_reference_board_full', None, 'env')
    '''Full name for reference board, e.g. 96Boards HiKey'''

    app.add_directive('osf-artifacts', OsfArtifactsDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
