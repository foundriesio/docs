Intel Core i7 CPU (and later) - External Flash
==============================================

This section explains how to boot the :term:`system image` from an external flash like a USB stick or SD Card.

.. include:: generic-prepare.rst

Flashing
--------

Now, flash the ``lmp-factory-image-intel-corei7-64.wic.gz`` retrieved from the previous section
to a flash drive. This contains the :term:`system image` that the device will boot.

.. include:: generic-flashing.rst

1. Remove the flash drive from the host and plug it into the Intel board.

2. Power on the board and select from the boot menu the flash drive.

Most Intel devices will boot from USB automatically. If the device doesn't automatically boot from USB, 
try holding ``F12`` when your device first boots. This will allow you to select the USB device from a system-specific boot menu.

If ``F12`` doesn't work for you, check your device documentation to find how to bring up the boot menu.