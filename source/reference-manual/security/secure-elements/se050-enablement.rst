.. _ref-security_se050_enablement:

Enabling SE050
==============

This section demonstrates how to enable the SE050 middleware in
``meta-subscriber-overrides``.

.. note::
    This procedure refers to the steps to enable SE050 with the
    :ref:`ref-rm_board_imx6ullevk` board. Similar procedures can be applied for
    different boards. Please be aware that at this moment only ``imx6ullevk``,
    ``imx8mm-lpddr4-evk`` and ``imx8mqevk`` support SE050 integration.

.. note::
    This procedure is valid for boards running OP-TEE 3.10.

1. Create the path to extend the ``optee-os-fio`` recipe in
``meta-subscriber-overrides`` (if not already created):

.. prompt:: bash host:~$, auto

    host:~$ mkdir -p recipes-security/optee/optee-os-fio

2. Get the ``EdgeLock SE05x Plug & Trust Middleware`` from the `NXP sources <https://www.nxp.com/products/security-and-authentication/authentication/edgelock-se050-plug-trust-secure-element-family-enhanced-iot-security-with-maximum-flexibility:SE050?tab=Design_Tools_Tab>`_
and move it to the folder created in the last step.

.. note::
    This tutorial was tested using
    ``EdgeLock SE05x Plug & Trust Middleware version (03.03.00)``.

3. Create the .bbappend file for the ``optee-os-fio`` recipe to include the
middleware and needed configurations to enable SE050.

**recipes-security/optee/optee-os-fio_%.bbappend:**

.. prompt:: text

    FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

    SRC_URI_append = " \
        file://SE-PLUG-TRUST-MW.zip;name=se050-mw \
    "

    SRC_URI[se050-mw.md5sum] = "9f34b2bf2e4fcf6f576c078df5dd98f8"
    SRC_URI[se050-mw.sha256sum] = "f8d1b355f21f3fd380087efc0517a9df06e3dd387744ede99f0542642b4b7aab"

    do_compile_prepend() {
        # Link SE050 MW in order for it to available to OP-TEE
        ln -sf ${WORKDIR}/simw-top ${S}/lib/libnxpse050/se050/simw-top
    }

    EXTRA_OEMAKE_append = " \
        CFG_IMX_I2C=y CFG_CORE_SE05X=y CFG_NXP_SE05X_RNG_DRV=n \
        CFG_NXP_CAAM_RSA_DRV=n CFG_NUM_THREADS=1 CFG_CORE_SE05X_DISPLAY_INFO=1 \
        CFG_CORE_SE05X_SCP03_EARLY=1 \
        CFG_CORE_SE05X_OEFID=0xA1F4 CFG_CORE_SE05X_I2C_BUS=1 \
    "

.. note::
    You might need to adapt some parameters in this file, especially if building
    for a different board than ``imx6ullevk`` or if building different versions
    of the SE050 middleware. In those cases, double check the ``md5sum`` and
    ``sha256sum`` for the middleware file as well as ``CFG_CORE_SE05X_I2C_BUS``,
    which should refer to the correct I2C bus on the target board. For other
    references on the used parameters, please check :ref:`ref-secure-element`.

Push the changes to the ``meta-subscriber-overrides`` repository to trigger a
new build with SE050 support enabled. Be aware that an image created with SE050
enabled does not boot on boards without the SE050 properly attached.
