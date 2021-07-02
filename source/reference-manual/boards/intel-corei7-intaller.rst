Intel Core i7 CPU (and later) - Installer
=========================================

To install the :term:`system image` into an internal flash drive, you should enable 
the :ref:`ref-linux-wic-installer`.

With the WIC installer enabled, follow the instructions to flash the installer into a USB stick.

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

Booting installer
-----------------

.. warning::

   The following steps will delete all your programs, documents, photos, music, and any other files on the selected device.

After boot, wait until the message:

.. prompt::

    Please select an install target or press n to exit (sda sdc)
    sda

Type the name of the device you want to install the :term:`system image`. 
In the example above, the device used was ``sda``.

Right after select the device, the prompt will ask if you want to proceed:

.. prompt::

    Proceed anyway? (y,N)

Type ``y`` if you want to continue the installation.

When the installation completes, the following message will be displayed:

.. prompt::

    Installation successful. Remove your installation media and press Enter to reboot.

Follow the instructions and reboot the device.