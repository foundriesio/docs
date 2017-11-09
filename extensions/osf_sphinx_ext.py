"""Open Source Foundries Sphinx extensions"""

from artifacts import LinuxPrebuiltsDirective


def setup(app):
    app.add_config_value('osf_subscriber_version', None, 'env')
    '''Latest released version for subscribers, YY.MM.x'''

    app.add_config_value('osf_public_version', None, 'env')
    '''Latest released version to the public, YY.MM.x'''

    app.add_directive('lmp-prebuilts', LinuxPrebuiltsDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
