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

Make sure you have set up dependencies as described in
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

     brew install dtc python3 repo gpg
     pip3 install --user ply pyyaml cryptography pyelftools intelhex

#. Install the tools you need to flash your board.

   For `BLE Nano 2`_, you'll need `pyOCD`_, which you can install
   with `Python 2 from HomeBrew`_::

     brew install python cmake
     pip2 install --user pyOCD
     export PATH=$PATH:$HOME/Library/Python/2.7/bin

   Otherwise, check your board's documentation.

#. Configure your username and password in Git::

     git config --global user.name "Your Full Name"
     git config --global user.email "your-email-address@example.com"

Your build environment is now ready; continue by following the steps
in :ref:`tutorial-zephyr-install`.

Windows 10 (Experimental)
~~~~~~~~~~~~~~~~~~~~~~~~~

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

   On Ubuntu 16.04::

     sudo add-apt-repository ppa:osf-maintainers/ppa
     sudo apt-get update
     sudo apt-get install zmp-dev
     pip3 install --user pyelftools cryptography intelhex

   On other distributions, see :ref:`tutorial-zephyr-dependencies`.

#. Install the tools you need to flash your board.

   For `BLE Nano 2`_, you'll need `pyOCD`_, which you can install
   with `pip`_::

     pip install --user pyOCD

   On Linux platforms, you also need to install the following udev
   rules as root, then unplug and plug back in any boards you may have
   connected::

     echo 'ATTR{idProduct}=="0204", ATTR{idVendor}=="0d28", MODE="0666", GROUP="plugdev"' > /etc/udev/rules.d/50-cmsis-dap.rules

#. Configure your username and password in Git::

     git config --global user.name "Your Full Name"
     git config --global user.email "your-email-address@example.com"

Your system is now ready to install the Zephyr microPlatform.

.. _tutorial-zephyr-install:

Install the Zephyr microPlatform
--------------------------------

The Zephyr microPlatform can be installed in any directory on your
workstation. Installation uses the Repo tool to fetch a variety of Git
repositories at known-good revisions, and keep them in sync as time
goes on.

If you're new to Repo and want to know more, see :ref:`ref-zephyr-repo`.

Subscribers
~~~~~~~~~~~

The latest continuous release is available to Zephyr microPlatform
subscribers from source.foundries.io. Install it as follows.

