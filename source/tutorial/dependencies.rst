.. _tutorial-dependencies:

Procure Dependencies
====================

Hardware
--------

To set up this system, you will need a Linux or macOS workstation
computer, one or more IoT devices, and an IoT gateway.

The Zephyr and Linux microPlatforms were designed for portability, and
the LWM2M system has been ported to several boards.  To get started,
however, we recommend the following.

**Zephyr microPlatform** dependencies:

- `BLE Nano 2`_ as an IoT device. Make sure to purchase the entire
  kit, including the DAPLink board, not just the standalone BLE Nano 2
  board.

**Linux microPlatform** dependencies:

- `Raspberry Pi 3`_ as an IoT gateway
- 3.3 volt USB to TTL Serial Cable, such as this `SparkFun FTDI Basic
  Breakout 3.3V`_
- SD card compatible with Raspberry Pi 3 (see this `Embedded
  Linux wiki guide`_ for examples)
- (Optional, but recommended) Ethernet cable for Raspberry Pi 3

This hardware was chosen for this tutorial mainly because it is
commonly, and relatively inexpensively, available.

Subscriber Token
----------------

The latest Linux and Zephyr microPlatform updates are made
continuously avaiable to subscribers. To access subscriber-only
content, you'll need to generate a token at https://foundries.io/s/\ .

Non-subscribers can use the public microPlatform update streams. Note
note that these lag behind the subscriber updates by up to six months.

.. _BLE Nano 2:
   https://redbear.cc/product/ble-nano-kit-2.html

.. _Raspberry Pi 3:
   https://www.raspberrypi.org/products/raspberry-pi-3-model-b/

.. _SparkFun FTDI Basic Breakout 3.3V:
   https://www.sparkfun.com/products/9873

.. _Embedded Linux wiki guide:
   https://elinux.org/RPi_SD_cards
