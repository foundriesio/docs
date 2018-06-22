.. highlight:: sh

.. _tutorial-zephyr:

Install Zephyr microPlatform
============================

The Zephyr microPlatform is an extensible software platform that makes
it easier to develop, secure, and maintain Internet-connected
applications on microcontroller devices.

The Zephyr microPlatform is based on the `Zephyr`_ real-time operating
system, and the `MCUBoot`_ secure bootloader.

.. figure:: /_static/tutorial/zephyr-microplatform.png
   :alt: Zephyr microPlatform block diagram
   :align: center
   :width: 5in

   Zephyr microPlatform

This document describes how to:

- Set up a Zephyr microPlatform development environment on your workstation

- Flash MCUBoot and a Zephyr application image onto a microcontroller
  device

- Boot the device, verifying that MCUBoot correctly validates and
  chain-loads the Zephyr image

.. important::

   Make sure you've obtained dependencies as described in
   :ref:`tutorial-dependencies` before continuing.

Set up Build Environment
------------------------

Before installing the the Zephyr microPlatform, you need to set up
your workstation build environment. Instructions for each supported
platform follow.

macOS
~~~~~

We test on macOS Sierra (10.12).

#. Install `HomeBrew`_.

#. Install dependencies for the Zephyr microPlatform::

     brew install dtc python3 repo gpg cmake
     pip3 install --user ply pyyaml cryptography pyelftools intelhex ninja pyserial click

   .. note::

      If you are running pip version 10, you may see this error::

        ModuleNotFoundError: No module named 'pip.req'

      If that happens, install ninja with brew instead of pip::

        brew install ninja

      This is being tracked upstream as `ninja bug #1431
      <https://github.com/ninja-build/ninja/issues/1431>`_.

#. Install the tools you need to flash your board.

   For `BLE Nano 2`_, you'll need `pyOCD`_, which you can install with
   the pip2 provided by HomeBrew's Python 2 (`not pip3
   <https://github.com/mbedmicro/pyOCD/issues/208>`_!)::

     brew install python
     pip2 install --user pyOCD
     export PATH=$PATH:$HOME/Library/Python/2.7/bin


   For the nRF DK boards, you'll need the `nRF5x Command Line Tools`_.

   For other boards, check your board's documentation.  At this time,
   the Zephyr microPlatform only supports boards that can be flashed
   with pyOCD, nrfjprog, or dfu-util's DfuSe (i.e. STM32 extensions to
   the USB DFU protocol).

#. Configure your username and password in Git::

     git config --global user.name "Your Full Name"
     git config --global user.email "your-email-address@example.com"

Your build environment is now ready; continue by following the steps
in :ref:`tutorial-zephyr-install`.

Windows 10 (Experimental)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   Due to the Zephyr microPlatform's current use of the Repo tool to
   manage multiple Git repositories, only experimental directions
   using the Windows Subsystem for Linux are provided. This is because
   Repo does not work on Windows.

   When possible, the Zephyr microPlatform will use `Zephyr's West
   tool`_ to manage repositories instead, enabling first-class Windows
   support.

Windows versions supporting the Windows Subsystem for Linux have
experimental support. For this to work, you will need 64 bit Windows
10 Anniversary Update or later.

These instructions should let you build binaries; however, flashing
support is not yet documented.

#. Install the `Windows Subsystem for Linux`_, then open a Bash
   window to enter commands.

#. Change to your Windows user directory with a command like this::

     cd /mnt/c/Users/YOUR-USER-NAME

   You can press the Tab key after typing ``/Users/`` to see a list of
   user names.

   .. warning::

      Skipping this step means you won't be able to use the
      microPlatform with Windows tools like Explorer, graphical
      editors, etc.

      As documented by Microsoft, `changing files in Linux directories
      using Windows tools`_ can damage your system.

