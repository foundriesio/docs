.. highlight:: sh

.. _iot-device-96b_nitrogen:

IoT Device: 96Boards Nitrogen
=============================

From here, you can set up a 96Boards Nitrogen device to receive FOTA
updates.

.. contents::
   :local:

Choose Your Method
------------------

Using Released Binaries
~~~~~~~~~~~~~~~~~~~~~~~

TODO: add links to builds.lt.o

Once you have the binaries, install the flashing tool on your system,
and follow the instructions to flash binaries.

Building From Source
~~~~~~~~~~~~~~~~~~~~

If you're going to build from source instead, follow instructions on
:ref:`IoT Devices <iot-devices-build-source>` to clone the relevant
repositories and set up your build environment, then build both a
bootloader (mcuboot) and the Linaro FOTA Zephyr application. ::

      # Establish Zephyr environment
      cd <zephyr>
      export ZEPHYR_SDK_INSTALL_DIR=/path/to/your/zephyr-sdk
      export ZEPHYR_GCC_VARIANT=zephyr
      . zephyr-env.sh

      # Linaro FOTA app
      cd <zephyr-fota-hawkbit>
      make CONF_FILE=prj_nrf52.conf BOARD=96b_nitrogen

      # Build bootloader, and sign FOTA app built in previous step.
      cd <mcuboot>
      make BOARD=96b_nitrogen
      cp outdir/96b_nitrogen/zephyr.bin mcuboot-96b_nitrogen.bin
      ./scripts/zep2newt.py --bin <zephyr-fota-hawkbit>/outdir/96b_nitrogen/zephyr.bin \
                            --key root-rsa-2048.pem --sig RSA  --vtoff 0x100 \
                            --out linaro_fota-96b_nitrogen.signed.bin \
                            --word-size 4 --pad 0x3a000 --bit

Flashing Tool
-------------

Next, install pyOCD to flash images onto the Nitrogen board.

https://github.com/mbedmicro/pyOCD

Flash Nitrogen with Firmware Binaries
-------------------------------------

Flash the bootloader and FOTA application binaries to your Nitrogen
using pyOCD, after plugging the Nitrogen into your system via USB. ::

    # Bootloader and signed FOTA app. Run these commands from:
    # - the directory your downloaded binaries are stored, if you used released binaries.
    # - the mcuboot directory, if you built from source.
    sudo pyocd-flashtool -d debug -t nrf52 -ce -a 0x0 mcuboot-96b_nitrogen.bin
    sudo pyocd-flashtool -d debug -t nrf52 -a 0x8000 linaro_fota-96b_nitrogen.signed.bin

Device Flash layout
-------------------

This informational section describes the flash sector layout you have
set up using these instructions.

- **bootloader**

  - Flash: 0x0 - 0x7FFF
  - In this setup, the bootloader is the mcuboot zephyr.bin image

- **Application, Bank0**

  - Flash: 0x8000 - 0x41FFF
  - Any application; the FOTA app is used here.

- **Application, Bank1**

  - Flash: 0x42000 - 0x7BFFF
  - Used for storing an updated FOTA app before copying it to bank 0.

- **Scratch**

  - Flash: 0x7C000 - 0x7CFFF
  - Scratch is used when copying an application from Bank1 to Bank0
    during mcuboot OTA.

- **FOTA app state information**

  - Flash: 0x7D000 - 0x80000
