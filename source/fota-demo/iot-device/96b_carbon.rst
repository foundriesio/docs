.. highlight:: sh

.. _iot-device-96b_carbon:

IoT Device: 96Boards Carbon
===========================

From here, you can set up a 96Boards Carbon device to receive FOTA
updates.

.. contents::
   :local:

Flashing tools
--------------

- stlink
    - URL: https://github.com/texane/stlink (on some distros you can just get it using your package manager)
    - This can be used when flashing STMicro based devices.
- dfu-util
    - URL: git://git.code.sf.net/p/dfu-util/dfu-util
    - This is used when flashing 96boards Carbon

Device Flash Layout
-------------------

- **bootloader**
    - Flash: 0x08000000 - 0x08007FFF
    - In this setup, bootloader is the mcuboot zephyr.bin image
- **FOTA app state information**
    - Flash: 0x08008000 - 0x0800FFFF
    - Data storage area, currently unused
- **Application, Bank0**
    - Flash: 0x08020000 - 0x0803FFF7
- **Application, Bank1**
    - Flash: 0x08040000 - 0x0805FFF7
- **Scratch**
    - Flash:  0x08060000 - 0x0807FFF7
    - Scratch is used when copy an application from Bank1 to Bank0 during mcuboot OTA.

Build Firmware Binaries
-----------------------

Using the repositories you checked out earlier, build both a bootloader (mcuboot) and the Linaro FOTA Zephyr application.::

    # Establish Zephyr environment
    cd <zephyr-project>
    export ZEPHYR_SDK_INSTALL_DIR=/path/to/your/zephyr-sdk
    export ZEPHYR_GCC_VARIANT=zephyr
    . zephyr-env.sh

    # Bootloader
    cd <mcuboot>
    make BOARD=96b_carbon

    # Linaro FOTA app
    cd <zephyr-fota-hawkbit>
    make CONF_FILE=prj_stm32f4.conf BOARD=96b_carbon
    cd <zephyr-utils>
    python zep2newt.py --bin <zephyr-fota-hawkbit>/outdir/96b_carbon/zephyr.bin --key root.pem --sig RSA --vtoff 0x100 --out linaro_fota-carbon.signed.bin

Flash Carbon with Firmware Binaries
-----------------------------------

Flash the bootloader and FOTA application binaries to your Carbon
using dfu-util, after plugging the Carbon into your system via the
"OTG" USB connector. The "BOOT0" button on Carbon must be held down
while power is applied to the board.  You can release BOOT0 after the
board powers up. For more information, see Carbon's documentation. ::

    # Bootloader
    cd <mcuboot>
    sudo dfu-util -d [0483:df11] -a 0 -s 0x08000000:force:mass-erase -D outdir/96b_carbon/zephyr.bin


    # Linaro FOTA app
    cd <zephyr-utils>
    sudo dfu-util -d [0483:df11] -a 0 -D linaro_fota-carbon.signed.bin -s 0x08020000
