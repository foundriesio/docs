.. highlight:: sh

.. _ref-linux-targets:

Additional Linux microPlatform Targets
======================================

This section provides information on running the Linux microPlatform
for other targets. It is provided on a best-effort basis.

Prebuilt Binaries
-----------------

Several boards have reference builds provided by Foundries.io
in the latest Linux microPlatform release, available at
https://github.com/foundriesio/lmp-manifest/releases/latest.

Please note that these builds are provided for reference in hopes they
are useful; not all receive equal testing.

Intel Core i7 (e.g. MinnowBoard Turbot)
---------------------------------------

.. toggle-header::
   :header: Click to show/hide

    Set ``MACHINE`` to ``intel-corei7-64`` when setting up your work
    environment with the ``setup-environment`` script::

      MACHINE=intel-corei7-64 source setup-environment [BUILDDIR]

    At the end of the build, your build artifacts will be found under
    ``deploy/images/intel-corei7-64``. The artifact you will use to
    flash your microSD card is ``lmp-gateway-image-intel-corei7-64.wic.gz``.

    To flash your microSD card, run::

      gunzip -f lmp-gateway-image-intel-corei7-64.wic.gz
      sudo dd if=lmp-gateway-image-intel-corei7-64.wic of=/dev/mmcblkX bs=4M

    Where :file:`/dev/mmcblkX` is your SD card device.

    Please see https://elinux.org/Minnowboard:Basics
    for additional board documentation.

BeagleBone Black
----------------

.. toggle-header::
   :header: Click to show/hide

   Set ``MACHINE`` to ``beaglebone-yocto`` when setting up your work
   environment with the ``setup-environment`` script::

     MACHINE=beaglebone-yocto source setup-environment [BUILDDIR]

   At the end of the build, your build artifacts will be found under
   ``deploy/images/beaglebone-yocto``. The artifact you will use to
   flash your microSD card is ``lmp-gateway-image-beaglebone-yocto.wic.gz``.

   To flash your microSD card, run::

     gunzip -f lmp-gateway-image-beaglebone-yocto.wic.gz
     sudo dd if=lmp-gateway-image-beaglebone-yocto.wic of=/dev/mmcblkX bs=4M

   Where :file:`/dev/mmcblkX` is your SD card device.

   Please see https://elinux.org/Beagleboard:BeagleBoneBlack for additional
   board documentation.

Toradex Colibri iMX7D eMMC (Aster)
----------------------------------

.. toggle-header::
   :header: Click to show/hide

   Set ``MACHINE`` to ``colibri-imx7`` when setting up your work
   environment with the ``setup-environment`` script::

     MACHINE=colibri-imx7 source setup-environment [BUILDDIR]

   At the end of the build, your build artifacts will be found under
   ``deploy/images/colibri-imx7``. The artifact you will use to
   flash your microSD card is ``lmp-gateway-image-colibri-imx7.wic.gz``.

   To flash your microSD card, run::

     gunzip -f lmp-gateway-image-colibri-imx7.wic.gz
     sudo dd if=lmp-gateway-image-colibri-imx7.wic of=/dev/mmcblkX bs=4M

   Where :file:`/dev/mmcblkX` is your SD card device.

   To update U-Boot on Toradex Colibri iMX7D 1GB eMMC:

   #. From the U-Boot prompt, update the device tree name and boot into LMP::

        Colibri iMX7 # setenv boot_targets "mmc1 mmc0 usb0 dhcp"
        Colibri iMX7 # setenv fdt_board aster
        Colibri iMX7 # run bootcmd

   #. Once booted into LMP, flash U-Boot (as root)::

        mkdir /tmp/boot
        mount /dev/mmcblk0p1 /tmp/boot
        echo 0 > /sys/block/mmcblk1boot0/force_ro
        dd if=/tmp/boot/u-boot-emmc.imx of=/dev/mmcblk1boot0 bs=512 seek=2

   #. Reboot and from the U-Boot prompt update the device tree based on
      your module (e.g. Aster)::

        Colibri iMX7 # setenv boot_targets "mmc1 mmc0 usb0 dhcp"
        Colibri iMX7 # setenv fdt_board aster
        Colibri iMX7 # saveenv
        Colibri iMX7 # reset

   #. Boot LMP and change eMMC back to read-only (as root)::

        echo 1 > /sys/block/mmcblk1boot0/force_ro

   Please see https://developer.toradex.com for additional board documentation.

i.MX 8M Mini LPD4 Evaluation Kit
--------------------------------

