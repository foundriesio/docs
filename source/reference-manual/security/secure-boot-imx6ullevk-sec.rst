.. highlight:: sh

.. _ref-secure-boot-imx6ullevk-sec:

NXP iMX6ULL-EVK with secure boot enabled by FoundriesFactory
============================================================

The machine ``imx6ullevk-sec`` is the ``imx6ullevk`` machine configured to have
secure boot enabled by default.

The purpose of this machine is to gather the needed configuration to enable
secure boot and provide a set of artifacts to help in the process needed to have
the hardware board set to secure boot.

.. warning::

    It is recommended to read :ref:`ref-secure-boot-imx` before proceeding with
    the following steps.

How to enable
-------------

In the ``ci-scripts`` git repository from the FoundriesFactory, update the
``factory-config.yml`` to include the following configuration::

    machines:
    - imx6ullevk-sec

    mfg_tools:
    - machine: imx6ullevk-sec
        params:
        DISTRO: lmp-mfgtool
        IMAGE: mfgtool-files
        EXTRA_ARTIFACTS: mfgtool-files.tar.gz
        UBOOT_SIGN_ENABLE: "1"

How to use
----------

Trigger a platform build and wait until the target is created.

Follow the steps from :ref:`ref-rm_board_imx6ullevk` to prepare the hardware and
download the same artifacts.

The list of artifacts downloaded should be:

* ``mfgtool-files-imx6ullevk-sec.tar.gz``
* ``lmp-factory-image-imx6ullevk-sec.wic.gz``
* ``SPL-imx6ullevk-sec``
* ``sit-imx6ullevk-sec.bin``
* ``u-boot-imx6ullevk-sec.itb``

Expand the tarballs:

.. prompt:: bash host:~$

    gunzip lmp-factory-image-imx6ullevk.wic.gz
    tar -zxvf mfgtool-files-imx6ullevk.tar.gz

The resultant directory tree should look like the following::

    ├── lmp-factory-image-imx6ullevk-sec.wic
    ├── mfgtool-files-imx6ullevk-sec
    │   ├── bootloader.uuu
    │   ├── close.uuu
    │   ├── full_image.uuu
    │   ├── fuse.uuu
    │   ├── readme.md
    │   ├── SPL-mfgtool
    │   ├── u-boot-mfgtool.itb
    │   ├── uuu
    │   └── uuu.exe
    ├── mfgtool-files-imx6ullevk-sec.tar.gz
    ├── SPL-imx6ullevk-sec
    ├── sit-imx6ullevk-sec.bin
    └── u-boot-imx6ullevk-sec.itb


Follow ``readme.md`` instructions to sign the SPL images, to fuse, and close the
board.

.. warning:: The **fuse** and **close** procedures are irreversible. The
  instructions from the ``readme.md`` file should be followed and executed with
  caution and only after understanding the critical implication of those commands.

.. include:: imx-generic-custom-keys.rst
