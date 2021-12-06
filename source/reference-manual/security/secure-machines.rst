.. highlight:: sh

.. _ref-secure-machines:

Machines with secure aspects enabled by FoundriesFactory
========================================================

LmP provides machines with secure aspects enabled by default when using
FoundriesFactory.

The purpose of these machines is to gather the needed configuration to enable
secure boot and other security aspects and to provide a set of artifacts to help
in the process needed to have the hardware board set to secure boot.

.. warning::

    It is recommended to read :ref:`ref-secure-boot-imx-habv4` before proceeding with
    the following steps.

Supported machines
------------------

* NXP iMX6ULL-EVK Secure: ``imx6ullevk-sec`` is the ``imx6ullevk`` machine configured to have secure boot enabled by default.
* NXP iMX8M-MINILPD4 EVK Secure: ``imx8mm-lpddr4-evk-sec`` is the ``imx8mmevk`` machine configured to have secure boot and secure storage enabled by default.
* NXP Toradex Apalis-iMX6 Secure: ``apalis-imx6-sec`` is the ``apalis-imx6`` machine configured to have secure boot and secure storage enabled by default.

How to enable
-------------

The suggested way to enable a secure machine in a factory is to select the
correct platform when creating the factory. This might not be ideal as the
customer might want to evaluate their setup in an open state for easier
development.

The platform definition comes from ``ci-scripts`` but due to computation limits,
the CI is configured to decline changes in the ``machines:`` parameter. When
attempting to replace or add a new machine in a factory, customers face this
issue::

    remote: A new machine is being added: {'<machine>'}
    remote: ERROR: Please contact support to update machines
    remote: error: hook declined to update refs/heads/master
    To https://source.foundries.io/factories/<factory>/ci-scripts.git
     ! [remote rejected]           master -> master (hook declined)

In this case, ask a support engineer to update the ``factory-config.yml`` file
in ``ci-scripts`` git repository for your FoundriesFactory to the following
configuration::

    machines:
    - <machine-sec>

    mfg_tools:
    - machine: <machine-sec>
        params:
        DISTRO: lmp-mfgtool
        IMAGE: mfgtool-files
        EXTRA_ARTIFACTS: mfgtool-files.tar.gz
        UBOOT_SIGN_ENABLE: "1"

How to use
----------

Trigger a platform build and wait until the target is created.

Follow the steps from :ref:`ref-boards` to prepare the hardware and download the
same artifacts.

The list of artifacts downloaded should be:

* ``mfgtool-files-<machine-sec>.tar.gz``
* ``lmp-factory-image-<machine-sec>.wic.gz``
* ``SPL-<machine-sec>``
* ``sit-<machine-sec>.bin``
* ``u-boot-<machine-sec>.itb``


.. note::
    For the i.MX8* based machines, the ``SPL`` binary is included in ``imx-boot``
    and the user should refer to ``imx-boot-<machine-sec>`` through this
    document.

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


Follow the ``readme.md`` under ``mfgtool-files-<machine-sec>`` for instructions
to sign the SPL images, to fuse, and close the board.

.. warning:: The **fuse** and **close** procedures are irreversible. The
  instructions from the ``readme.md`` file should be followed and executed with
  caution and only after understanding the critical implication of those commands.

.. include:: imx-generic-custom-keys.rst
