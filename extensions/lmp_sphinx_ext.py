"""Linux microPlatform specific Sphinx extensions"""

from rpi3 import LmpRPi3LinksDirective, LmpRPi3OSTreeDirective


def setup(app):
    app.add_config_value('mp_version', None, 'env')
    '''Latest released version for subscribers'''

    app.add_directive('lmp-rpi3-links', LmpRPi3LinksDirective)
    app.add_directive('lmp-rpi3-ostree', LmpRPi3OSTreeDirective)

    return {
        'version': '0.2',
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
