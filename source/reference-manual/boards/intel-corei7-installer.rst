.. _ref-rm_board_intel-corei7-64:

Intel Core i7 CPU (and later): Installing to Internal Flash
===========================================================

To install the :term:`system image` onto an internal flash drive, enable  the :ref:`ref-linux-wic-installer`.
Next, follow these instructions to flash the installer onto a USB stick/SD Card.

.. include:: generic-prepare.rst

Flashing
--------

Flash ``lmp-factory-image-intel-corei7-64.wic.gz`` onto a USB Stick/SD Card.
This contains the :term:`system image` installer.

.. include:: generic-flashing.rst

Most Intel devices will boot from USB automatically.
If the device does not, hold **F12** when the device boots.
This will allow you to select the USB from a system-specific boot menu.

If **F12** does not work for you, check your device's documentation for how to bring up the boot menu.

Booting the Installer
---------------------

.. warning::

   The following steps will delete anything already on the selected device.

After boot, wait until the message:

.. prompt::

    Please select an install target or press n to exit (sda sdc)
    sda

Type the name of the device you want to install the :term:`system image`. 
In the example above, the device used was ``sda``.

After selecting the device, you will be asked if you want to proceed.
Type `y` to continue the installation.

.. prompt::

    Installation successful. Remove your installation media and press Enter to reboot.

Follow the instructions and reboot the device.
