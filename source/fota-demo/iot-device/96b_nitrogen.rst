.. highlight:: sh

.. _iot-device-96b_nitrogen:

IoT Device: 96Boards Nitrogen
=============================

From here, you can set up a 96Boards Nitrogen device to receive FOTA
updates.

.. contents::
   :local:

Flashing Tools
--------------

- **nrfjprog**
  - URL: https://github.com/NordicSemiconductor/nrfjprog
  - Nordic Semiconductor provides this tool for working with their devices.
- **pyOCD**
  - URL: https://github.com/mbedmicro/pyOCD
  - This is used when flashing 96boards Nitrogen.

Device Flash layout
-------------------

- **bootloader**
  - Flash: 0x0 - 0x7FFF
  - In this setup, the bootloader is the mcuboot zephyr.bin image
- **Application, Bank0**
  - Flash: 0x8000 - 0x41FFF
  - Any application, Zephyr is used here.
- **Application, Bank1**
  - Flash: 0x42000 - 0x7BFFF
- **Scratch**
  - Flash: 0x7C000 - 0x7CFFF
  - Scratch is used when copying an application from Bank1 to Bank0 during mcuboot OTA.
- **FOTA app state information**
  - Flash: 0x7D000 - 0x80000

Build Firmware Binaries
-----------------------

Using the repositories you checked out earlier, build both a
bootloader (mcuboot) and the Linaro FOTA Zephyr application. ::

    # Establish Zephyr environment
    cd <zephyr>
    export ZEPHYR_SDK_INSTALL_DIR=/path/to/your/zephyr-sdk
    export ZEPHYR_GCC_VARIANT=zephyr
    . zephyr-env.sh

    # Bootloader
    cd <mcuboot>
    make BOARD=96b_nitrogen

    # Linaro FOTA app
    cd <zephyr-fota-hawkbit>
    make CONF_FILE=prj_nrf52.conf BOARD=96b_nitrogen

    cd <zephyr-utils>
    python zep2newt.py --bin <zephyr-fota-hawkbit>/outdir/96b_nitrogen/zephyr.bin \
                       --key root.pem --sig RSA --vtoff 0x100 --word-size 4 \
                       --out linaro_fota-nitrogen.signed.bin

Flash Nitrogen with Firmware Binaries
-------------------------------------

Flash the bootloader and FOTA application binaries to your Nitrogen
using pyOCD, after plugging the Nitrogen into your system via USB. ::

    # Bootloader
    cd <mcuboot>
    pyocd-flashtool -d debug -t nrf52 -ce -a 0x0 outdir/96b_nitrogen/zephyr.bin

    # Signed Linaro FOTA app
    cd <zephyr-utils>
    pyocd-flashtool -d debug -t nrf52 -a 0x8000 linaro_fota-nitrogen.signed.bin