.. toggle-header::
   :header: Click to show/hide

   Build the manufacturing tools (mfgtools) by setting ``MACHINE`` to
   ``imx8mmevk`` and ``DISTRO`` to ``lmp-mfgtool`` when setting up
   your work environment with the ``setup-environment`` script::

     DISTRO=lmp-mfgtool MACHINE=imx8mmevk source setup-environment [BUILDDIR]
     bitbake mfgtool-files

   At the end of the build, your manufacturing build artifacts will be
   found under ``deploy/images/imx8mmevk``. The artifact you will use for
   flashing your eMMC device is ``mfgtool-files.tar.gz``.

   Build the Linux microPlatform image by setting ``MACHINE`` to
   ``imx8mmevk`` and ``DISTRO`` to ``lmp`` when setting up your work
   environment with the ``setup-environment`` script::

     DISTRO=lmp MACHINE=imx8mmevk source setup-environment [BUILDDIR]
     bitbake lmp-gateway-image

   At the end of the build, your build artifacts will be found under
   ``deploy/images/imx8mmevk``. The artifact you will use to
   flash your eMMC device is ``lmp-gateway-image-imx8mmevk.wic``.

   To flash your board, change the boot switch to download mode, connect a USB-C
   cable, turn on the board and run::

     tar -zxvf mfgtool-files.tar.gz
     cd mfgtool-files
     sed -i 's/lmp-image-imx8mmevk.wic/lmp-gateway-image-imx8mmevk.wic/g' full_image.uuu
     sudo ./uuu full_image.uuu

   Power off the board, change the boot switch back to eMMC / SDHC3 and power it
   on again.

   .. note::

      Notice that the i.MX 8M Mini LPD4-EVK is different to i.MX 8M Mini D4-EVK.
      Find more information at `NXP i.MX8 Mini`_.


SiFive HiFive Unleashed Freedom U540
------------------------------------

.. toggle-header::
   :header: Click to show/hide

   Set ``MACHINE`` to ``freedom-u540`` when setting up your work
   environment with the ``setup-environment`` script::

     MACHINE=freedom-u540 source setup-environment [BUILDDIR]

   Build the Linux microPlatform minimal image ``lmp-mini-image``
   instead of the usual ``lmp-gateway-image``, as there is no golang
   and docker support for RISC-V yet. At the end of the build, your
   build artifacts will be found under
   ``deploy/images/freedom-u540``. The artifact you will use to flash
   your microSD card is ``lmp-mini-image-freedom-u540.wic.gz``.

   To flash your microSD card, run::

     gunzip -f lmp-mini-image-freedom-u540.wic.gz
     sudo dd if=lmp-mini-image-freedom-u540.wic of=/dev/mmcblkX bs=4M

   Where :file:`/dev/mmcblkX` is your SD card device.

   Please see https://www.sifive.com/boards/hifive-unleashed/
   for additional board documentation.

Generic RISC-V 64 Machine
-------------------------

.. toggle-header::
   :header: Click to show/hide

   Set ``MACHINE`` to ``qemuriscv64`` when setting up your work
   environment with the ``setup-environment`` script::

     MACHINE=qemuriscv64 source setup-environment [BUILDDIR]

   Build the Linux microPlatform minimal image ``lmp-mini-image``
   instead of the usual ``lmp-gateway-image``, as there is no golang
   and docker support for RISC-V yet::

     bitbake lmp-mini-image

   The artifacts required by QEMU are ``bbl`` (Berkeley Boot Loader +
   Kernel + initrd) and ``lmp-mini-image-qemuriscv64.ota-ext4`` in
   ``deploy/images/qemuriscv64``.

   **Boot the generic RISC-V target with QEMU**

   At the end of the build, change directory to where the build
   artifacts are found, then copy the image to where ``runqemu``
   expects it and run it::

     cd deploy/images/qemuriscv64
     cp lmp-mini-image-qemuriscv64.ota-ext4 lmp-mini-image-qemuriscv64.ext4
     runqemu nographic slirp qemuparams="-m 512"

   Please see
   https://wiki.qemu.org/Documentation/Networking#User_Networking_.28SLIRP.29
   for information and additional details on networking restrictions.

   **SSH into guest**

   You can SSH into the RISC-V 64 guest by using the port forwarded to
   the RISC-V 64 guest::

     ssh -p 2222 fio@localhost

   Please see https://wiki.qemu.org/Documentation/Platforms/RISCV for additional
   information.


.. _NXP i.MX8 Mini:
   https://www.nxp.com/design/development-boards/i.mx-evaluation-and-development-boards/evaluation-kit-for-the-i.mx-8m-mini-applications-processor:8MMINILPD4-EVK