#. We recommend making sure your Linux subsystem is up to date with
   these commands (which can take a while they first time they're run)::

     apt-get update
     apt-get upgrade

#. Finish by following the Ubuntu instructions in the next section.

Linux
~~~~~

1. Install dependencies for the Zephyr microPlatform.

   On Ubuntu (16.04 and up)::

     sudo add-apt-repository ppa:osf-maintainers/ppa
     sudo apt-get update
     sudo apt-get install zmp-dev
     pip3 install --user pyelftools intelhex pyserial click \
                         cryptography --only-binary cryptography

   On other distributions, see :ref:`tutorial-zephyr-dependencies`.

#. Install the tools you need to flash your board.

   For `BLE Nano 2`_, you'll need `pyOCD`_, which you can install with
   `pip`_ (`not pip3
   <https://github.com/mbedmicro/pyOCD/issues/208>`_!)::

     sudo apt-get install python-pip
     # Make sure this is a Python 2 pip!
     pip install --user pyOCD

   For the nRF DK boards, you'll need the `nRF5x Command Line Tools`_.

   For other boards, check your board's documentation.  At this time,
   the Zephyr microPlatform only supports boards that can be flashed
   with pyOCD, nrfjprog, or dfu-util's DfuSe (i.e. STM32 extensions to
   the USB DFU protocol).

#. Install the following udev rules as root, then unplug and plug back
   in any boards you have connected::

     echo 'ATTR{idProduct}=="0204", ATTR{idVendor}=="0d28", MODE="0666", GROUP="plugdev"' > /etc/udev/rules.d/50-cmsis-dap.rules

#. Configure your username and password in Git::

     git config --global user.name "Your Full Name"
     git config --global user.email "your-email-address@example.com"

Your system is now ready to install the Zephyr microPlatform.

.. _tutorial-zephyr-install:

Install the Zephyr microPlatform
--------------------------------

The Zephyr microPlatform can be installed in any directory on your
workstation.

The Zephyr microPlatform currently uses the Repo tool to fetch a
variety of Git repositories at known-good revisions, and keep them in
sync as time goes on. If you're new to Repo and want to know more, see
:ref:`ref-zephyr-repo`.

Subscribers
~~~~~~~~~~~

The latest continuous release is available to Zephyr microPlatform
subscribers from `source.foundries.io`_. Install it as follows.

