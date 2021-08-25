Intel Core i7 CPU (and later) - Booting from External Flash
===========================================================

This section explains how to boot the :term:`system image` from an external flash like a USB stick or SD Card.

.. include:: generic-prepare.rst

Flashing
--------

Now, flash the ``lmp-factory-image-intel-corei7-64.wic.gz`` retrieved from the
previous section to a USB Stick/SD Card. This contains the :term:`system image` that the
device will boot.

.. include:: generic-flashing.rst

Most Intel devices will boot from USB automatically. If the device doesn't automatically boot from USB,
try holding ``F12`` when your device first boots. This will allow you to select the USB from a system-specific boot menu.

If ``F12`` doesn't work for you, check your device documentation to find how to bring up the boot menu.