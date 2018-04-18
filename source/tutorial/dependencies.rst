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

**Zephyr microPlatform**:

- `RedBear BLE Nano 2`_ kit: make sure to purchase the kit, which
  includes the DAPLink board, and not just a standalone BLE Nano 2
  board.

**Linux microPlatform**:

- `Raspberry Pi 3 Model B`_
- 3.3 volt USB to TTL Serial Cable, such as this `SparkFun FTDI Basic
  Breakout 3.3V`_
- SD card compatible with Raspberry Pi 3 (see this `Embedded
  Linux wiki guide`_ for examples)
- Ethernet cable (optional)

This hardware was chosen mainly because it is well-tested with the
microPlatforms, as well as commonly and relatively inexpensively
available.

Subscriber Token (Optional)
---------------------------

The latest Linux and Zephyr microPlatform updates are made
continuously available to subscribers. To access subscriber-only
content, you'll need to generate a token at https://foundries.io/s/\ .

Non-subscribers can use latest public release. Public releases match
the subscriber trees, but lag behind them; they are typically released
once or twice a year.

.. _RedBear BLE Nano 2:
   https://redbear.cc/product/ble-nano-kit-2.html

.. _Raspberry Pi 3 Model B:
   https://www.raspberrypi.org/products/raspberry-pi-3-model-b/

.. _SparkFun FTDI Basic Breakout 3.3V:
   https://www.sparkfun.com/products/9873

.. _Embedded Linux wiki guide:
   https://elinux.org/RPi_SD_cards
