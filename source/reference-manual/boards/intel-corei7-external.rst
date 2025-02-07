Intel Core i7 CPU (and later): Booting From External Flash
===========================================================

This section explains how to boot the :term:`system image` a USB stick or SD Card.

.. include:: generic-prepare.rst

Flashing
--------

Flash ``lmp-factory-image-intel-corei7-64.rootfs.wic.gz`` to a USB stick/SD Card.
This contains the bootable :term:`system image`.

.. include:: generic-flashing.rst

Most Intel devices will boot from USB automatically.
If the device does not,  hold ``F12`` when the device boots.
This will allow you to select the USB from a system-specific boot menu.

If ``F12`` does not work for you, check your device's documentation for how to bring up the boot menu.