#. Configure Git to cache usernames and passwords you enter in memory for
   one hour::

     git config --global credential.helper 'cache --timeout=3600'

   Using some credential helper is necessary for ``repo sync`` to work
   properly later\ [#git-creds]_.

#. If you haven't already, `create a subscriber token on
   foundries.io/s/`_.

#. Make an installation directory for the Zephyr microPlatform, and
   change into its directory::

     mkdir zmp && cd zmp

#. Install the latest release using ``repo``::

     repo init -u https://source.foundries.io/zmp-manifest
     repo sync

   When prompted by ``repo init``, enter your subscriber token for
   your username and nothing for the password.

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

Now that you've installed the Zephyr microPlatform, it's time to build a
demonstration application.

Since one of the main features of the microPlatform is making it easy
to build application binaries which are cryptographically checked by
MCUBoot, a secure bootloader, you'll first build a simple "Hello
World" application provided by MCUBoot.

.. warning::

   This cryptographic verification uses a publicly available RSA key
   pair bundled with MCUBoot, for ease of demonstration. The private
   key is in :file:`mcuboot/root-rsa-2048.pem`; the public key is
   embedded in the sources in :file:`boot/zephyr/keys.c`. This key
   pair is for **development use only**.

   For secure deployment, **you must generate and use your own keys**
   in your production image build environment.

When using a BLE Nano 2, run this from the ``zmp`` directory you made
earlier::

  ./zmp build -b nrf52_blenano2 mcuboot/samples/zephyr/hello-world

(For more information, see :ref:`ref-zephyr-zmp-build`.)

Connect to the Board's Console
------------------------------

Next, connect to your board's console so you'll be able to see the
message printed when you flash the application in the next step.

If you're using a BLE Nano 2:

- Make sure it's plugged into computer via USB. A serial port device
  (usually named ``/dev/ttyACM0`` on Linux, but the number may change
  if you've got other devices plugged in) will be created when the
  board enumerates.
- Open the device with your favorite serial console program\
  [#serial]_ at 115200 baud.

Flash the Application
---------------------

Now you'll flash MCUBoot and the ``hello-world`` application to your board.

When using BLE Nano 2, run this from the the Zephyr microPlatform
directory::

  ./zmp flash -b nrf52_blenano2 mcuboot/samples/zephyr/hello-world

(For more information, see :ref:`ref-zephyr-zmp-flash`.)

You should now see some messages printed on the board's console.

When the board boots:

#. The MCUBoot bootloader runs first, and checks the cryptographic
   signature on the application binary.

#. If the signature is valid for the given binary, will run the
   application itself.

#. The application you just built will print a "Hello World" message
   on screen.

The combined output looks like this:

.. code-block:: none

   [MCUBOOT] [INF] main: Starting bootloader
   [MCUBOOT] [INF] boot_status_source: Image 0: magic=good, copy_done=0xff, image_ok=0xff
   [MCUBOOT] [INF] boot_status_source: Scratch: magic=unset, copy_done=0x2f, image_ok=0xff
   [MCUBOOT] [INF] boot_status_source: Boot source: slot 0
   [MCUBOOT] [INF] boot_swap_type: Swap type: none
   [MCUBOOT] [INF] main: Bootloader chainload address offset: 0x8000
   [MCUBOOT] [INF] main: Jumping to the first image slot
   ***** BOOTING ZEPHYR OS v1.9.99 - BUILD: Nov  8 2017 20:38:06 *****
   Hello World from Zephyr on nrf52_blenano2!

If you're using another board, you may need to do something slightly
different, but the basic idea is the same: connect a serial console at
115200 baud, and run ``zmp flash`` to flash and run the program.

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
- `GNU Make <https://www.gnu.org/software/make/>`_
- `GCC and G++ <https://gcc.gnu.org/>`_ with 32-bit application support
- `gperf <https://www.gnu.org/software/gperf/>`_
- `bzip2 <http://www.bzip.org/>`_
- `Python 3 <https://www.python.org/>`_ with the following packages:

  - `setuptools <https://packaging.python.org/installing/>`_
  - `PLY <http://www.dabeaz.com/ply/>`_
  - `PyYaml <http://pyyaml.org/wiki/PyYAML>`_
  - `Cryptography <https://cryptography.io/en/latest/>`_
  - `pyelftools <https://github.com/eliben/pyelftools>`_
  - `IntelHex <https://pypi.python.org/pypi/IntelHex>`_

- `Google Repo <https://gerrit.googlesource.com/git-repo/>`_

.. rubric:: Footnotes

.. [#git-creds]

   If you don't want to do that, see
   https://git-scm.com/docs/gitcredentials for some alternatives.

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

.. _HomeBrew: https://brew.sh/

.. _Python 2 from HomeBrew: http://docs.python-guide.org/en/latest/starting/install/osx/

.. _Windows Subsystem for Linux: https://docs.microsoft.com/en-us/windows/wsl/about

.. _changing files in Linux directories using Windows tools: https://blogs.msdn.microsoft.com/commandline/2016/11/17/do-not-change-linux-files-using-windows-apps-and-tools/

.. _pip: https://pip.pypa.io/en/stable/installing/

.. _create a subscriber token on foundries.io/s/: https://foundries.io/s/

.. _Open Source Foundries GitHub: https://github.com/OpenSourceFoundries

.. _picocom: https://github.com/npat-efault/picocom

.. _screen: http://savannah.gnu.org/projects/screen

.. _PuTTY: https://www.putty.org/

.. _Connecting to a local serial line: https://the.earth.li/~sgtatham/putty/0.69/htmldoc/Chapter3.html#using-serial
