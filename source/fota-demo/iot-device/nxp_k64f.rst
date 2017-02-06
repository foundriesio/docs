.. highlight:: sh

.. _iot-device-nxp_k64f:

IoT Device: NXP FRDM-K64F
=========================

From here, you can set up a FRDM-K64F device to receive FOTA updates.

.. contents::
   :local:

Flashing Tool
-------------

- pyOCD
  - URL: https://github.com/mbedmicro/pyOCD
  - This is used when flashing FRDM-K64F.

Device Flash layout
-------------------

- **bootloader**
    - Flash: 0x00000000 - 0x00010000 (In this setup, bootloader is the mcuboot zephyr.bin image)
- **FOTA app state information**
    - Flash: 0x00010000 - 0x00017FFF
    - Data storage area, currently unused
- **Currently Unused**
    - Flash: 0x00018000 - 0x0001FFFF
- **Application, Bank0**
    - Flash: 0x00020000 - 0x0003FFFF
- **Application, Bank1**
    - Flash: 0x00040000 - 0x0005FFFF
    - Scratch Flash:  0x00060000 - 0x0007FFFF (Scratch is used when copy an application from Bank1 to Bank0 during mcuboot OTA.)
- **Currently Unused**
    - Flash: 0x00080000 - 0x000FFFFF
    - **The flash layout for K64F leaves 512k unused flash – this is for testing compatibility with smaller HW devices such as Carbon.**

Build Firmware Binaries
-----------------------

Using the repositories you checked out earlier, build both a
bootloader (mcuboot) and the Linaro FOTA Zephyr application.::

    # Establish Zephyr environment
    $ cd <zephyr-project>
    $ export ZEPHYR_SDK_INSTALL_DIR=/path/to/your/zephyr-sdk
    $ export ZEPHYR_GCC_VARIANT=zephyr
    $ . zephyr-env.sh


    # Bootloader
    $ cd <mcuboot>
    $ make BOARD=frdm_k64f


    # Linaro FOTA app
    $ cd <zephyr-fota-hawkbit>
    $ make CONF_FILE=prj_frdm_k64f.conf BOARD=frdm_k64f
    $ cd <zephyr-utils>
    $ python zep2newt.py --bin <zephyr-fota-hawkbit>/outdir/frdm_k64f/zephyr.bin \
                         --key root.pem --sig RSA --vtoff 0x200 --word-size 8 \
                         --out linaro_fota-frdm_k64f.signed.bin

Flash K64F with Firmware Binaries
---------------------------------

Flash the bootloader and FOTA application binaries to the K64F using
pyOCD, after plugging the K64F into your system via USB. ::

    # Bootloader
    $ cd <mcuboot>
    $ pyocd-flashtool -ce outdir/frdm_k64f/zephyr.bin

    # Signed Linaro FOTA app
    $ cd <zephyr-utils>
    $ pyocd-flashtool -se --address 0x20000 linaro_fota-frdm_k64f.signed.bin
