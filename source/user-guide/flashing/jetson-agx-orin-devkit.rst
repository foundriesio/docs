.. _ref-rm_board_jetson-agx-orin-devkit:

Jetson AGX Orin Developer Kit
=============================

This page covers flashing a Jetson AGX Orin Developer Kit with LmP artifacts.

Preparation
-----------

1. In your Factory, click on the latest ``platform`` build.

2. Expand the run for ``jetson-agx-orin-devkit``.
   Find ``lmp-factory-image-jetson-agx-orin-devkit.tegraflash.tar.gz`` and download the file.

3. Unzip the file:

   .. code-block:: console
   
   $ tar -xvf lmp-factory-image-jetson-agx-orin-devkit.tegraflash.tar.gz

The script used for flashing is ``doflash.sh``.

Hardware Preparation
--------------------

Set the board to boot into recovery mode:

.. figure:: /_static/boards/jetson-agx-orin-devkit.png
     :width: 600
     :align: center

     jetson-agx-orin-devkit

1. Connect the USB cable in the base board Type-C connector (**10**) to the host machine.

2. While holding down the force recovery button, either press the Reset button (if already powered), or the Power button.
   Release both buttons.

   To check if the board is in recovery mode, ``lsusb`` can be used.
   Check if a device from vendor ``0955`` (NVIDIA) is available

   .. code-block:: console

       $ lsusb | grep 0955
       Bus 001 Device 014: ID 0955:7023 NVIDIA Corp. APX

   This device is only available when the board successfully boots in recovery mode.

3. **OPTIONAL**: For UART output, connect a USB cable from the base board's USB Micro B connector (**9**), to the host machine.

Flashing
--------

1. With the board powered in recovery mode, flash the board:

  .. code-block:: console

     $ sudo ./doflash.sh

  This can take a few minutes to complete. The process can be watched from the host console or UART output.

2. Once the flashing procedure finishes, reset the board to boot the installed LmP image.
