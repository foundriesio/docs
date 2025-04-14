.. _ref-rm_board_beaglebone-yocto:

Beaglebone Black
================

.. note:: 
   This tutorial applies to both the Beaglebone Black and Beaglebone Black Wireless.

.. include:: generic-prepare.rst

Flashing
--------

Flash your Factory image to an SD Card.
This contains the bootable :term:`system image`.

By default, the Beaglebone Black boots from internal eMMC.
To avoid this, you can either:

   * Press the **S2** button before powering on.
     This causes the boot sequence to start from SPI0, followed by SD card.
     If the board is not connected to any SPI boot source, the SD card should be used.

   * Erase the eMMC, or disable the 'bootable' flag on the eMMC boot partition.

.. include:: generic-flashing.rst