#. Configure Git to cache usernames and passwords you enter in memory for
   one hour::

     git config --global credential.helper 'cache --timeout=3600'

   Using some credential helper is necessary for ``repo sync`` to work
   properly later\ [#git-creds]_.

#. If you haven't already, `create a subscriber access token on
   foundries.io/s/`_.

#. Make an installation directory for the Zephyr microPlatform, and
   change into it::

     mkdir zmp && cd zmp

#. Install the latest release using ``repo``::

     repo init -u https://source.foundries.io/zmp-manifest
     repo sync

   When prompted by ``repo init``, enter your subscriber access token
   for your username and nothing for the password.

Public
~~~~~~

The latest public release is available from the `Open Source Foundries
GitHub`_ organization.

#. Make an installation directory for the Zephyr microPlatform, and
   change into its directory::

     mkdir zmp && cd zmp

#. Install the latest release using ``repo``::

     repo init -u https://github.com/OpenSourceFoundries/zmp-manifest
     repo sync

.. _tutorial-zephyr-build:

Build an Application
--------------------

Now that you've installed the Zephyr microPlatform, it's time to build
a demonstration application using the :ref:`zmp tool <ref-zephyr-zmp>`
provided in the Zephyr microPlatform installation directory [#zmpwest]_.

You'll start with a "hello world" app. However, ``zmp`` will also sign
the application image for chainloading by MCUboot, a secure bootloader
for microcontrollers, as well as build an MCUboot image for your
board.

.. important::

   The build uses a publicly available RSA key pair bundled with
   MCUBoot itself by default, for ease of demonstration (the private
   key is in :file:`mcuboot/root-rsa-2048.pem`; the public key is
   embedded in the sources in :file:`mcuboot/boot/zephyr/keys.c`).

   This key pair is for **development use only**.

   For production, **you must generate and use your own keys**, or
   anyone will be able to sign binaries for your boards. See
   :ref:`howto-mcuboot-keys` for details.

When using a BLE Nano 2, run this from the ``zmp`` directory you made
earlier::

  ./zmp build -b nrf52_blenano2 zephyr/samples/hello_world/

For nRF52 DK, use ``-b nrf52_pca10040``; for nRF52840 DK, use ``-b
nrf52840_pca10056``.

(For more information, see :ref:`ref-zephyr-zmp-build`.)

Connect to the Board's Console
------------------------------

Next, connect to your board's console so you'll be able to see the
message printed when you flash the application in the next step.

- Make sure your board is plugged into your computer via USB. A serial
  port device (usually named ``/dev/ttyACM0`` or ``/dev/ttyUSB0`` on
  Linux, but the number may change if you've got other devices plugged
  in) should be created when the board enumerates if it supports USB
  serial.

- Open the device with your favorite serial console program\
  [#serial]_ at 115200 baud.

Flash MCUboot and the Application
---------------------------------

Now you'll flash MCUBoot and the ``hello-world`` application to your board.

When using BLE Nano 2, run this from the the Zephyr microPlatform
directory::

  ./zmp flash -b nrf52_blenano2 zephyr/samples/hello_world/

For nRF52 DK, use ``-b nrf52_pca10040``; for nRF52840 DK, use ``-b
nrf52840_pca10056``.

(For more information, see :ref:`ref-zephyr-zmp-flash`.)

You should now see some messages printed on the board's console.

During the flashing process:

#. The chip's flash is completely erased, and MCUboot is installed. It
   is unable to find an application, since it's a fresh install.

#. The signed "hello world" application image is flashed, and the chip
   is reset.

#. MCUBoot runs out of reset, and checks the cryptographic signature
   on the application binary.

#. Since the signature is valid, MCUboot runs the application itself.

#. The application you just built will print a "Hello World" message
   on screen.

The combined output looks like this:

.. code-block:: none

   ***** Booting Zephyr OS vX.Y.Z-NN-gabcdef *****
   [MCUBOOT] [INF] main: Starting bootloader
   [MCUBOOT] [INF] boot_status_source: Image 0: magic=unset, copy_done=0xff, image_ok=0xff
   [MCUBOOT] [INF] boot_status_source: Scratch: magic=unset, copy_done=0x0, image_ok=0xff
   [MCUBOOT] [INF] boot_status_source: Boot source: slot 0
   [MCUBOOT] [INF] boot_swap_type: Swap type: none
   [MCUBOOT] [ERR] main: Unable to find bootable image
   ***** Booting Zephyr OS vX.Y.Z-NN-gabcdef *****
   [MCUBOOT] [INF] main: Starting bootloader
   [MCUBOOT] [INF] boot_status_source: Image 0: magic=unset, copy_done=0xff, image_ok=0xff
   [MCUBOOT] [INF] boot_status_source: Scratch: magic=unset, copy_done=0x0, image_ok=0xff
   [MCUBOOT] [INF] boot_status_source: Boot source: slot 0
   [MCUBOOT] [INF] boot_swap_type: Swap type: none
   [MCUBOOT] [INF] main: Bootloader chainload address offset: 0x8000
   [MCUBOOT] [INF] main: Jumping to the first image slot
   ***** Booting Zephyr OS vX.Y.Z-NN-gabcdef *****
   Hello World! arm

If you're using another board, you may need to do something slightly
different, but the basic idea is the same: connect a serial console at
115200 baud, and run ``zmp flash`` to flash and run the program.

Change the Application and Reflash
----------------------------------

Next, make a trivial change to the application: change "Hello World"
to "Hello Zephyr microPlatform" in
:file:`zephyr/samples/hello_world/src/main.c`.

On BLE Nano 2, re-build just the application (since you don't need to
rebuild MCUboot)::

  ./zmp build -o app -b nrf52_blenano2 zephyr/samples/hello_world

Now re-flash the application only (so you don't erase the entire chip
flash as part of installing MCUboot itself)::

  ./zmp flash -o app -b nrf52_blenano2 zephyr/samples/hello_world

For nRF52 DK, use ``-b nrf52_pca10040``; for nRF52840 DK, use ``-b
nrf52840_pca10056``.

The console output will now end with:

.. code-block:: none

   Hello Zephyr microPlatform! arm

The Zephyr microPlatform development environment is now set up on your
workstation, and you've verified you can flash your device. Move on to
the next page to set up the basic LWM2M system.

.. include:: reporting-issues.include

.. _tutorial-zephyr-dependencies:

Appendix: Zephyr microPlatform Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is a list of dependencies needed to install the Zephyr microPlatform
with these instructions, which may be useful on other development platforms.

- `Device tree compiler (dtc)
  <https://git.kernel.org/pub/scm/utils/dtc/dtc.git>`_
- `Git <https://git-scm.com/>`_
- `CMake <https://cmake.org/>`_ version 3.8.2 or later
- `Ninja <https://ninja-build.org/>`_
- `GCC and G++ <https://gcc.gnu.org/>`_ with 32-bit application support
- `gperf <https://www.gnu.org/software/gperf/>`_
- `bzip2 <http://www.bzip.org/>`_
- `Python 3 <https://www.python.org/>`_ with the following packages:

  - `setuptools <https://packaging.python.org/tutorials/installing-packages/>`_
  - `PLY <http://www.dabeaz.com/ply/>`_
  - `PyYaml <http://pyyaml.org/wiki/PyYAML>`_
  - `Cryptography <https://cryptography.io/en/latest/>`_
  - `pyelftools <https://github.com/eliben/pyelftools>`_
  - `IntelHex <https://pypi.python.org/pypi/IntelHex>`_
  - `Click <http://click.pocoo.org/>`_

- `Google Repo <https://gerrit.googlesource.com/git-repo/>`_
- `GPG <https://www.gnupg.org/>`_ (optional, but strongly recommended)

.. rubric:: Footnotes

.. [#git-creds]

   If you don't want to do that, see
   https://git-scm.com/docs/gitcredentials for some alternatives.

.. [#zmpwest]

   The ``zmp`` tool is optional; it's possible to build this all
   "manually" without using this tool, but instructions are not
   provided here. To see what ``zmp`` is doing, run ``zmp --debug
   COMMAND <args>`` instead of ``zmp COMMAND <args>``.

   In the future, zmp will be replaced by Zephyr's West tool.

.. [#signatures]

   Since this tutorial is meant to help you get started, the binaries
   are signed with keys that aren't secret, and **are not suitable for
   production use**.

.. [#serial]

   On Linux, with `picocom`_::

     picocom -b 115200 /dev/ttyACM0

   On Linux or macOS, with `screen`_::

     screen /dev/ttyACM0 115200

   To use `PuTTY`_ on Windows, see `Connecting to a local serial
   line`_ in the PuTTY documentation.

.. _Zephyr:
   https://www.zephyrproject.org/

.. _MCUBoot:
   https://mcuboot.com/

.. _BLE Nano 2: https://redbear.cc/product/ble-nano-kit-2.html

.. _pyOCD: https://github.com/mbedmicro/pyOCD

.. _nRF5x Command Line Tools:
   http://infocenter.nordicsemi.com/index.jsp?topic=%2Fcom.nordic.infocenter.tools%2Fdita%2Ftools%2Fnrf5x_command_line_tools%2Fnrf5x_installation.html

.. _source.foundries.io: https://source.foundries.io

.. _HomeBrew: https://brew.sh/

.. _Zephyr's West tool: http://docs.zephyrproject.org/west/index.html

.. _Windows Subsystem for Linux: https://docs.microsoft.com/en-us/windows/wsl/about

.. _changing files in Linux directories using Windows tools: https://blogs.msdn.microsoft.com/commandline/2016/11/17/do-not-change-linux-files-using-windows-apps-and-tools/

.. _pip: https://pip.pypa.io/en/stable/installing/

.. _create a subscriber access token on foundries.io/s/:
   https://foundries.io/s/

.. _Open Source Foundries GitHub: https://github.com/OpenSourceFoundries

.. _picocom: https://github.com/npat-efault/picocom

.. _screen: http://savannah.gnu.org/projects/screen

.. _PuTTY: https://www.putty.org/

.. _Connecting to a local serial line: https://the.earth.li/~sgtatham/putty/0.69/htmldoc/Chapter3.html#using-serial
