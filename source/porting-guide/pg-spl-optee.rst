.. _ref-pg-spl-optee:

OP-TEE (When Applicable)
========================

OP-TEE is deployed as part of the FIT image.
Foundries.io has its own OP-TEE recipes.
You will need to provide machine-specific configuration in ``meta-subscriber-overrides`` for the OP-TEE build, e.g.
OP-TEE machine name, UART address, and overlay address.
The recommendation is to use the reference board OP-TEE support for the ``OPTEEMACHINE``.

``recipes-security/optee/optee-os-fio_3.10.0.bbappend``:

.. prompt:: text

    OPTEEMACHINE:<machine> = "imx-mx8mmevk"
    EXTRA_OEMAKE:append:<machine> = " \
      CFG_UART_BASE=UART4_BASE \
      CFG_NXP_CAAM=y CFG_RNG_PTA=y \
      CFG_DT=y CFG_EXTERNAL_DTB_OVERLAY=y CFG_DT_ADDR=0x43200000 \
    "

.. note::

    If you choose to not use the reference board as the ``OPTEEMACHINE``,
    further considerations are needed to integrate OP-TEE support into LmP.
    See :ref:`ref-sec-tfa-optee`.
