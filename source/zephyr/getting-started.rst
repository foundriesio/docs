.. highlight:: sh

.. _zephyr-getting-started:

Getting Started
===============

All you need to get started is a development board supported by
the Zephyr microPlatform, a computer to develop on, and an Internet
connection.

Get Hardware
------------

You'll need a development board supported by the Zephyr
microPlatform. We support the `BLE Nano 2`_, and other boards
on a best effort basis.

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
     pip3 install --user ply pyyaml pycrypto pyasn1 ecdsa pyelftools

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
in :ref:`zephyr-install`.

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
     pip3 install --user pyelftools

   On other distributions, see :ref:`zephyr-dependencies`.

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

.. _zephyr-install:

Install the Zephyr microPlatform
--------------------------------

The Zephyr microPlatform can be installed in any directory on your
workstation. Installation uses the Repo tool to fetch a variety of Git
repositories at known-good revisions, and keep them in sync as time
goes on.

If you're new to Repo and want to know more, see :ref:`repo-primer`.

Subscribers
~~~~~~~~~~~

The latest continuous release is available to Zephyr microPlatform
subscribers from source.foundries.io. Install it as follows.

#. Configure Git to cache usernames and passwords you enter in memory for
   one hour::

     git config --global credential.helper 'cache --timeout=3600'

   Using a credential helper is necessary for ``repo sync`` to work
   unprompted later\ [#git-creds]_.

#. If you haven't already, create a `personal access token for git on
   foundries.io`_.

   .. note:: Beta users will get their tokens via email.

   .. todo:: remove this once https://foundries.io/s/ is up

#. Make an installation directory for the Zephyr microPlatform, and
   change into its directory::

     mkdir zmp && cd zmp

#. Install the latest release using ``repo``::

     repo init -u https://source.foundries.io/zmp-manifest
     repo sync

   When prompted by ``repo init``, enter your personal access token for
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

Build an Application
--------------------

Now that you've installed the Zephyr microPlatform, it's time to build a
demonstration application.

Since one of the main features of the microPlatform is making it easy
to build application binaries which are cryptographically checked by
mcuboot, a secure bootloader, you'll first build a simple "Hello
World" application provided by mcuboot.

If you're using a BLE Nano 2, run this from the ``zmp``
directory you made earlier::

  ./zmp build -b nrf52_blenano2 mcuboot/samples/zephyr/hello-world

If you're using another board, run this instead::

  ./zmp build -b your_board mcuboot/samples/zephyr/hello-world

Where ``your_board`` is Zephyr's ``BOARD`` name for your
board. (Here's a `list of Zephyr boards
<http://docs.zephyrproject.org/boards/boards.html>`_, but some of them
may not work with the Zephyr microPlatform.)

(If you want to know more, see :ref:`zephyr-build`.)

Flash the Application
---------------------

Now you'll flash the application to your board.

If you're using BLE Nano 2, plug it into your computer via USB,
then run this from the the Zephyr microPlatform directory::

  ./zmp flash -b nrf52_blenano2 mcuboot/samples/zephyr/hello-world

If you're using another board, make sure it's connected, and use this
instead::

  ./zmp flash -b your_board mcuboot/samples/zephyr/hello-world

