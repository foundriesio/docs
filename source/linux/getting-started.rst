.. highlight:: sh

.. _linux-getting-started:

Getting Started
===============

All you need to get started is a gateway device supported by the Linux
microPlatform, a computer, and an Internet connection.

Get Hardware
------------

Here's what you'll need:

- A computer to develop on. This can be running Windows, Mac OS X, or
  Linux.

- A gateway device supported by the Linux microPlatform. We currently support
  the `96Boards HiKey <https://www.96boards.org/product/hikey/>`_, and
  assume you have a `96Boards UART Serial Adapter
  <https://www.96boards.org/product/debug/>`_ for console access.

Get Installation Dependencies
-----------------------------

To install the Linux microPlatform on your device, you'll need Python 2,
pySerial, drivers for FTDI serial port devices, and Android's fastboot tool.

Windows
~~~~~~~

- Install the latest `Python 2 release for Windows
  <https://www.python.org/downloads/windows/>`_.

- Install `pySerial`_ and the `FTDI drivers`_.

- Install fastboot with the latest `Android SDK Platform Tools for
  Windows`_.

Mac OS X
~~~~~~~~

- Python 2 is installed by default by Apple.

- Install `pySerial`_ and the `FTDI drivers`_.

- Install fastboot with the latest `Android SDK Platform Tools for
  Mac`_.

Linux
~~~~~

On Debian-based Linux distributions, including Ubuntu, run::

  sudo apt-get install python-serial fastboot

On other Linux distributions:

- Python 2 may be installed by default, and should be available in
  your package manager if not. You can also install `Python from
  source <https://www.python.org/downloads/source/>`_.

- `pySerial`_ is also likely available via your package manager or
  pip.

- Most distribution kernels provide FTDI USB serial port device
  support.

- Install fastboot using your package manager or the latest `Android
  SDK Platform Tools for Linux`_.

Get Prebuilt images
-------------------

.. osf-artifacts:: lmp-prebuilts

Set Your Board Up For Flashing
------------------------------

If you're using a 96Boards HiKey, do this by putting it into "Recovery
Mode" as follows:

1. Remove power from the HiKey.

#. Remove both jumpers from the 2x3 header at the top left of the
   board (J601 on LeMaker HiKeys).

   The board should now look like this:

   .. figure:: /_static/linux/hikey-no-jumpers.jpg
      :scale: 50%
      :align: center
      :alt: HiKey with no jumpers on J601

#. Use the jumpers to connect pins 1 and 2, as well as pins 3 and 4,
   on the 2x3 header.

   The board should now look like this:

   .. figure:: /_static/linux/hikey-recovery-jumpers.jpg
      :scale: 50%
      :align: center
      :alt: HiKey with jumpers on J601 set up for Recovery Mode

#. Connect the HiKey to your PC via USB.

#. Power on the HiKey.

See `HiKey board recovery documentation`_ for more information on
Recovery Mode.

If you're using a different 96Boards CE board, check its `96boards.org
documentation <https://www.96boards.org/products/ce/>`_ for
instructions on how to reflash the bootloader, install fastboot
support, and flash images via fastboot.

If you're not using a 96Boards board, refer to your vendor's
documentation for similar instructions, or contact your vendor
directly.

Flash Images To Your Board
--------------------------

These instructions assume you're using HiKey.

Windows
~~~~~~~

First, make sure that the directories containing the ``python.exe``
and ``fastboot.exe`` executables are on your ``PATH`` environment
variable.

Now run the following, replacing ``XXXX`` and ``YYYY`` appropriately
for the files you downloaded previously::

  python.exe hisi-idt.py --img1=l-loader.bin
  timeout 3 > NUL
  fastboot.exe flash fastboot fip.bin
  fastboot.exe flash nvme nvme.img
  fastboot.exe flash boot boot-XXXX.uefi.img
  fastboot.exe flash system rpb-ltd-gateway-image-hikey-YYYY.rootfs.img

Mac OS X and Linux
~~~~~~~~~~~~~~~~~~

.. note::

   On Linux, the ``hisi-idt.py`` script searches for a serial port
   device provided by your HiKey in ``/dev/serial/by-id``. Some HiKey
   boards have non-Roman characters in their serial devices' names,
   which confuse the script and cause it to fail.

   If this happens, passing the script ``-d /dev/ttyUSBx``, where
   ``/dev/ttyUSBx`` is the absolute path pointed to by the symlink in
   ``/dev/serial/by-id``, should resolve the issue.

Run the following, replacing ``XXXX`` and ``YYYY`` appropriately for
the files you downloaded previously::

  python2 hisi-idt.py --img1=l-loader.bin
  sleep 2
  fastboot flash fastboot fip.bin
  fastboot flash nvme nvme.img
  fastboot flash boot boot-XXXX.uefi.img
  fastboot flash system rpb-ltd-gateway-image-hikey-YYYY.rootfs.img

Boot the Board
--------------

Now that you've flashed the board, it's time to boot it. If you're
using a HiKey, follow these instructions.

1. Remove the jumper connecting pins 3 and 4 from the 2x3 header you
   used when putting the board in Recovery Mode.

#. Install the 96Boards UART Serial Adapter board on the board.

   .. warning:: Make sure the USB connector faces outward from the
                board, or you will damage or break both HiKey and the
                UART Serial Adapter.

#. Connect the UART Serial Adapter to your host PC via USB.

#. Apply power to the HiKey via the barrel jack connector.

Your board should look like this:

.. figure:: /_static/linux/hikey-boot.jpg
   :align: center
   :alt: HiKey when booting

.. highlight:: none

Wait for the following login prompt to appear at the serial console::

  hikey login:

Enter ``osf`` for the username, and ``osf`` for the password. You will
be dropped into a normal user shell, and **should now change the
password** using ``passwd``.

The ``osf`` user may use ``sudo`` to obtain root access on the device.

You can connect to a WiFi network like so::

  nmcli device wifi connect NETWORK_SSID password NETWORK_PASSWORD

USB Ethernet dongles will also work out of the box.

Onwards!
--------

That's it! You've successfully installed the Linux microPlatform,
booted into your device's console, and connected it to the network.

Your device is now ready for use. The Linux microPlatform makes it
easy for you to deploy applications to your device as either one
solitary or multiple coordinating Docker containers.

Possible next steps:

- See :ref:`iotfoundry-top` to use your device in IoT reference
  systems provided by Open Source Foundries.

- See :ref:`iot-gateway` to deploy IoT gateway applications on the
  Linux microPlatform, allowing other devices on local networks
  (including :ref:`zephyr-top` devices) to communicate with the cloud.

.. _pySerial:
   https://pythonhosted.org/pyserial/pyserial.html#installation

.. _FTDI drivers:
   http://www.ftdichip.com/FTDrivers.htm

.. _Android SDK Platform Tools for Windows:
   https://dl.google.com/android/repository/platform-tools-latest-windows.zip

.. _Android SDK Platform Tools for Mac:
   https://dl.google.com/android/repository/platform-tools-latest-darwin.zip

.. _Android SDK Platform Tools for Linux:
   https://dl.google.com/android/repository/platform-tools-latest-linux.zip

.. _HiKey board recovery documentation:
   https://github.com/96boards/documentation/blob/master/ConsumerEdition/HiKey/Installation/BoardRecovery.md#set-board-link-options
