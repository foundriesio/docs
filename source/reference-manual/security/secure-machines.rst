.. highlight:: sh

.. _ref-secure-machines:

Machines with Secure Aspects Enabled by FoundriesFactory
========================================================

The Linux® microPlatform (LmP) provides machines with secure aspects enabled by default.

These machines obtain the configuration needed to enable Secure Boot and other security aspects.
They provide a set of artifacts to help in the process of getting hardware set to Secure Boot.

.. warning::

    It is recommended to read :ref:`ref-secure-boot-imx-habv4` (for i.MX8, :ref:`ref-secure-boot-imx-ahab`) before proceeding with the following steps.

Supported Machines
------------------

* NXP iMX6ULL-EVK Secure: ``imx6ullevk-sec`` is the ``imx6ullevk`` machine configured to have Secure Boot enabled by default.
* NXP iMX8MMINILPD4 EVK Secure: ``imx8mm-lpddr4-evk-sec`` is the ``imx8mm-lpddr4-evk`` machine configured to have Secure Boot and secure storage enabled by default.
* NXP iMX8MNANOD4 EVK Secure: ``imx8mn-ddr4-evk-sec`` is the ``imx8mn-ddr4-evk`` machine configured to have Secure Boot and secure storage enabled by default.
* NXP iMX8MPLUSLPD4 EVK Secure: ``imx8mp-lpddr4-evk-sec`` is the ``imx8mp-lpddr4-evk`` machine configured to have Secure Boot and secure storage enabled by default.
* NXP Toradex Apalis-iMX6 Secure: ``apalis-imx6-sec`` is the ``apalis-imx6`` machine configured to have Secure Boot and secure storage enabled by default.
* NXP Toradex Apalis-iMX8 Secure: ``apalis-imx8-sec`` is the ``apalis-imx8`` machine configured to have Secure Boot and secure storage enabled by default.

Enabling
--------

The suggested way to enable a secure machine is to select the correct platform when creating your Factory.
However, this may not be ideal for evaluating your setup in an open state for easier development.

The platform definition comes from ``ci-scripts``, but due to computation limits, the CI is configured to decline changes in the ``machines:`` parameter.
When attempting to replace or add a new machine in a Factory, you will likely encounter something like::

    remote: A new machine is being added: {'<machine>'}
    remote: ERROR: Please contact support to update machines
    remote: error: hook declined to update refs/heads/master
    To https://source.foundries.io/factories/<factory>/ci-scripts.git
     ! [remote rejected]           master -> master (hook declined)

In this case, you should open a support ticket.

Using the Secure Machine
------------------------

Trigger a platform build and wait until the Target is created.

Follow the steps from :ref:`ug-flashing` to prepare the hardware and download the same artifacts.

The list of artifacts downloaded should be:

* ``mfgtool-files-<machine-sec>.tar.gz``
* ``lmp-factory-image-<machine-sec>.wic.gz``
* ``SPL-<machine-sec>``
* ``sit-<machine-sec>.bin``
* ``u-boot-<machine-sec>.itb``

.. note::
    For i.MX8* based machines, the ``SPL`` binary is included in ``imx-boot``.
    Refer to ``imx-boot-<machine-sec>`` through this document.

Expand the tarballs:

.. prompt:: bash host:~$

    gunzip lmp-factory-image-<machine-sec>.wic.gz
    tar -zxvf mfgtool-files-<machine-sec>.tar.gz

The resultant directory tree should look like the following::

    ├── lmp-factory-image-<machine-sec>.wic
    ├── mfgtool-files-<machine-sec>
    │   ├── bootloader.uuu
    │   ├── close.uuu
    │   ├── full_image.uuu
    │   ├── fuse.uuu
    │   ├── readme.md
    │   ├── SPL-mfgtool
    │   ├── u-boot-mfgtool.itb
    │   ├── uuu
    │   └── uuu.exe
    ├── mfgtool-files-<machine-sec>.tar.gz
    ├── SPL-<machine-sec>
    ├── sit-<machine-sec>.bin
    └── u-boot-<machine-sec>.itb


Follow the ``readme.md`` under ``mfgtool-files-<machine-sec>`` for instructions to sign the SPL images, to fuse, and close the board.

.. warning::
   
   The **fuse** and **close** procedures are irreversible.
   The instructions from the ``readme.md`` file should be followed and executed with caution and only after understanding the critical implication of those commands.

.. include:: imx-generic-custom-keys.rst

Accessing Secure Storage
------------------------

.. note::
   The LmP leverages the eMMC Replay Protected Memory Block (RPMB) as secure storage. This section is only applicable for devices that provide this feature.

Once a device has been successfully fused and closed, the secure storage RPMB becomes available.
This is accessed through ``fiovb`` (Foundries.io™ Verified Boot) early trusted application from Open Portable-Trusted Execution Environment (OP-TEE).

By default, the secure storage only holds the variables used by ``aktualizr-lite`` to handle the updates, previously stored in ``uboot-env`` for non-fused boards.
You can extend this to store custom variables that need to be made secure, like mac addresses, serial numbers and other critical device information.

Writing to Secure Storage
^^^^^^^^^^^^^^^^^^^^^^^^^

.. prompt:: bash device:~#, auto

   device:~# fiovb_setenv <variable> <value>

Reading From Secure Storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. prompt:: bash device:~#, auto

   device:~# fiovb_printenv <variable>
