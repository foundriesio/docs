.. _ref-security_se05x_enablement:

Enabling SE05X
==============

This section demonstrates how to enable the SE05X middleware in ``meta-subscriber-overrides``.

.. note::
    This procedure is valid for boards running OP-TEE 3.15.0 or newer.

Enable the ``se05x`` ``MACHINE_FEATURES`` for the target machine and provide the correct OEFID in ``lmp-factory-custom``.
The OEFID value can be found in `SE050 configurations`_.

``conf/machine/include/lmp-factory-custom.inc``:

.. prompt:: text

    SE05X_OEFID:<machine> = "0xA1F4"
    MACHINE_FEATURES:append:<machine> = " se05x"

.. note::
    If set incorrectly, the *correct* OEFID value can be checked in the boot log:

    .. code-block:: none

        I/TC: OP-TEE version: 3.15.0-84-gf0446cdb3 (gcc version 10.2.0 (GCC)) #1 Sat 11 Dec 2021 02:11:09 AM UTC aarch64
        I/TC: Primary CPU initializing
        I/TC: se050: Info: Applet ID
        ...
        I/TC: se050: Info: OEF ID
        I/TC: se050: Info: 	a1.f4

This step is enough to enable SE05X for the supported machines for Factories created since LmP v85.

Push the changes to the ``meta-subscriber-overrides``, triggering a new build with SE05X support enabled.
Be aware that an image created with SE05X enabled does not boot on boards without the SE05X properly attached.

.. note::
    Please be aware that at this moment only:

    * ``imx6ullevk``
    * ``imx8mn-ddr4-evk``
    * ``imx8mm-lpddr4-evk``
    * ``imx8mp-lpddr4-evk``

    support SE05X integration without extra changes in LmP.

.. _SE050 configurations:
   https://www.nxp.com/docs/en/application-note/AN12436.pdf
