.. highlight:: sh

.. _iot-device-96b_carbon:

IoT Device: 96Boards Carbon
===========================

From here, you can set up a 96Boards Carbon device to receive FOTA
updates.

.. contents::
   :local:

Choose Your Method
------------------

Using Released Binaries
~~~~~~~~~~~~~~~~~~~~~~~

TODO: add links to builds.lt.o

Once you have the binaries, install the flashing tools on your system,
and follow the instructions to flash binaries.

Building From Source
~~~~~~~~~~~~~~~~~~~~

If you're going to build from source instead, follow instructions on
:ref:`IoT Devices <iot-devices-build-source>` to clone the relevant
repositories and set up your build environment, then build both a
bootloader (mcuboot) and the Linaro FOTA Zephyr application. ::

    # Establish Zephyr environment and build NRF51 binary
    cd <zephyr-project>
    export ZEPHYR_SDK_INSTALL_DIR=/path/to/your/zephyr-sdk
    export ZEPHYR_GCC_VARIANT=zephyr
    . zephyr-env.sh
    make -C samples/bluetooth/hci_spi/ CONF_FILE=96b_carbon_nrf51.conf BOARD=96b_carbon_nrf51

    # Linaro FOTA app
    cd <zephyr-fota-hawkbit>
    make CONF_FILE=prj_stm32f4.conf BOARD=96b_carbon

    # Build bootloader, and sign FOTA app built in previous step.
    cd <mcuboot>
    make BOARD=96b_carbon
    cp outdir/96b_carbon/zephyr.bin mcuboot-96b_carbon.bin
    cp <zephyr>/samples/bluetooth/hci_spi/outdir/96b_carbon_nrf51/zephyr.bin 96b_carbon_nrf51.bin
    ./scripts/zep2newt.py --bin <zephyr-fota-hawkbit>/outdir/96b_carbon/zephyr.bin \
                                --key root-rsa-2048.pem --sig RSA --vtoff 0x100 \
                                --out linaro_fota-96b_carbon.signed.bin \
                                --word-size 1 --pad 0x20000 --bit

Flashing tools
--------------

- **stlink**
    - URL: https://github.com/texane/stlink (on some distros you can just get it using your package manager)
    - This can be used when flashing STMicro based devices.
- **dfu-util**
    - URL: http://dfu-util.sourceforge.net/
    - Git Repository: git://git.code.sf.net/p/dfu-util/dfu-util
    - This is used when flashing 96boards Carbon
- Flashing the Carbon NRF51 device requires an external, SWD flashing
  tool. See `Flash Carbon NRF51 with Firmware Binaries`_.

Flash Carbon with Firmware Binaries
-----------------------------------

There are two chips on the Carbon that need firmware, an STM32 and an
NRF51. The STM32 runs the bootloader and main FOTA application. The
NRF51 is a support chip which allows the application on the STM32 to
communicate with the IoT Gateway via Bluetooth.

Flash Carbon STM32 with Firmware Binaries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first chip you will flash is the STM32 chip, which will contain
the bootloader and FOTA application.

Flash the bootloader and FOTA application binaries to your Carbon
using dfu-util, after plugging the Carbon into your system via the
"OTG" USB connector. The "BOOT0" button on Carbon must be held down
while power is applied to the board.  You can release BOOT0 after the
board powers up. For more information, see `Carbon's documentation
<http://www.96boards.org/documentation/IoTEdition/Carbon/GettingStarted/README.md/>`_. ::

    # Bootloader and signed FOTA app. Run these commands from:
    # - the directory your downloaded binaries are stored, if you used released binaries.
    # - the directory the binaries were built (linaro_fota and mcuboot)
    sudo dfu-util -d [0483:df11] -a 0 -s 0x08000000:force:mass-erase -D mcuboot-96b_carbon.bin
    sudo dfu-util -d [0483:df11] -a 0 -s 0x08020000 -D linaro_fota-96b_carbon.signed.bin

Flash Carbon NRF51 with Firmware Binaries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The second chip on the Carbon that needs firmware is the NRF51, which
allows the STM32 you flashed earlier to communicate with the IOT
gateway via Bluetooth. The firmware binary for the NRF51 is:

``96b_carbon_nrf51.bin``

You can find it wherever you unpacked the release binaries if you
chose that method, or in the mcuboot directory if you followed the
instructions to build from source.

Refer to :ref:`device-support-stm32f4x` for flashing instructions.

Device Flash Layout
-------------------

This informational section describes the flash sector layout you have
set up on the Carbon STM32 using these instructions.

- **bootloader**

    - Flash: 0x08000000 - 0x08007FFF (this spans two sectors)
    - In this setup, the bootloader is the mcuboot zephyr.bin image

- **Unused area**

    - Flash: 0x08008000 - 0x0800BFFF
    - Currently unused

- **FOTA app state information**

    - Flash: 0x0800C000 - 0x0800FFFF
    - Data storage area

- **Unused area**

    - Flash: 0x08010000 - 0x0801FFFF
    - Currently unused

- **Application, Bank0**

    - Flash: 0x08020000 - 0x0803FFFF
    - Any application; the FOTA app is used here.

- **Application, Bank1**

    - Flash: 0x08040000 - 0x0805FFFF
    - Used for storing an updated FOTA app before copying it to
      bank 0.

- **Scratch**

    - Flash:  0x08060000 - 0x0807FFFF
    - Scratch is used when copy an application from Bank1 to Bank0
      during mcuboot OTA.
