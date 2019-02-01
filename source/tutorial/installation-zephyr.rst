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

Select your platform for instructions:

.. content-tabs::

   .. tab-container:: linux
      :title: Linux

      1. Install dependencies for the Zephyr microPlatform.

         On Ubuntu (16.04 and up)::

           sudo add-apt-repository ppa:fio-maintainers/ppa
           sudo apt-get update
           sudo apt-get install zmp-dev
           pip3 install --user west

         On other distributions, see :ref:`tutorial-zephyr-dependencies`.

      #. Install the tools you need to flash your board.

         For the nRF DK boards, you'll need the `nRF5x Command Line Tools`_.
         (Make sure you install the SEGGER tools too.)

         For other boards, check `your board's documentation`_.

      #. Configure your username and password in Git::

           git config --global user.name "Your Full Name"
           git config --global user.email "your-email-address@example.com"

      Your system is now ready to install the Zephyr microPlatform.

   .. tab-container:: macos
      :title: macOS

      We test on macOS Sierra (10.12).

      #. Install `HomeBrew`_.

      #. Install dependencies for the Zephyr microPlatform::

           brew install cmake ninja gperf ccache dtc python3
           pip3 install --user west

      #. Install the tools you need to flash your board.

         For the nRF DK boards, you'll need the `nRF5x Command Line Tools`_.
         (Make sure you install the SEGGER tools too.)

         For other boards, check `your board's documentation`_.

      #. Configure your username and password in Git::

           git config --global user.name "Your Full Name"
           git config --global user.email "your-email-address@example.com"

      Your system is now ready to install the Zephyr microPlatform.

   .. tab-container:: windows
      :title: Windows 10

      .. note::

         Earlier versions of Windows may work, but are not tested.

      #. Install `Chocolatey`_.

      #. Open ``cmd.exe`` as an Administrator (press Windows,
         ``cmd.exe``, right-click the result, click "Run as
         Administrator").

      #. For convenience, disable global confirmation for choco
         command entry::

           choco feature enable -n allowGlobalConfirmation

      #. Install CMake::

           choco install cmake --installargs 'ADD_CMAKE_TO_PATH=System'

      #. Install the rest of the Zephyr tools you need::

           choco install git ninja gperf dtc-msys2 python

      #. Install the tools you need to flash your board.

         For the nRF DK boards, you'll need the `nRF5x Command Line
         Tools`_. (Note Nordic recommends a particular version of the
         required SEGGER tools as well.)

         For other boards, check `your board's documentation`_.

      #. Configure your username and password in Git::

           git config --global user.name "Your Full Name"
           git config --global user.email "your-email-address@example.com"

      Your system is now ready to install the Zephyr microPlatform.

Install and Set Up a Toolchain
------------------------------

For nRF DK boards (and other boards based on ARM Cortex-M cores), the
`GNU Arm Embedded`_ toolchain works on Mac, Linux, and
Windows. Install it somewhere on your system in a directory with no
spaces in the path.

Now set these environment variables:

