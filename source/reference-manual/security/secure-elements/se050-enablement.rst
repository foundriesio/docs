.. _ref-security_se05x_enablement:

Enabling SE05X
==============

This section demonstrates how to enable the SE05X middleware in
``meta-subscriber-overrides``.

.. note::
    This procedure is valid for boards running OP-TEE 3.15.0.

Enable the `se05x` MACHINE_FEATURES for the target machine and provide the
correct OEFID for the `se05x` device in **lmp-factory-custom**. The OEFID value
can be found in `SE050 configurations`_.

**conf/machine/include/lmp-factory-custom.inc:**

.. prompt:: text

    SE05X_OEFID:<machine> = "0xA1F4"
    MACHINE_FEATURES:append:<machine> = " se05x"

.. note::
    If set incorrectly, the correct OEFID value can be checked in the boot log:

    .. code-block:: none

        I/TC: OP-TEE version: 3.15.0-84-gf0446cdb3 (gcc version 10.2.0 (GCC)) #1 Sat 11 Dec 2021 02:11:09 AM UTC aarch64
        I/TC: Primary CPU initializing
        I/TC: se050: Info: Applet ID
        ...
        I/TC: se050: Info: OEF ID
        I/TC: se050: Info: 	a1.f4

This step is enough to enable SE05X for the supported machines for factories
created since v85.

Push the changes to the ``meta-subscriber-overrides`` repository to trigger a
new build with SE05X support enabled. Be aware that an image created with SE05X
enabled does not boot on boards without the SE05X properly attached.

.. note::
    Please be aware that at this moment only ``imx6ullevk`` and
    ``imx8mm-lpddr4-evk`` support SE05X integration without extra changes in
    LmP.

Special cases
-------------

1. For older factories created **before v85**, it is also needed to add the `se05x`
features to the **lmp-factory-image** build:

**recipes-samples/images/lmp-factory-image.bb:**

.. prompt:: text

    # Support for SE05X
    require ${@bb.utils.contains('MACHINE_FEATURES', 'se05x', 'recipes-samples/images/lmp-feature-se05x.inc', '', d)}

2. If working with a different i.MX machine without SE05X LmP default support
(``imx6ullevk`` and ``imx8mm-lpddr4-evk``), also provide which SoC I2C bus
connects to the SE05X device:

**recipes-security/optee/optee-os-fio_%.bbappend:**

.. prompt:: text

    EXTRA_OEMAKE:append:<machine> = " \
        ${@bb.utils.contains('MACHINE_FEATURES', 'se05x', 'CFG_IMX_I2C=y CFG_CORE_SE05X_I2C_BUS=<i2c_bus>', '', d)} \
    "

Make sure to push the changes to the ``meta-subscriber-overrides`` repository
to trigger a build with the new configurations.

.. _SE050 configurations:
   https://www.nxp.com/docs/en/application-note/AN12436.pdf
