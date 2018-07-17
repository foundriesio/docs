.. _tutorial-dependencies:

Procure Dependencies
====================

Hardware
--------

To complete the entire tutorial, you need a Linux or macOS workstation
computer, one or more Zephyr microPlatform devices, and a Linux
microPlatform device.

The Zephyr and Linux microPlatforms are portable, and builds for
several boards are available. To get started, however, we recommend:

**Zephyr microPlatform**: at least one of the following:

.. important:: Only one of these Zephyr devices is required to
               complete the tutorial.

- `RedBear BLE Nano 2`_ kit: make sure to purchase the kit, which
  includes the DAPLink board, and not just a standalone BLE Nano 2
  board. [#rb]_
- `nRF52 DK`_ (for nRF52832)
- `nRF52840 DK`_

**Linux microPlatform**:

- `Raspberry Pi 3 Model B`_ or `Raspberry Pi 3 Model B+`_
- SD card compatible with Raspberry Pi 3 (see this `Embedded
  Linux wiki guide`_ for examples)
- Ethernet cable (recommended)
- 3.3 volt USB to TTL Serial Cable, such as this `SparkFun FTDI Basic
  Breakout 3.3V`_ (optional, only needed if connecting via WiFi)

This hardware was chosen mainly because it is well-tested with the
microPlatforms, commonly available, and relatively inexpensive.
Performance seems adequate for connecting up to five or so Zephyr
microPlatform devices.

Subscriber Token
----------------

The latest Linux and Zephyr microPlatform updates are made
continuously available to subscribers. To access subscriber-only
content, you'll need to `create a subscriber access token on
app.foundries.io`_.

.. rubric:: Footnotes

.. [#rb]

   Since RedBear was acquired by Particle, supply of these boards has
   become limited; availability is expected to continue through Q1
   2019.

.. _RedBear BLE Nano 2:
   https://redbear.cc/product/ble-nano-kit-2.html

.. _nRF52 DK:
   https://www.nordicsemi.com/eng/Products/Bluetooth-low-energy/nRF52-DK

.. _nRF52840 DK:
   https://www.nordicsemi.com/eng/Products/nRF52840-DK

.. _Raspberry Pi 3 Model B:
   https://www.raspberrypi.org/products/raspberry-pi-3-model-b/

.. _Raspberry Pi 3 Model B+:
   https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/

.. _SparkFun FTDI Basic Breakout 3.3V:
   https://www.sparkfun.com/products/9873

.. _Embedded Linux wiki guide:
   https://elinux.org/RPi_SD_cards

.. _create a subscriber access token on app.foundries.io:
   https://app.foundries.io/settings/tokens
