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
  the `96Boards HiKey <http://www.96boards.org/product/hikey/>`_, and
  assume you have a `96Boards UART Serial Adapter
  <http://www.96boards.org/product/debug/>`_ for console access.

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

- Optionally, install the latest `Ansible release for OS X`_. This
  will make it easier to deploy containers on your device.

Linux
~~~~~

On Debian-based Linux distributions, including Ubuntu, run::

  sudo apt-get install python-serial fastboot

Optionally, install Ansible, to make it easier to deploy containers on
your device::

  sudo apt-get install ansible

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

- You may optionally install Ansible using instructions on its
  `Installation page
  <http://docs.ansible.com/ansible/intro_installation.html>`_.

Get prebuilt images
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
documentation <http://www.96boards.org/products/ce/>`_ for
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

#. Install the 96Boards UART Serial Adapter board on the board. Make
   sure the USB connector faces outward from the board, or you will
   damage or break both HiKey and the UART Serial Adapter.

#. Connect the UART Serial Adapter to your host PC via USB.

#. Apply power to the HiKey via the barrel jack connector.

Your board should look like this:

.. figure:: /_static/linux/hikey-boot.jpg
   :align: center
   :alt: HiKey when booting

.. highlight:: none

At the serial console, the following login prompt should appear after
the board finishes booting::

  Reference-Platform-Build-X11 2.0+linaro hikey ttyAMA3

  hikey login:

Enter ``osf`` for the username, and ``osf`` for the
password. You will be dropped into a normal user shell, and should now
change the password. The ``osf`` user may use ``sudo`` to obtain
root access on the device.

That's it! You've successfully installed the Linux microPlatform onto your
device, and booted into its console.

Onwards!
--------

At this point your device is ready to run Docker containers.  If you would
like to configure the device as a Basic IoT Gateway, follow the instructions
at :ref:`basic-gateway`.

You're now ready to take your next steps. This will take the form of
deploying containerized applications to your device.

One of the greatest advantages of using Cerberus is that it makes it
easier to deploy and manage container-based applications. What's more,
unlike other container-based embedded device platforms, Cerberus
allows you to deploy **multiple applications to the same gateway, each
running at the same time in its own container**. This is called
**multitenancy**.

Check out the Linaro Technologies Division `Gateway Containers
<https://github.com/linaro-technologies/gateway-containers>`_
repository for example Docker containers, along with instructions for
how to get them running on your board. Start with the top-level
`gateway-containers README.md`_, and move on to the subdirectories for
containers which interest you.

If you installed Ansible earlier, you can also use Ansible playbooks
to deploy the containers; these are available in the `gateway-ansible
<https://github.com/OpenSourceFoundries/gateway-ansible>`_
repository. (While Ansible isn't supported on Windows, you can run
`Ubuntu in a Docker container <https://hub.docker.com/_/ubuntu/>`_ and
run Ansible from Ubuntu.)

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

.. _Ansible release for OS X:
   http://docs.ansible.com/ansible/intro_installation.html#latest-releases-on-mac-osx

.. _gateway-containers README.md:
   https://github.com/linaro-technologies/gateway-containers/blob/master/README.md

.. _HiKey board recovery documentation:
   https://github.com/96boards/documentation/blob/master/ConsumerEdition/HiKey/Installation/BoardRecovery.md#set-board-link-options
