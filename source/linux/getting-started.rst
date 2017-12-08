.. highlight:: sh

.. _linux-getting-started:

Getting Started: Install Linux microPlatform
============================================

This page describes how to install the base Linux microPlatform onto a
device. All you need to get started is a gateway device supported by
the Linux microPlatform, a computer, and an Internet connection.

For a complementary guide on getting set up to develop and deploy
containerized applications onto your device, see :ref:`iot-gateway`.

Get Hardware
------------

Here's what you'll need:

- A computer to develop on. This can be running Windows, Mac OS X, or
  Linux.

- A gateway device supported by the Linux microPlatform. We currently
  recommend getting started with the `Raspberry Pi 3`_.

Get Prebuilt images
-------------------

Prebuilt images for Linux microPlatform release v0.1 are available for
Raspberry Pi 3 either uncompressed, or as an .xz compressed archive:

- `.sdcard format`_
- `.sdcard.xz format`_

The downloaded images currently have odd names. You will need to
rename the image to something like :file:`rpi3.sdcard` or
:file:`rpi3.sdcard.xz`. This issue will be resolved in a subsequent
release.

Flash Images To Your Board
--------------------------

To flash images to your board, the Raspberry Pi 3 foundation
recommends installing images using the the cross-platform `Etcher`_
tool.

After you've installed Etcher on your system:

#. Attach an SD card onto your host computer. Refer to this `Embedded
   Linux wiki guide`_ for a list of SD cards compatible with Raspberry
   Pi 3.
#. Run Etcher, and select the pre-built Linux microPlatform image you
   downloaded on your file system.
#. Select the SD card you mounted from Etcher, and flash it.
#. Safely unmount the SD card from your computer, and insert it into
   the Raspberry Pi 3.

Additional, more advanced guides are available for `macOS`_,
`Windows`_, and `Linux`_.

Boot the Board
--------------

Apply power to the Raspberry Pi 3.

Note that the serial console is disabled by default on the Raspberry
Pi 3 because it requires the device to run at significantly slower
speeds. To wire up the USB to TTL adapter follow `this AdaFruit
guide`_. You'll need a 3.3 volt USB to TTL Serial Cable, such as this
`SparkFun FTDI Basic Breakout 3.3V`_.

To enable the serial console:

#. Insert the micro SD card into a PC.
#. Edit the ``config.txt`` file on the VFAT partition, adding a new
   line with the following content:

   .. code-block:: none

      enable_uart=1
#. Safely unmount the micro SD card.
#. Insert micro SD into Raspberry Pi 3, connect serial console and
   power on the board.

After you've connected to the serial console, you can log in. The
default username is ``osf``, and the default password is ``osf``. You
should change these before connecting to the network.

Connect to the Network
----------------------

Both native Ethernet and USB Ethernet dongles should work out of the box
if a DHCP Server is available on the same local network.

If using WiFi, you can connect with:

.. code-block:: console

   sudo nmcli device wifi connect NETWORK_SSID password NETWORK_PASSWORD

Where ``NETWORK_SSID`` is your WiFi network's SSID, and
``NETWORK_PASSWORD`` is the password.

Locating the Board via Zeroconf
-------------------------------

Zeroconf is a set of technologies that allows automatic discovery of systems
and services available on a local area network. It helps by assigning a local
address name (e.g. raspberrypi3.local instead of 192.168.1.10), which can be
used by other zeroconf compatible services (e.g. Bonjour on macOS).

Avahi (a free zeroconf implementation) is available by default on the Linux
microPlatform, making it easy for other zeroconf-compatible hosts to locate
the IP address assigned to the board, which can be specially useful when a
console is not available.

To locate your board, simply use ``raspberrypi3.local`` instead of the board's
IP address.

Next Steps
----------

You've now successfully installed the Linux microPlatform, booted into
your device's console, and connected it to the network.

Your device is now ready for use. The Linux microPlatform makes it
easy for you to deploy applications to your device as either one
solitary or multiple coordinating Docker containers.

We recommend these next steps:

#. First, move on to :ref:`iot-gateway` to get set up to deploy IoT
   gateway applications on the Linux microPlatform, allowing other
   devices on local networks (including :ref:`zephyr-top` devices) to
   communicate with the cloud.

#. Then use your device in IoT reference systems provided by Open
   Source Foundries in :ref:`iotfoundry-top`.

#. Once you've got a demonstration system working, start customizing
   for your needs.

.. _Raspberry Pi 3:
   https://www.raspberrypi.org/products/raspberry-pi-3-model-b/

.. _Etcher:
    https://etcher.io/

.. _Embedded Linux wiki guide:
   https://elinux.org/RPi_SD_cards

.. _macOS:
    https://www.raspberrypi.org/documentation/installation/installing-images/mac.md

.. _Windows:
   https://www.raspberrypi.org/documentation/installation/installing-images/windows.md

.. _Linux:
   https://www.raspberrypi.org/documentation/installation/installing-images/linux.md

.. _this AdaFruit guide:
   https://learn.adafruit.com/adafruits-raspberry-pi-lesson-5-using-a-console-cable/connect-the-lead

.. _SparkFun FTDI Basic Breakout 3.3V:
   https://www.sparkfun.com/products/9873

.. _.sdcard format:
    https://foundries.io/r/lmp/0.3/artifacts/build-raspberrypi3/lmp-gateway-image.rootfs.sdimg

.. _.sdcard.xz format:
   https://foundries.io/r/lmp/0.3/artifacts/build-raspberrypi3/lmp-gateway-image.rootfs.sdimg.xz
