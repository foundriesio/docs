.. _ref-pg-spl-optee:

OP-TEE (when applicable)
========================

OP-TEE is deployed as part of the FIT image. Foundries.io has its own
OP-TEE recipes and the user needs to provide machine-specific
configuration in ``meta-subscriber-overrides`` for the OP-TEE build, e.g.
OP-TEE machine name, UART address, overlay address. The recommendation is to
use the reference board OP-TEE support for the OPTEEMACHINE.

``recipes-security/optee/optee-os-fio_3.10.0.bbappend``:

.. prompt:: text

    OPTEEMACHINE_<machine> = "imx-mx8mmevk"
    EXTRA_OEMAKE_append_<machine> = " \
      CFG_UART_BASE=UART4_BASE \
      CFG_NXP_CAAM=y CFG_RNG_PTA=y \
      CFG_DT=y CFG_EXTERNAL_DTB_OVERLAY=y CFG_DT_ADDR=0x43200000 \
    "

.. note::

    If the user chooses to not use the reference board as the
    OPTEEMACHINE, further considerations have to be made in order to
    integrate OP-TEE support into LmP: :ref:`ref-sec-tfa-optee`.