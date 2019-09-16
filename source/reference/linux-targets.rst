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

    Please see https://minnowboard.org/tutorials/getting-started-minnowboard-turbot-dual-e
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

IOT-GATE-iMX7
-------------

.. toggle-header::
   :header: Click to show/hide

   Set ``MACHINE`` to ``cl-som-imx7`` when setting up your work
   environment with the ``setup-environment`` script::

     MACHINE=cl-som-imx7 source setup-environment [BUILDDIR]

   At the end of the build, your build artifacts will be found under
   ``deploy/images/cl-som-imx7``. The artifact you will use to
   flash your microSD card is ``lmp-gateway-image-cl-som-imx7.wic.gz``.

   To flash your microSD card, run::

     gunzip -f lmp-gateway-image-cl-som-imx7.wic.gz
     sudo dd if=lmp-gateway-image-cl-som-imx7.wic of=/dev/mmcblkX bs=4M

   Where :file:`/dev/mmcblkX` is your SD card device.

   Close the E2 jumper (near the audio socket) to boot from the SD card.

   Update the U-Boot environment based on latest U-Boot:

   #. From the U-Boot prompt, erase default environment and save the new environment::

        CL-SOM-iMX7 # env default -a
        CL-SOM-iMX7 # saveenv

   #. Then set fdtfile in case EEPROM has an invalid product name::

        CL-SOM-iMX7 # setenv fdtfile imx7d-sbc-iot-imx7.dtb
        CL-SOM-iMX7 # saveenv

   Please see https://www.mediawiki.compulab.com/index.php/IOT-GATE-iMX7:_Getting_Started
   for additional board documentation.

Toradex Colibri iMX7D (Aster)
-----------------------------

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

   To update U-Boot on Toradex Colibri iMX7D 512MB NAND:

   #. From the U-Boot prompt::

        Colibri iMX7 # run setupdate
        Colibri iMX7 # run update

   #. Reboot and from the U-Boot prompt update the device tree based on
      your module (e.g. Aster)::

        Colibri iMX7 # setenv fdt_board aster
        Colibri iMX7 # saveenv
        Colibri iMX7 # reset

   To update U-Boot on Toradex Colibri iMX7D 1GB eMMC:

   #. From the U-Boot prompt, update the device tree name and boot into LMP::

        Colibri iMX7 # setenv boot_targets "mmc1 mmc0 usb0 dhcp"
        Colibri iMX7 # setenv fdt_board aster
        Colibri iMX7 # run bootcmd

   #. Once booted into LMP, flash U-Boot (as root)::

        mkdir /tmp/boot
        mount /dev/mmcblk0p1 /tmp/boot
        echo 0 > /sys/block/mmcblk2boot0/force_ro
        dd if=/tmp/boot/u-boot-emmc.imx of=/dev/mmcblk2boot0 bs=512 seek=2

   #. Reboot and from the U-Boot prompt update the device tree based on
      your module (e.g. Aster)::

        Colibri iMX7 # setenv boot_targets "mmc1 mmc0 usb0 dhcp"
        Colibri iMX7 # setenv fdt_board aster
        Colibri iMX7 # saveenv
        Colibri iMX7 # reset

   #. Boot LMP and change eMMC back to read-only (as root)::

        echo 1 > /sys/block/mmcblk2boot0/force_ro

   Please see https://developer.toradex.com for additional board documentation.

HummingBoard 2
--------------

.. toggle-header::
   :header: Click to show/hide

   Set ``MACHINE`` to ``cubox-i`` when setting up your work environment
   with the setup-environment script::

     MACHINE=cubox-i source setup-environment [BUILDDIR]

   At the end of the build, your build artifacts will be found under
   ``deploy/images/cubox-i``. The artifact you will use to
   flash your microSD card is ``lmp-gateway-image-cubox-i.wic.gz``.

   To flash your microSD card, run::

     gunzip -f lmp-gateway-image-cubox-i.wic.gz
     sudo dd if=lmp-gateway-image-cubox-i.wic of=/dev/mmcblkX bs=4M

   Where :file:`/dev/mmcblkX` is your SD card device.

   Please see https://developer.solid-run.com/products/hummingboard-gate-edge/
   for additional board documentation.

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
