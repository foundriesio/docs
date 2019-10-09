.. highlight:: sh

.. _tutorial-linux:

Install Linux microPlatform
===========================

The Linux microPlatform is split into two parts:

1. A *base system*, which is built using OpenEmbedded / Yocto. It
   provides a minimal runtime for application development which is
   over the air updatable.

2. Applications, which are developed and deployed as *containers*
   running on the base system. Application updates are accomplished by
   running updated containers. Currently, Docker containers are
   supported.

.. figure:: /_static/tutorial/linux-microplatform.png
   :alt: Linux microPlatform block diagram
   :align: center
   :width: 5in

   Linux microPlatform

This document describes how to:

- Install the base system onto your device, connect it to the network,
  and connect to its console.

- Run a web server in a container on the device, demonstrating
  application deployment.

.. important::

   Make sure you've obtained dependencies as described in
   :ref:`tutorial-dependencies` before continuing.

.. _tutorial-linux-base:

Install Base microPlatform
--------------------------

You'll start by installing the base microPlatform and connecting to
your device's console.

This document provides instructions for the Raspberry Pi 3 models B
and B+ reference development boards. If you are using a different
board, or want to build from source then see
:ref:`ref-linux-targets` and :ref:`ref-linux-building` in the
reference manual.

**Get Prebuilt Image**

Update |version| can be downloaded here:

.. lmp-rpi3-links::

**Flash Image To SD Card**

The Raspberry Pi foundation recommends using the the cross-platform
`Etcher`_ tool to flash images onto the SD card you'll use to boot
your `Raspberry Pi 3`_.

After you've installed Etcher on your system:

#. Attach an SD card onto your host computer. Refer to this `Embedded
   Linux wiki guide`_ for a list of SD cards compatible with Raspberry
   Pi 3.
#. Run Etcher, and select the pre-built Linux microPlatform image you
   downloaded on your file system.
#. Select the SD card you mounted from Etcher, and flash it.

More detailed guides are available for `macOS`_,
`Windows`_, and `Linux`_.

**Boot Raspberry Pi 3 and Connect to the Network**

Choose a method:

.. content-tabs::

   .. tab-container:: ethernet
      :title: Ethernet (Recommended)

      Ethernet works out of the box if a DHCP server is available on the
      local network.

      #. Connect an Ethernet cable to the Raspberry Pi 3.
      #. Remove the SD card from your computer, and insert it into
         the Raspberry Pi 3.
      #. Apply power to the Raspberry Pi 3.

      Your board will connect to the network via Ethernet. The board should
      be ready to connect within a minute or two of booting.

   .. tab-container:: wifi
      :title: WiFi

      If you don't have Ethernet connectivity, you can connect to a
      WiFi network by temporarily enabling the UART console on your
      Raspberry Pi 3 and running a command to connect to your WiFi
      network.

      .. note::

         While a hardware serial port is available, enabling it
         unfortunately requires this device to run at significantly
         reduced speeds, and causes serious Bluetooth instability.
         Make sure to disable the console and reboot before
         proceeding.

      You'll need a 3.3 volt USB to TTL serial adapter, such as this
      `SparkFun FTDI Basic Breakout 3.3V`_.

      #. Mount the micro SD card containing the SD image you
         flashed on your workstation PC.

      #. Edit the ``config.txt`` file on the VFAT partition,
         adding a new line with the following content::

            enable_uart=1

      #. Safely unmount the micro SD card, remove it from your
         workstation, and insert it into the Raspberry Pi 3.

      #. Connect the adapter to your Raspberry Pi 3's UART and
         to your workstation computer via USB, e.g. by following
         `this AdaFruit guide`_.

      #. Connect a serial console program on your workstation to
         the adapter, and power on the Raspberry Pi 3.

      #. When prompted, log in via the console. The default
         username is ``fio``, and the default password is
         ``fio``. You should change the password before
         connecting to the network.

      #. Connect to the network using the following command::

            sudo nmcli device wifi connect NETWORK_SSID password NETWORK_PASSWORD

         Where ``NETWORK_SSID`` is your WiFi network's SSID, and
         ``NETWORK_PASSWORD`` is the password.

      #. Safely shut down the Raspberry Pi 3, re-mount the SD
         card on your host workstation, and delete the line you
         added to ``config.txt``.

      #. Unmount the SD card from your workstation, insert it
         into the Raspberry Pi 3, and reboot it.

      .. warning::

         Do not skip the final steps. Functionality with the
         serial console enabled is severely degraded.

      Your board will connect to the network you've saved after
      rebooting. You can now log in using SSH.

**Log in via SSH**

Use ``fio`` as the username and ``raspberrypi3-64.local`` as the
hostname::

  ssh fio@raspberrypi3-64.local

The default password is ``fio``; we recommend changing it now if you
haven't already. For this to work, your local network needs to support
Zeroconf\ [#zeroconf]_ and the hostname must be otherwise unclaimed.

If that doesn't work, you can also log in by IP address. See
:ref:`Troubleshooting <tutorial-linux-troubleshooting>` below for
advice.

**Finish Installation**

Once you have an SSH console connection, finish your installation by
setting up aktualizr-lite. Follow instructions in
:ref:`tutorial-aklite` for a demonstration.

.. _tutorial-linux-troubleshooting:

**Troubleshooting**

If the above methods to connect your Raspberry Pi 3 to the
network don't work, try one of the following.

- Temporarily enable and connect to the UART (see directions above in
  the WiFi section) and determine available IP addresses with::

    # Ethernet
    ip addr show eth0 scope global

    # WiFi
    ip addr show wlan0 scope global

  Then connect by IP address::

    ssh fio@rpi3.ip.addr.ess

- List connected devices and their local IP addresses on your network
  router's administrative interface, and log in by IP address as
  above.

Test Your Connection
~~~~~~~~~~~~~~~~~~~~

Test your Linux microPlatform device's network connection any way you
would like. For example::

    ping -c 3 foundries.io

.. _tutorial-aklite:

Using Aktualizr-lite
--------------------

Aktualizr-lite is the update agent included with the Linux microPlatform. It
runs as a system daemon periodically looking for new updates to apply to
your device. There are a few interesting things you can do with aktualizr-lite:

Configuring Docker Apps
~~~~~~~~~~~~~~~~~~~~~~~
TODO - and link to docker-app reference

Controlling incoming updates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TODO - describe how to controll reboot and flocking options - probably link to reference doc

.. include:: reporting-issues.include

.. rubric:: Footnotes

.. [#zeroconf]

   Zeroconf is a set of technologies that allows automatic discovery
   of systems and services available on a local area network. It helps
   by assigning a local address name (e.g. ``hostname.local``
   instead of ``192.168.1.10``), which can be used by other Zeroconf
   compatible services like Bonjour on macOS.

   Avahi, a free Zeroconf implementation, is available by default on
   the Linux microPlatform, making it easy for other
   Zeroconf-compatible hosts to locate the IP address assigned to the
   board.

   To use Zeroconf, simply use ``hostname.local`` in place of the
   board's IP address when that is needed.

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