Congratulations; you've just flashed a bootloader and
cryptographically signed application binaries\ [#signatures]_ you
built in the previous step onto your board!

(If you want to know more, see :ref:`zephyr-flash`.)

Test the Application
--------------------

You're now ready to test the application itself.

If you're using a BLE Nano 2:

- Make sure it's plugged into computer via USB. A serial port device
  (usually named ``/dev/ttyACM0`` on Linux, but the number may change
  if you've got other devices plugged in) will be created when the
  board enumerates.
- Open the device with your favorite serial console program\
  [#serial]_ at 115200 baud.
- Reset the chip by pressing the RST button on the board.

You should see some messages printed in the serial console.

When you power on or reset the board:

#. The mcuboot bootloader runs first, and checks the cryptographic
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
115200 baud, and reset the chip.

That's it! You've successfully installed the Zephyr microPlatform, compiled an
application, flashed it to a device, and seen it work.

Onwards!
--------

You're now ready to take your next steps with the Zephyr
microPlatform. Check out :ref:`iotfoundry-top` for example systems you
can set up which let your device communicate with the cloud, receive
firmware updates, and more.

----

Appendixes
----------

.. _zephyr-dependencies:

Appendix: Zephyr microPlatform Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is a list of dependencies needed to install the Zephyr microPlatform
with these instructions, which may be useful on other development platforms.

- `Device tree compiler (dtc)
  <https://git.kernel.org/pub/scm/utils/dtc/dtc.git>`_
- `Git <https://git-scm.com/>`_
- `GNU Make <https://www.gnu.org/software/make/>`_
- `GCC and G++ <https://gcc.gnu.org/>`_ with 32-bit application support
- `bzip2 <http://www.bzip.org/>`_
- `Python 3 <https://www.python.org/>`_ with the following packages:

  - `setuptools <https://packaging.python.org/installing/>`_
  - `PLY <http://www.dabeaz.com/ply/>`_
  - `PyYaml <http://pyyaml.org/wiki/PyYAML>`_
  - `Crypto <https://www.dlitz.net/software/pycrypto/>`_
  - `ECDSA <https://pypi.python.org/pypi/ecdsa/>`_
  - `ASN.1 <http://pyasn1.sourceforge.net/>`_
  - `pyelftools <https://github.com/eliben/pyelftools>`_

- `Google Repo <https://gerrit.googlesource.com/git-repo/>`_

.. _zephyr-container:

Appendix: Zephyr microPlatform Development Container (Experimental)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can install a Docker container based on Ubuntu 16.04 which
provides a Zephyr microPlatform build environment. This will let you
compile firmware binaries, which can be useful for reproducible
builds.

However, flashing binaries from the container is neither documented
nor supported on all platforms.

#. `Install Docker`_.

#. Accessing Container Registry

   Open Source Foundries provides a continuously updated container
   registry to subscribers. Public releases to Docker Hub lag these
   subscriber releases.

#. Public releases can be fetched from `Docker Hub`_::

      docker pull opensourcefoundries/zmp-sdk

#. Subscriber releases can be fetched from hub.foundries.io::

      docker pull hub.foundries.io/zmp-sdk

   If this command fails, make sure to run ``docker login`` as described
   in :ref:`iot-gateway`.

#. **Optional**: Create a mount in your host environment to access the
   builds; see the `Docker documentation on data management`_ for more
   details.

   On **macOS only**, you can just create a directory to contain the
   SDK sources and build artifacts in your host file system. For
   example::

     mkdir zmp

#. Run the container as the ``zmp-dev`` user, granting it access
   to the host data area if you created one.

   For example::

     docker run -it -w /home/zmp-dev -u zmp-dev zmp-sdk

   If you created a directory in your macOS environment, it's easier
   to run as the root user in the container::

     docker run -it -v zmp:/root/zmp -w /root/zmp zmp-sdk

#. Set up Git inside the container::

     git config --global user.name "Your Full Name"
     git config --global user.email "your-email-address@example.com"

You can now follow the above instructions to :ref:`install the Zephyr
microPlatform <zephyr-install>` inside the running container.

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

.. _BLE Nano 2: https://redbear.cc/product/ble-nano-kit-2.html

.. _Ubuntu: https://www.ubuntu.com/download/desktop

.. _pyOCD: https://github.com/mbedmicro/pyOCD

.. _HomeBrew: https://brew.sh/

.. _Python 2 from HomeBrew: http://docs.python-guide.org/en/latest/starting/install/osx/

.. _Windows Subsystem for Linux: https://msdn.microsoft.com/commandline/wsl/about

.. _changing files in Linux directories using Windows tools: https://blogs.msdn.microsoft.com/commandline/2016/11/17/do-not-change-linux-files-using-windows-apps-and-tools/

.. _pip: https://pip.pypa.io/en/stable/installing/

.. _personal access token for git on foundries.io: https://foundries.io/s/

.. _Open Source Foundries GitHub: https://github.com/OpenSourceFoundries

.. _install Docker: https://docs.docker.com/engine/installation/

.. _Docker documentation on data management: https://docs.docker.com/engine/admin/volumes/

.. _picocom: https://github.com/npat-efault/picocom

.. _screen: http://savannah.gnu.org/projects/screen

.. _PuTTY: http://www.putty.org/

.. _Connecting to a local serial line: https://the.earth.li/~sgtatham/putty/0.69/htmldoc/Chapter3.html#using-serial

.. _Docker Hub: https://hub.docker.com/r/opensourcefoundries/lmp-sdk/
