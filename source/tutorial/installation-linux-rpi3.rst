:orphan:

.. Note: this page is an orphan to make the "next"/"prev" links at the
   bottom of each page in the tutorial reflect the order they should
   be read in.

.. highlight:: sh

.. _tutorial-linux-rpi3:

Install Base Linux microPlatform: Raspberry Pi 3
================================================

These are the board-specific instructions for :ref:`installing the
base Linux microPlatform <tutorial-linux-base>` on the Raspberry Pi 3
Model B.

Get Prebuilt Image
------------------

A prebuilt image for Linux microPlatform update |version| is available:

.. osf-rpi3-links::

Flash Image To SD Card
----------------------

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

Additional, more advanced guides are available for `macOS`_,
`Windows`_, and `Linux`_.

Boot Raspberry Pi 3 and Connect to the Console
----------------------------------------------

A serial console is not available. You will need to set up an SSH
connection to your device to get a console. (For size and security
reasons, the base Linux microPlatform doesn't have windowing support
enabled, so a graphical shell is not available.)

.. note::

   While a hardware serial port is available, enabling it
   unfortunately requires this device to run at significantly reduced
   speeds, and causes serious Bluetooth instability.

Option 1: Ethernet (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ethernet works out of the box if a DHCP server is available on the
local network.

#. Connect an Ethernet cable to the Raspberry Pi 3.
#. Remove the SD card from your computer, and insert it into
   the Raspberry Pi 3.
#. Apply power to the Raspberry Pi 3.

Your board will connect to the network via Ethernet. The board should
be ready to connect within a minute or two of booting. Move on to
:ref:`tutorial-linux-rpi3-ssh`.

Option 2: WiFi
~~~~~~~~~~~~~~

If Zeroconf doesn't work, or you don't have Ethernet connectivity, you
can connect to a WiFi network by temporarily enabling the UART console
on your Raspberry Pi 3 and running a command to connect to your WiFi
network.

You'll need a 3.3 volt USB to TTL serial adapter, such as this
`SparkFun FTDI Basic Breakout 3.3V`_.

#. Mount the micro SD card containing the SD image you flashed on your
   workstation PC.

#. Edit the ``config.txt`` file on the VFAT partition, adding a new
   line with the following content::

      enable_uart=1

#. Safely unmount the micro SD card, remove it from your workstation,
   and insert it into the Raspberry Pi 3.

#. Connect the adapter to your Raspberry Pi 3's UART and to your
   workstation computer via USB, e.g. by following `this AdaFruit
   guide`_.

#. Connect a serial console program on your workstation to the
   adapter, and power on the Raspberry Pi 3.

#. When prompted, log in via the console. The default username is
   ``osf``, and the default password is ``osf``. You should change
   the password before connecting to the network.

#. Connect to the network using the following command::

      sudo nmcli device wifi connect NETWORK_SSID password NETWORK_PASSWORD

   Where ``NETWORK_SSID`` is your WiFi network's SSID, and
   ``NETWORK_PASSWORD`` is the password.

#. Safely shut down the Raspberry Pi 3, re-mount the SD card on your
   host workstation, and delete the line you added to ``config.txt``.

#. Unmount the SD card from your workstation, insert it into the
   Raspberry Pi 3, and reboot it.

.. warning::

   Do not skip the final steps. Functionality with the serial console
   enabled is severely degraded.

Your board will connect to the network you've saved after booting. You
can now log in using SSH.

.. _tutorial-linux-rpi3-ssh:

Connect via SSH
~~~~~~~~~~~~~~~

Log in via SSH using ``osf`` as the username and
``raspberrypi3-64.local`` as the hostname::

  ssh osf@raspberrypi3-64.local

The default password is ``osf``; we recommend changing it now if you
haven't already. For this to work, your local network needs to support
Zeroconf and the hostname must be otherwise unclaimed.

Finish Installation
-------------------

Once you have an SSH console connection, finish your installation by
setting up application containers. Follow instructions in
:ref:`tutorial-linux-nginx` for a demonstration.

Appendix: Troubleshooting
-------------------------

If the above methods to connect to the network don't work, try one of
the following.

- Temporarily enable and connect to the UART (see directions above in
  the WiFi section) and determine available IP addresses with::

    # Ethernet
    ip addr show eth0 scope global

    # WiFi
    ip addr show wlan0 scope global

  Then connect by IP address::

    ssh osf@rpi3.ip.addr.ess

- List connected devices and their local IP addresses on your network
  router's administrative interface, and log in by IP address as
  above.

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