- :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`: set this to ``gnuarmemb``.
- :envvar:`GNUARMEMB_TOOLCHAIN_PATH`: set this to the location you
  installed the toolchain.

If you're on Linux, you can also try the `Zephyr SDK`_ as an
alternative. This comes with some additional tools, such as a recent
OpenOCD, that may be useful on non-nRF boards.

.. _tutorial-zephyr-install:

Install the Zephyr microPlatform
--------------------------------

The Zephyr microPlatform can be installed in any directory on your
workstation. These instructions create a directory named
:file:`zmp`. You can change this to anything you want.

The latest continuous release is available as open source software on
GitHub from `github.com/foundriesio`_. Install it as follows.

#. Install Zephyr microPlatform update |version| using the Zephyr
   ``west`` tool in a new directory named :file:`zmp`:

   .. parsed-literal::

      west init -m https://github.com/foundriesio/zmp-manifest --mr |manifest_tag| zmp
      cd zmp
      west update

   .. note::

      If you just want to install the latest, drop the "-\\-mr
      |manifest_tag|" option.

#. Install additional dependencies required by Zephyr and MCUboot
   (make sure you are in the :file:`zmp` directory created by ``west
   init``)::

     # Windows and macOS
     pip3 install -r zephyr/scripts/requirements.txt
     pip3 install -r mcuboot/scripts/requirements.txt
     pip3 install -r zmp-manifest/requirements.txt

     # Linux
     pip3 install --user -r zephyr/scripts/requirements.txt
     pip3 install --user -r mcuboot/scripts/requirements.txt
     pip3 install --user -r zmp-manifest/requirements.txt

   .. note::

      These requirements change with time. If something stops working
      after an update, run these lines again and retry.

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

.. _tutorial-zephyr-mcuboot:

Build and Flash MCUboot
-----------------------

Choose your board from the below options, and run the corresponding
commands from the ``zmp`` directory you made earlier to build and
flash MCUboot on the board.

.. content-tabs::

   .. tab-container:: nrf52_pca10040
      :title: nRF52 DK (nRF52832)

      .. code-block:: console

         west build -s mcuboot/boot/zephyr -d build-mcuboot -b nrf52_pca10040
         west flash -d build-mcuboot

   .. tab-container:: nrf52840_pca10056
      :title: nRF52840 DK

      .. code-block:: console

         west build -s mcuboot/boot/zephyr -d build-mcuboot -b nrf52840_pca10056
         west flash -d build-mcuboot

You will see something that looks like the following:

.. code-block:: none

   ***** Booting Zephyr OS zephyr-v1.13.0-4453-gf2ef52f122 *****
   [00:00:00.004,333] <inf> mcuboot: Starting bootloader
   [00:00:00.010,986] <inf> mcuboot: Image 0: magic=unset, copy_done=0x3, image_ok=0x3
   [00:00:00.019,348] <inf> mcuboot: Scratch: magic=unset, copy_done=0xc0, image_ok=0x3
   [00:00:00.027,801] <inf> mcuboot: Boot source: slot 0
   [00:00:00.036,193] <inf> mcuboot: Swap type: none
   [00:00:00.041,503] <err> mcuboot: Unable to find bootable image

.. important::

   The default MCUboot build uses a publicly available RSA key pair
   bundled with MCUBoot (:file:`mcuboot/root-rsa-2048.pem`) for ease
   of demonstration.

   This key pair is for **development use only**.

   For production, **you must generate and use your own keys**, or
   anyone will be able to sign binaries for your boards. See
   :ref:`howto-mcuboot-keys` for details on how to do this.

MCUboot is now installed on your board. You only need to do this once;
from now on, you'll just install bootable application images onto the
same board to be loaded and run by MCUboot. No Zephyr application is
available on the flash which can be loaded by MCUboot yet, though,
which explains the ``Unable to find bootable image`` error message.

Let's fix that now.

.. _tutorial-zephyr-hello_world:

Build and Flash "Hello World" for MCUBoot
-----------------------------------------

Now it's time to build and flash Zephyr's ``hello_world`` app. Unlike
the Zephyr getting started tutorial, you're going to build and flash
it as an application image which can be loaded by the MCUboot
bootloader that's already on your board.

.. content-tabs::

   .. tab-container:: nrf52_pca10040
      :title: nRF52 DK (nRF52832)

      .. code-block:: console

         west build -s zephyr/samples/hello_world -d build-hello \
                    -b nrf52_pca10040 -- -DCONFIG_BOOTLOADER_MCUBOOT=y
         west sign -t imgtool -d build-hello -- --key mcuboot/root-rsa-2048.pem
         west flash -d build-hello --hex-file zephyr.signed.hex

   .. tab-container:: nrf52840_pca10056
      :title: nRF52840 DK

      .. code-block:: console

         west build -s zephyr/samples/hello_world -d build-hello \
                    -b nrf52840_pca10056 -- -DCONFIG_BOOTLOADER_MCUBOOT=y
         west sign -t imgtool -d build-hello -- --key mcuboot/root-rsa-2048.pem
         west flash -d build-hello --hex-file zephyr.signed.hex

.. note::

   This requires that ``west flash`` for your board supports (and in
   fact prefers) to flash Intel Hex files. This is the case for the
   flash back-end which uses the nRF5x Command Line Tools.

When running ``west flash``, the board should reset and the console
should print messages that look roughly like this:

.. code-block:: none

   ***** Booting Zephyr OS vX.Y.Z-NN-gabcdef *****
   [MCUBOOT] [INF] main: Starting bootloader
   [MCUBOOT] [INF] boot_status_source: Image 0: magic=unset, copy_done=0xff, image_ok=0xff
   [MCUBOOT] [INF] boot_status_source: Scratch: magic=unset, copy_done=0x0, image_ok=0xff
   [MCUBOOT] [INF] boot_status_source: Boot source: slot 0
   [MCUBOOT] [INF] boot_swap_type: Swap type: none
   [MCUBOOT] [INF] main: Bootloader chainload address offset: 0x8000
   [MCUBOOT] [INF] main: Jumping to the first image slot
   ***** Booting Zephyr OS vX.Y.Z-NN-gabcdef *****
   Hello World! <BOARD>

During this second flashing process:

#. The signed "hello world" application image is flashed, and the chip
   is reset.

#. MCUBoot runs out of reset, and checks the cryptographic signature
   on the application binary.

#. Since the signature is valid, MCUboot runs the application itself.

#. The application you just built will print a "Hello World" message
   on screen.

If you're using another board, you may need to do something slightly
different (especially depending on your flashing tools), but the basic
idea is the same.

Change the Application and Reflash
----------------------------------

Next, build and flash the dining philosophers sample.  You've already
flashed MCUboot, so just flash the new application:

.. content-tabs::

   .. tab-container:: nrf52_pca10040
      :title: nRF52 DK (nRF52832)

      .. code-block:: console

         west build -s zephyr/samples/philosophers -d build-philosophers \
                    -b nrf52_pca10040 -- -DCONFIG_BOOTLOADER_MCUBOOT=y
         west sign -t imgtool -d build-philosophers -- --key mcuboot/root-rsa-2048.pem
         west flash -d build-philosophers --hex-file zephyr.signed.hex

   .. tab-container:: nrf52840_pca10056
      :title: nRF52840 DK

      .. code-block:: console

         west build -s zephyr/samples/philosophers -d build-philosophers \
                     -b nrf52840_pca10056 -- -DCONFIG_BOOTLOADER_MCUBOOT=y
         west sign -t imgtool -d build-philosophers -- --key mcuboot/root-rsa-2048.pem
         west flash -d build-philosophers --hex-file zephyr.signed.hex

The console output will now show a text view of the famous "dining
philosophers" concurrency puzzle executing.

Next Steps
----------

So far this just seems like an extra-complicated way to flash an
ordinary Zephyr application. However, if you can continue the tutorial
at :ref:`tutorial-basic`, you'll learn how to flash an application
that can update itself over the air, using MCUboot to install updated
application images.

Alternatively, learn more about the Zephyr microPlatform in
:ref:`howto` and :ref:`ref-zephyr`.

.. include:: reporting-issues.include

.. _tutorial-zephyr-dependencies:

Appendix: Zephyr microPlatform Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is a list of dependencies needed to install the Zephyr microPlatform
with these instructions, which may be useful on other development platforms.

- `Device tree compiler (dtc)
  <https://git.kernel.org/pub/scm/utils/dtc/dtc.git>`_ version 1.4.6 or later
