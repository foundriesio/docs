.. _ref-rm_board_jetson-agx-xavier-devkit:

Jetson AGX Xavier Developer Kit
===============================

This page shows how to flash a Jetson AGX Xavier Developer Kit with LmP artifacts.

Preparation
-----------

1. On your factory, click on the latest ``platform-devel`` build:

  .. figure:: /_static/boards/generic-steps-1.png
     :width: 769
     :align: center

2. Expand the run for ``jetson-agx-xavier-devkit`` and look for the **lmp-factory-image-jetson-agx-xavier-devkit.tegraflash.tar.gz**
artifact:

  .. figure:: /_static/boards/jetson-agx-xavier-devkit_artifacts.png

3. Unzip the downloaded file:

  .. prompt:: bash host:~$, auto

     host:~$ tar -xvf lmp-factory-image-jetson-agx-xavier-devkit.tegraflash.tar.gz

The script used for flashing is **doflash.sh**.

Hardware Preparation
--------------------

Set up the board to boot into recovery mode:

.. figure:: /_static/boards/jetson-agx-xavier-devkit.png
     :width: 600
     :align: center

     jetson-agx-xavier-devkit

1. Connect the USB cable in the base board Type-C connector (J512) to the host machine.

2. Press and hold down the Force Recovery button, then either press the Reset button (if already powered) or press the Power button, releasing both buttons in the end.

   To check if the board is in recovery mode ``lsusb`` can be used to check if a device from vendor ``0955`` (NVIDIA) is available::

       host:~$ lsusb | grep 0955
       Bus 001 Device 013: ID 0955:7019 NVIDIA Corp. APX

   This device is only available when the board successfully booted in recovery mode.

3. **OPTIONAL:** For UART output connect a USB cable in the base board USB Micro B connector (J501) to the host machine.

Flashing
--------

1. With the board powered in recovery mode, flash the board:

  .. prompt:: bash host:~$, auto

    host:~$ sudo ./doflash.sh

  This can take a few minutes to complete. The process can be watched from the host console or UART output.

2. Once the flashing procedure finishes, reset the board to boot the installed LmP image.
