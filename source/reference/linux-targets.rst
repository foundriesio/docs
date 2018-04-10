.. highlight:: sh

.. _ref-linux-targets:

Additional Linux microPlatform Targets
======================================

This section provides information on running the Linux microPlatform
for other targets. It is provided on a best-effort basis.

Prebuilt Binaries
-----------------

Several boards have reference builds provided by Open Source Foundries
in the latest Linux microPlatform release, available at
https://foundries.io/mp/lmp/latest/artifacts/.

Please note that these builds are provided for reference in hopes they
are useful; not all receive equal testing.

BeagleBone Black
----------------

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

Please see http://mediawiki.compulab.com/w/index.php5/IOT-GATE-iMX7:_Getting_Started
for additional board documentation.

Toradex Colibri iMX7D (Aster)
-----------------------------

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

     Colibri iMX7 # setenv fdt_board emmc-aster
     Colibri iMX7 # run bootcmd

#. Once booted into LMP, flash U-Boot (as root)::

     mkdir /tmp/boot
     mount /dev/mmcblk0p1 /tmp/boot
     echo 0 > /sys/block/mmcblk2boot0/force_ro
     dd if=/tmp/boot/u-boot-emmc.imx of=/dev/mmcblk2boot0 bs=512 seek=2

#. Reboot and from the U-Boot prompt update the device tree based on
   your module (e.g. Aster)::

     Colibri iMX7 # setenv fdt_board emmc-aster
     Colibri iMX7 # saveenv
     Colibri iMX7 # reset

#. Boot LMP and change eMMC back to read-only (as root)::

     echo 1 > /sys/block/mmcblk2boot0/force_ro

Please see https://developer.toradex.com for additional board documentation.

HummingBoard 2
--------------

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

Please see https://wiki.solid-run.com/doku.php?id=products:imx6:hummingboard
for additional board documentation.

96Boards HiKey
--------------

Set ``MACHINE`` to ``hikey`` when setting up your work environment
with the ``setup-environment`` script::

  MACHINE=hikey source setup-environment [BUILDDIR]

At the end of the build, your build artifacts will be found under
``deploy/images/hikey``.

To convert the rootfs to a fastboot-compatible format, run::

  gunzip -f lmp-gateway-image-hikey.ext4.gz
  ext2simg -v lmp-gateway-image-hikey.ext4 lmp-gateway-image-hikey.img

To flash your HiKey over micro-USB::

  fastboot flash boot boot-hikey.uefi.img
  fastboot flash system lmp-gateway-image-hikey.img

Please see https://www.96boards.org/documentation/consumer/hikey/
for additional board documentation.

96Boards DragonBoard 410c
-------------------------

Set ``MACHINE`` to ``dragonboard-410c`` when setting up your work
environment with the ``setup-environment`` script::

  MACHINE=dragonboard-410c source setup-environment [BUILDDIR]

At the end of the build, your build artifacts will be found under
``deploy/images/dragonboard-410c``. The artifact you will use to
flash your microSD card is ``lmp-gateway-image-cdragonboard-410c.wic.gz``.

To flash your microSD card, run::

  gunzip -f lmp-gateway-image-dragonboard-410c.wic.gz
  sudo dd if=lmp-gateway-image-dragonboard-410c.wic of=/dev/mmcblkX bs=4M

Where :file:`/dev/mmcblkX` is your SD card device.

U-Boot is provided as part of the fastboot boot image.

To flash your DragonBoard 410c boot image over micro-USB::

  fastboot flash boot boot-dragonboard-410c.img

Please see https://www.96boards.org/documentation/consumer/dragonboard410c/
for additional board documentation.

96Boards DragonBoard 820c
-------------------------

Set ``MACHINE`` to ``dragonboard-820c`` when setting up your work
environment with the ``setup-environment`` script::

  MACHINE=dragonboard-820c source setup-environment [BUILDDIR]

At the end of the build, your build artifacts will be found under
``deploy/images/dragonboard-820c``. The artifact you will use to
flash your microSD card is ``lmp-gateway-image-cdragonboard-820c.wic.gz``.

To flash your microSD card, run::

  gunzip -f lmp-gateway-image-dragonboard-820c.wic.gz
  sudo dd if=lmp-gateway-image-dragonboard-820c.wic of=/dev/mmcblkX bs=4M

Where :file:`/dev/mmcblkX` is your SD card device.

U-Boot is provided as part of the fastboot boot image.

To flash your DragonBoard 820c boot image over micro-USB::

  fastboot flash boot boot-dragonboard-820c.img

Please see https://www.96boards.org/documentation/consumer/dragonboard820c/
for additional board documentation.