- `Git <https://git-scm.com/>`_
- `CMake <https://cmake.org/>`_ version 3.8.2 or later
- `Ninja <https://ninja-build.org/>`_
- `gperf <https://www.gnu.org/software/gperf/>`_
- `Python 3 <https://www.python.org/>`_ with the `west
  <https://pypi.org/project/west/>`_ project and various additional
  requirements in the :file:`requirements.txt` files mentioned above.

.. rubric:: Footnotes

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

.. _nRF5x Command Line Tools:
   https://www.nordicsemi.com/DocLib/Content/User_Guides/nrf5x_cltools/latest/UG/cltools/nrf5x_command_line_tools_lpage

.. _GNU Arm Embedded:
   https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads

.. _Zephyr SDK:
   https://docs.zephyrproject.org/latest/getting_started/installation_linux.html#install-the-zephyr-software-development-kit-sdk

.. _github.com/foundriesio: https://github.com/foundriesio

.. _HomeBrew: https://brew.sh/

.. _picocom: https://github.com/npat-efault/picocom

.. _screen: http://savannah.gnu.org/projects/screen

.. _PuTTY: https://www.putty.org/

.. _Connecting to a local serial line: https://the.earth.li/~sgtatham/putty/0.69/htmldoc/Chapter3.html#using-serial

.. _Chocolatey:
   https://chocolatey.org/

.. _your board's documentation:
   https://docs.zephyrproject.org/latest/boards/boards.html
