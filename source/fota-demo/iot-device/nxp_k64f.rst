.. highlight:: sh

.. _iot-device-nxp_k64f:

IoT Device: NXP FRDM-K64F
=========================

From here, you can set up a FRDM-K64F device to receive FOTA updates.

.. contents::
   :local:

Choose Your Method
------------------

Using Released Binaries
~~~~~~~~~~~~~~~~~~~~~~~

.. warning:: The released binaries assume that the FRDM-K64F can join
             your Ethernet network at IP address 192.168.0.2, and that
             the :ref:`IoT gateway <iot-gateways>` will respond on IP
             address 192.168.0.1.

             If that won't work in your environment, you can follow
             instructions to build from source below with a different
             network configuration.

Download the binaries::

    wget https://builds.linarotechnologies.org/End-to-end_IoT_system/17.02-preview/mcuboot-frdm_k64f.bin
    wget https://builds.linarotechnologies.org/End-to-end_IoT_system/17.02-preview/linaro_fota-frdm_k64f.signed.bin

Once you have the binaries, install the flashing tool on your system,
and follow the instructions to flash binaries.

Building From Source
~~~~~~~~~~~~~~~~~~~~

If you're going to build from source instead, follow instructions on
:ref:`IoT Devices <iot-devices-build-source>` to clone the relevant
repositories and set up your build environment.

.. note::

   Since the FRDM-K64F board connects via Ethernet, and local network
   configurations differ, you need to provide some network
   configuration to the build so that the board connects to your
   network correctly when you flash it.

To provide network configuration to the build, create a file named
``boards/frdm_k64f-local.conf`` in the zephyr-fota-hawkbit directory
of your build environment. This file is ignored by Git. The file
should set values for ``CONFIG_NET_SAMPLES_MY_IPV4_ADDR``, the
FRDM-K64F's IP address, and ``CONFIG_NET_SAMPLES_PEER_IPV4_ADDR``, the
IoT gateway' IP address. Here is an example::

    CONFIG_NET_SAMPLES_MY_IPV4_ADDR="192.168.0.2"
    CONFIG_NET_SAMPLES_PEER_IPV4_ADDR="192.168.0.1"

.. note::

   The IP addresses "192.168.0.2" and "192.168.0.1" above are just
   example values. You can change them for your local network.

You can also write ``CONFIG_NET_DHCPV4=y`` instead of setting
``CONFIG_NET_SAMPLES_MY_IPV4_ADDR`` to dynamically request an IP
address from a DHCP server on your network router.

If you're not sure what your IoT Gateway's IP address is, you can run
``ip addr show`` on its console and check the output. Automatic
discovery of the IoT gateway by FRDM-K64F is not supported; you must
provide the gateway IP address using
``CONFIG_NET_SAMPLES_PEER_IPV4_ADDR``.

Now, build both a bootloader (mcuboot) and the Linaro FOTA Zephyr
application. ::

    # Establish Zephyr environment
    cd <zephyr-project>
    export ZEPHYR_SDK_INSTALL_DIR=/path/to/your/zephyr-sdk
    export ZEPHYR_GCC_VARIANT=zephyr
    . zephyr-env.sh

    # Linaro FOTA app
    cd <zephyr-fota-hawkbit>
    make BOARD=frdm_k64f

    # Build bootloader, and sign FOTA app built in previous step.
    cd <mcuboot>
    make BOARD=frdm_k64f
    cp outdir/frdm_k64f/zephyr.bin mcuboot-frdm_k64f.bin
    ./scripts/zep2newt.py --bin <zephyr-fota-hawkbit>/outdir/frdm_k64f/zephyr.bin \
                          --key root-rsa-2048.pem --sig RSA --vtoff 0x200 \
                          --out linaro_fota-frdm_k64f.signed.bin \
                          --word-size 8 --pad 0x20000 --bit

Flashing Tool
-------------

Next, install pyOCD to flash images onto the Nitrogen board.

https://github.com/mbedmicro/pyOCD

Flash K64F with Firmware Binaries
---------------------------------

Flash the bootloader and FOTA application binaries to the K64F using
pyOCD, after plugging the K64F into your system via USB. ::

    # Bootloader and signed FOTA app. Run these commands from:
    # - the directory your downloaded binaries are stored, if you used released binaries.
    # - the directory the binaries were built (linaro_fota and mcuboot)

    pyocd-flashtool -ce mcuboot-frdm_k64f.bin
    pyocd-flashtool -se --address 0x20000 linaro_fota-frdm_k64f.signed.bin

Device Flash Layout
-------------------

This informational section describes the flash sector layout you have
set up using these instructions.

- **bootloader**

    - Flash: 0x00000000 - 0x00010000
    - In this setup, the bootloader is the mcuboot zephyr.bin image

- **FOTA app state information**

    - Flash: 0x00010000 - 0x00017FFF

- **Currently Unused**

    - Flash: 0x00018000 - 0x0001FFFF

- **Application, Bank0**

    - Flash: 0x00020000 - 0x0003FFFF
    - Any application, the FOTA app is used here.

- **Application, Bank1**

    - Flash: 0x00040000 - 0x0005FFFF
    - Used for storing an updated FOTA app before copying it to bank 0.

- **Scratch**

    - Flash:  0x00060000 - 0x0007FFFF
    - Scratch is used when copy an application from Bank1 to Bank0
      during mcuboot OTA.

- **Currently Unused**

    - Flash: 0x00080000 - 0x000FFFFF
    - **The flash layout for K64F leaves 512k unused flash – this is
      for testing compatibility with smaller HW devices such as
      Carbon.**
