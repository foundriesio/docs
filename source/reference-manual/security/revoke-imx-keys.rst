.. highlight:: sh

.. _ref-revoke-imx-keys:

Revoke Secure Boot Keys on i.MX
===============================

This page covers how to revoke a SRK key on i.MX SoC boards.
This includes the purpose of revocations, and where to find more information on this topic.

Revocation of a Key: Overview
-----------------------------

Revoking a SRK key should be done when one or more SRK keys become compromised.
The SRK keys are keys permanently copied to the hardware and are used during boot to unsure the Root of Trust.

When a SRK key is revoked, the key is considered unreliable.
Thus, any image signed with that key will not be executed during boot.
This is a permanent change to the hardware.

The example used on this page is a root of trust with 4 SRK keys fused to an i.MX machine.
For different architectures, some commands may differ.
Details on how to setup Secure Boot on i.MX machines can be found under :ref:`ref-secure-boot`.

The following table lists the values for each SRK key.
The value for ``SRK_REVOKE`` mask is used for the revocation command line, and is detailed in the following sections.
The value for ``srk-index`` is a parameter for ``sign-file.sh``, used to sign the boot artifacts.

.. _srk-revoke-imx:

.. csv-table:: **SRK Revoke i.MX**
   :file: ../../_static/csv/revoke_imx.csv
   :widths: 30, 30, 30, 30, 30
   :header-rows: 1

``srk-index`` is a ``sign-file.sh`` parameter that defines a SRK key to be used to sign the SPL.

Columns 1, 2 and 3 are from Table 4 from the `Secure Boot Using HABv4 Guide`_.

.. note::

    In a HABv4 environment, only the first 3 SRK keys can be revoked.
    In a AHAB environment, all 4 SRK can be revoked.
    For more details, check the `Code-Signing Tool User's Guide`_.
    When there is no available SRK key, the board cannot boot!

How to Sign the Boot Image for Revoking a Key
---------------------------------------------

The first step is to make sure there are other SRK keys available for the boot.
A key can only be revoked after a secure boot with a different key is executed, with the permission to unlock ``SRK_REVOKE`` write access.
After that a fuse is burned. In short:

    * boot with an available SRK key, different from the one to revoke
    * unlock ``SRK_REVOKE``
    * fuse a register according to the SRK key being revoked.

The signing process is based on the commands from :ref:`ref-secure-boot`, adding two parameters:

    ``--srk-index = <value>`` to choose the SRK key to be used on that boot sequence.
    For the right value, consult :ref:`srk-revoke-imx`.

    ``--enable-revoke`` to unlock the key revocation register write access.

Write access to register ``SRK_REVOKE`` is protected by the bit ``SRK_REVOKE_LOCK``.
This can be configured by CST.
The parameter ``--enable-revoke`` brings the configuration needed by CST to unlock write access to ``SRK_REVOKE``, making revocation possible.

.. warning::
    After revoking a SRK key, it cannot be used to boot the board again.
    A board with no remaining reliable SRK keys does not boot.

For example, for a ``imx6ullevk-sec`` SPL image to be signed with SRK1, use the following command::

    #Sign the MFGTool SPL file
    ./sign-file.sh --engine SW --key-dir $KEY_PATH \
                --cst $CST_PATH \
                --spl $SPL_PATH/mfgtool-files-imx6ullevk-sec/SPL-mfgtool \
                --fix-sdp-dcd \
                --srk-index 2 \
                --enable-revoke

    #Sign the SPL file
    ./sign-file.sh --engine SW --key-dir $KEY_PATH \
                --cst $CST_PATH \
                --spl $SPL_PATH/SPL-imx6ullevk-sec \
                --srk-index 2

.. warning::

    In the example, only the SPL from MFGtool has write access to revoke the key.
    The suggestion is to use ``bootloader.uuu`` to load the MFGTool SPL, and then U-Boot prompt to perform the fuse programming command.
    For other boot scripts,you may be required to include ``--enable-revoke`` to the SPL file signing process (second command).

How to Revoke a Key
-------------------

The suggestion is to use ``bootloader.uuu`` to access U-Boot prompt for executing the following command::

    fuse prog <bank> <word> <hexval>

The values for ``<bank>`` and ``<word>`` for the register ``SRK_REVOKE`` can be found on the SoC Reference Manual.
The value for ``<hexval>`` is from :ref:`srk-revoke-imx`.

For example, to revoke SRK2 for ``imx6ullevk-sec``::

    fuse prog 5 7 0x4
    Programming bank 5 word 0x00000007 to 0x00000004...
    Warning: Programming fuses is an irreversible operation!
            This may brick your system.
            Use this command only if you are sure of what you are doing!

    Really perform this fuse programming? <y/N>
    y

The following error happens when the key revocation write access is not available (``SRK_REVOKE`` is not unlocked).
This can be fixed by adding ``--enable-revoke`` during the signing of the boot image::

    mxc_ocotp fuse_prog(): Access protect error
    ERROR

After the revocation of SRK2, it can never be used to boot that board again.
Test it by signing again using this SRK key and the boot must fail.

How to Revoke a Key for Devices in a Fleet
------------------------------------------

The method suggested here describes the commands needed to revoke a key from the SoC perspective.
It requires serial download and console and bootloader access, which are not always accessible on devices in the field.
However, this is the base procedure to be used on a fleet.

The process can be automated in a Factory by creating a signed SPL using another SRK key and enabling the ``SRK_REVOKE`` write access.
While on this, the ``bootcmd`` can be customized to perform the fusing command needed to revoke the compromised key.

The fusing can be performed in Linux® Kernel mode instead, when the system is configured to allow this kind of execution.

Then the firmware update is performed in a Wave—described in detail under :ref:`ref-production-targets`.

After the revocation wave, another firmware update wave is required.
This time, with the bootloader configured to disable write access to the ``SRK_REVOKE``, and still using the reliable SRK key.

This is a two-steps process which is highly dependent on the device configuration and access, and requires caution.
The revoke fusing command can make the device unavailable if not executed properly.

To get help with the revocation automatization, open a `support ticket <https://support.foundries.io>`_.

.. i.MX Secure Boot on HABv4 Supported Devices (Rev. 4 — June 2020)
.. _Secure Boot Using HABv4 Guide:
   https://www.nxp.com/webapp/Download?colCode=AN4581&location=null

.. Code-Signing Tool User's Guide, Rev. 3.3.1
.. _Code-Signing Tool User's Guide:
   https://cache.nxp.com/secured/bsps/cst-3.3.1.tgz?fileExt=.tgz
