.. _rtos-appendix-devices:

Additional IoT Devices
----------------------

96Boards Carbon
~~~~~~~~~~~~~~~

.. _Black Magic Debug Probe:
   https://github.com/blacksphere/blackmagic/wiki

.. _Segger JLink:
   https://www.segger.com/jlink_base.html

.. _96b_carbon_nrf51 flashing instructions:
   https://www.zephyrproject.org/doc/boards/arm/96b_carbon_nrf51/doc/96b_carbon_nrf51.html

There are two chips on the Carbon that need firmware, an STM32 and an
nRF51. The STM32 runs the bootloader and main FOTA application. The
nRF51 is a support chip which allows the application on the STM32 to
communicate with the IoT gateway via Bluetooth.

From the RTOS MicroPlatform installation directory, build the main application
for the STM32::

  ./genesis build -b 96b_carbon zephyr-fota-samples/dm-hawkbit-mqtt

.. todo:: add lwm2m build example

Then build another binary needed for the nRF51::

  ./genesis build -b 96b_carbon_nrf51 -c prj_96b_carbon_nrf51.conf \
                  --skip-signature zephyr/samples/bluetooth/hci_spi/

You'll need flashing tools to flash each of these chips.

- **dfu-util**
    - URL: http://dfu-util.sourceforge.net/
    - Git Repository: git://git.code.sf.net/p/dfu-util/dfu-util
    - This is used when flashing 96boards Carbon
- Flashing the Carbon nRF51 device requires an external SWD flashing
  tool, such as the `Black Magic Debug Probe`_ or `Segger JLink`_.

To flash the STM32, first put your Carbon into DFU mode by unplugging
it, then plugging it back in while the BOOT0 button is pressed.

Then, from the RTOS MicroPlatform installation directory, run::

  ./genesis flash -b 96b_carbon zephyr-fota-samples/dm-hawkbit-mqtt

.. todo:: add lwm2m flash example

Next, flash the nRF51, which allows the STM32 you flashed earlier to
communicate with the IOT gateway via Bluetooth. Relative to the
RTOS MicroPlatform installation directory, the firmware binary for the
nRF51 is:

``outdir/zephyr/samples/bluetooth/hci_spi/96b_carbon_nrf51/app/zephyr.elf``

Before flashing this file, first **put your Carbon in DFU mode again**
to ensure the STM32 firmware does not interfere with the nRF51. Then
follow the Zephyr `96b_carbon_nrf51 flashing instructions`_ to flash
the binary.

FRDM-K64F
~~~~~~~~~

.. _FRDM-K64F:
   http://www.nxp.com/products/developer-resources/hardware-development-tools/freedom-development-boards/freedom-development-platform-for-kinetis-k64-k63-and-k24-mcus:FRDM-K64F

Building for FRDM-K64F requires some configuration information which
depends on your local network:

- An IP address to use for the IoT gateway
- Whether to use DHCP, or a static IP address to use for the board
  itself

This information must be written to the file
``zephyr-fota-samples/dm-hawkbit-mqtt/boards/frdm_k64f-local.conf`` in
the RTOS MicroPlatform installation directory.

.. todo:: add k64f configfile for lwm2m example

.. highlight:: none

To use DHCP, with gateway IP address A.B.C.D, create the file with the
following contents::

  CONFIG_NET_DHCPV4=y
  CONFIG_NET_APP_PEER_IPV4_ADDR="A.B.C.D"

To use a static IP address X.Y.Z.W for the FRDM-K64F instead::

  CONFIG_NET_APP_MY_IPV4_ADDR="X.Y.Z.W"
  CONFIG_NET_APP_PEER_IPV4_ADDR="A.B.C.D"

.. highlight:: sh

Now you can build the binaries. From the RTOS MicroPlatform installation
directory::

    ./genesis build -b frdm_k64f zephyr-fota-samples/dm-hawkbit-mqtt

.. todo:: add lwm2m build example

.. include:: pyocd.include

To flash the binaries, plug the K64F into your system via the USB
connector labeled "SDA USB". Then, from the RTOS MicroPlatform installation
directory::

    ./genesis flash -b frdm_k64f zephyr-fota-samples/dm-hawkbit-mqtt

.. todo:: add lwm2m flash example
