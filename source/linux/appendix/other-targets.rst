.. highlight:: sh

.. _lmp-appendix-other-targets:

Appendix: Additional Linux microPlatform Targets
================================================

This section provides information on running the Linux microPlatform
for other targets. It is provided on a best-effort basis.

Prebuilt Binaries
-----------------

Several boards have reference builds provided by Open Source Foundries
in the latest Linux microPlatform release, available at
https://foundries.io/r/.

Please note that these builds are provided for reference in hopes they
are useful; not all receive equal testing.

BeagleBone Black
----------------

Set ``MACHINE`` to ``beaglebone`` when setting up your work
environment with the ``setup-environment`` script::

  MACHINE=beaglebone source setup-environment [BUILDDIR]

At the end of the build, your build artifacts will be found under
``tmp-lmp-glibc/deploy/images/beaglebone``. The artifact you will use to
flash your microSD card is ``lmp-gateway-image-beaglebone.wic.gz``.

To flash your microSD card, run::

  gunzip -f lmp-gateway-image-beaglebone.wic.gz
  sudo dd if=lmp-gateway-image-beaglebone.wic of=/dev/mmcblkX bs=4M

Where :file:`/dev/mmcblkX` is your SD card device.

Please see https://elinux.org/Beagleboard:BeagleBoneBlack for additional
board documentation.

HummingBoard 2
--------------

Set ``MACHINE`` to ``cubox-i`` when setting up your work environment
with the setup-environment script::

  MACHINE=cubox-i source setup-environment [BUILDDIR]

At the end of the build, your build artifacts will be found under
``tmp-lmp-glibc/deploy/images/cubox-i``. The artifact you will use to
flash your microSD card is ``lmp-gateway-image-cubox-i.wic.gz``.

To flash your microSD card, run::

  gunzip -f lmp-gateway-image-cubox-i.wic.gz
  sudo dd if=lmp-gateway-image-cubox-i.wic of=/dev/mmcblkX bs=4M

Where :file:`/dev/mmcblkX` is your SD card device.

Please see https://wiki.solid-run.com/doku.php?id=products:imx6:hummingboard
for additional board documentation.

96Boards HiKey
--------------

.. todo:: reference or move the getting-started etc. pictures here

Set ``MACHINE`` to ``hikey`` when setting up your work environment
with the ``setup-environment`` script::

  MACHINE=hikey source setup-environment [BUILDDIR]

At the end of the build, your build artifacts will be found under
``tmp-lmp-glibc/deploy/images/hikey``.

To convert the rootfs to a fastboot-compatible format, run::

  gunzip -f lmp-gateway-image-hikey.ext4.gz
  ext2simg -v lmp-gateway-image-hikey.ext4 lmp-gateway-image-hikey.img

To flash your HiKey over micro-USB::

  fastboot flash boot boot-hikey.uefi.img
  fastboot flash system lmp-gateway-image-hikey.img

Please see https://github.com/96boards/documentation/tree/master/ConsumerEdition/HiKey
for additional board documentation.

96Boards Dragonboard 410c
-------------------------

Set ``MACHINE`` to ``dragonboard-410c`` when setting up your work
environment with the ``setup-environment`` script::

  MACHINE=dragonboard-410c source setup-environment [BUILDDIR]

At the end of the build, your build artifacts will be found under
``tmp-lmp-glibc/deploy/images/dragonboard-410c``.

To convert the rootfs to a fastboot-compatible format::

  gunzip -f lmp-gateway-image-dragonboard-410c.ext4.gz
  ext2simg -v lmp-gateway-image-dragonboard-410c.ext4 lmp-gateway-image-dragonboard-410c.img

To flash your Dragonboard 410c over micro-USB::

  fastboot flash boot boot.img
  fastboot flash rootfs lmp-gateway-image-dragonboard-410c.img

Please see https://github.com/96boards/documentation/tree/master/ConsumerEdition/DragonBoard-410c
for additional board documentation.
