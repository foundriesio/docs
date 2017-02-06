.. _iot-devices:

IoT Devices
===========

The FOTA Demonstration System supports a variety of boards which can
be used as IoT Devices. This section contains setup and usage guides
for the available devices.

From here, you can follow instructions to set up an IoT Device to
which you can perform FOTA updates using the hawkBit server instance
you set up earlier.

Get the Source
--------------

To get started, clone the following repositories, then check out the
relevant commits. These contain firmware and associated tools you will
build and flash to your IoT Device.

- **Zephyr**:
     - Getting started: https://www.zephyrproject.org/doc/getting_started/getting_started.html
     - URL: https://github.com/Linaro/zephyr
     - Branch: master-upstream-dev
- **mcuboot**
     - URL: https://github.com/Linaro/mcuboot/
     - Common bootloader (Mynewt/Zephyr) that supports dual-bank and
       signed updates
     - Branch: master-upstream-dev
- **zephyr-utils**
     - Include tools that can create (both signed and unsigned) images
       that will work with mcuboot
     - URL: https://github.com/Linaro/zephyr-utils
     - Branch: master
- **zephyr-fota-hawkbit**
     - Linaro firmware over the air update (FOTA) Zephyr application,
       using hawkBit as backend process manager
     - URL: https://github.com/Linaro/zephyr-fota-hawkbit
     -  Branch: master

Set Up Your Device
------------------

Now use a device-specific guide to set up your IoT Device.

.. toctree::
   :maxdepth: 2

   96b_nitrogen
   nxp_k64f
   96b_carbon
