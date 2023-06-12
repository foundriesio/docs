.. highlight:: sh

.. _ref-anti-rollback-protection:

Anti-Rollback Protection
========================

Introduction
------------

The main role of anti-rollback protection is to prevent downgrading boot
firmware, which has been marked as obsolete or deprecated due to
security concerns.

In some cases, downgrading of boot firmware can lead to a unbootable
system due to boot firmware runtime service API changes.
This why it is required on some platforms to have the Linux® kernel in sync with
appropriate boot firmware.

Store Boot Firmware Version in Boot Firmware Artifacts
------------------------------------------------------

To define the boot firmware version number, set the ``LMP_BOOT_FIRMWARE_VERSION``
global variable in your ``meta-subscriber-overrides`` layer. For example:
::

    diff --git a/conf/machine/include/lmp-factory-custom.inc b/conf/machine/include/lmp-factory-custom.inc
    index 0fe26b8..2a9815d 100644
    --- a/conf/machine/include/lmp-factory-custom.inc
    +++ b/conf/machine/include/lmp-factory-custom.inc
    @@ -22,4 +22,4 @@ UEFI_SIGN_KEYDIR = "${TOPDIR}/conf/factory-keys/uefi"
     # TF-A Trusted Boot
     TF_A_SIGN_KEY_PATH = "${TOPDIR}/conf/factory-keys/tf-a/privkey_ec_prime256v1.pem"

    +LMP_BOOT_FIRMWARE_VERSION:stm32mp15-eval = "3"



When ``LMP_BOOT_FIRMWARE_VERSION`` is defined, an additional
node, which contains information about boot firmware version, is automatically
added to U-Boot Device Tree BLOB during compilation.
Example of a node (added to ``/firmware``):
::

    bootloader {
        bootfirmware-version = "3";
        compatible = "lmp,bootloader";
    };


Enable U-Boot Access to Boot Firmware Metadata
-----------------------------------------------

U-Boot has to be aware of the boot firmware information stored in its DTB,
so as to read/access it. To enable this, add the following
config option to your board's ``lmp.cfg``:
::

    CONFIG_BOOTFIRMWARE_INFO=y


Enable Anti-Rollback Protection
-------------------------------

When the board is flashed with a LmP Factory image, anti-rollback protection
is disabled by default. To enable it, use ``fiovb_setenv`` (closed boards) or
``fw_setenv`` (open board) cmds in the Linux shell:
::

    $ fiovb_setenv rollback_protection 1

During the next OTA update, aktualizr-lite will report in logs
that anti-rollback protection for boot firmware is activated:
::

   ....
   info: Installing package using ostree+compose_apps package manager
   info: Performing sync()
   info: Bootloader will be updated from version 2 to 3; rollback protection: ON
   info: Update complete. Please reboot the device to activate


and U-Boot will print the boot firmware version of currently loaded firmware and
status of anti-rollback protection:
::

    U-Boot 2022.04+fio+g3eb76326d0 (Apr 25 2023 - 15:12:11 +0000)
    ......
    Boot firmware version: 3
    ......
    FIO: Anti-rollback protection for boot firmware is enabled
