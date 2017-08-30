.. highlight:: sh

.. _zephyr-getting-started:

Getting Started
===============

All you need to get started is a development board supported by
the Zephyr microPlatform, a computer to develop on, and an Internet
connection.

.. todo::

   Add link to a top-level "supported boards" page when that's
   ready.

Get Hardware
------------

.. _96Boards Nitrogen:
   https://www.seeedstudio.com/BLE-Nitrogen-p-2711.html

.. _Ubuntu:
   https://www.ubuntu.com/download/desktop

.. _pyOCD:
   https://github.com/mbedmicro/pyOCD

Here's what you'll need:

- A development computer, running one of:

  - macOS (experimental; we test on Sierra, 10.12)
  - 64 bit Windows 10 Anniversary Update or later (experimental)
  - a 64 bit Linux distribution (we test on `Ubuntu`_ 16.04.)

- A development board supported by the Zephyr microPlatform. We
  support the `96Boards Nitrogen`_, and other boards on a best effort
  basis.

Set up Build Environment
------------------------

Before installing the the Zephyr microPlatform, you need to set up
your workstation build environment. Instructions for each supported
platform follow.

macOS
~~~~~

.. _HomeBrew:
   https://brew.sh/

.. _Python 2 from HomeBrew:
   http://docs.python-guide.org/en/latest/starting/install/osx/

#. Install `HomeBrew`_.

#. Install dependencies for the Zephyr microPlatform::

     brew install dtc python3 repo gpg
     pip3 install --user ply pyyaml pycrypto pyasn1 ecdsa pyelftools

#. Install the tools you need to flash your board.

   For `96Boards Nitrogen`_, you'll need `pyOCD`_, which you can install
   with `Python 2 from HomeBrew`_::

     brew install python
     pip2 install --user pyOCD
     export PATH=$PATH:$HOME/Library/Python/2.7/bin

   Otherwise, check your board's documentation.

#. **Optional**: Set up Git::

     git config --global user.name "Your Full Name"
     git config --global user.email "your-email-address@example.com"

#. **Optional**: If you want to build this documentation, you'll need
   some additional dependencies::

     pip3 install --user sphinx sphinx_rtd_theme

     # Replace "3.X" with the version number you have installed.
     export PATH=$PATH:$HOME/Library/Python/3.X/bin

Your build environment is now ready; continue by following the steps
in :ref:`zephyr-install`.

Windows 10 (Experimental)
~~~~~~~~~~~~~~~~~~~~~~~~~

Windows versions supporting the Windows Subsystem for Linux have
experimental support. These instructions will let you build binaries;
however, flashing support is not yet documented.

.. _Windows Subsystem for Linux:
   https://msdn.microsoft.com/en-us/commandline/wsl/install_guide

.. _changing files in Linux directories using Windows tools:
      https://blogs.msdn.microsoft.com/commandline/2016/11/17/do-not-change-linux-files-using-windows-apps-and-tools/

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

.. _pip:
   https://pip.pypa.io/en/stable/installing/

1. Install dependencies for the Zephyr microPlatform.

   On Ubuntu 16.04::

     sudo add-apt-repository ppa:linaro-maintainers/ltd
     sudo apt-get update
     sudo apt-get install genesis-dev
     pip3 install --user pyelftools

   On other distributions, see :ref:`zephyr-dependencies`.

#. Install the tools you need to flash your board.

   For `96Boards Nitrogen`_, you'll need `pyOCD`_, which you can install
   with `pip`_::

     pip install --user pyOCD

   On Linux platforms, you also need to install the following udev
   rules as root, then unplug and plug back in any boards you may have
   connected::

     echo 'ATTR{idProduct}=="0204", ATTR{idVendor}=="0d28", MODE="0666", GROUP="plugdev"' > /etc/udev/rules.d/50-cmsis-dap.rules

#. **Optional**: Set up Git::

     git config --global user.name "Your Full Name"
     git config --global user.email "your-email-address@example.com"

Your system is now ready to install the Zephyr microPlatform.

.. _zephyr-install:

Install Zephyr microPlatform
----------------------------

.. todo:: Generate instructions for other manifest repository sources.

   In these configurations, we need extra docs:

   - Cache Git usernames and passwords you enter in memory for one
     hour; this allows ``repo sync`` to work unprompted in the next
     step. If you don't want to do this, see
     https://git-scm.com/docs/gitcredentials for alternatives. ::

       git config --global credential.helper 'cache --timeout=3600'

   - If you don't already have one, create a `GitHub
     <https://github.com/>`_ account (it's free).

   - Make sure you can see the Zephyr microPlatform SDK manifest
     repository when you're logged in to your account (**needs
     link**).

   - If you enabled `two-factor authentication
     <https://github.com/blog/1614-two-factor-authentication>`_ on
     your GitHub account, you also need a `personal access token
     <https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/>`_.
     Give this token at least "repo" access, and make sure you keep a
     copy.

   - When prompted by ``repo init``, enter your GitHub username and
     password (or access token, if you use two-factor authentication).

To install the latest release, make an installation directory and
install the Zephyr microPlatform there with ``repo``::

  mkdir genesis && cd genesis
  repo init -u https://github.com/linaro-technologies/genesis-sdk-manifest
  repo sync

.. note::

   If you're new to repo and want to know more, see
   :ref:`zephyr-branching-repo`.

Build an Application
--------------------

Now that you've installed the Zephyr microPlatform, it's time to build a
demonstration application.

Since one of the main features of the microPlatform is making it easy
to build application binaries which are cryptographically checked by
mcuboot, a secure bootloader, you'll first build a simple "Hello
World" application provided by mcuboot.

If you're using 96Boards Nitrogen, run this from the ``genesis``
directory you made earlier::

  ./genesis build mcuboot/samples/zephyr/hello-world

If you're using another board, run this instead::

  ./genesis build -b your_board mcuboot/samples/zephyr/hello-world

Where ``your_board`` is Zephyr's name for your board. (Here's a `list
of Zephyr boards
<https://www.zephyrproject.org/doc/boards/boards.html>`_, but some of
them may not work with the Zephyr microPlatform.)

(If you want to know more, see :ref:`zephyr-build`.)

Flash the Application
---------------------

Now you'll flash the application to your board.

If you're using 96Boards Nitrogen, plug it into your computer via USB,
then run this from the the Zephyr microPlatform directory::

  ./genesis flash mcuboot/samples/zephyr/hello-world

If you're using another board, make sure it's connected, and use this
instead::

  ./genesis flash -b your_board mcuboot/samples/zephyr/hello-world

Congratulations; you've just flashed a bootloader and
cryptographically signed application binaries\ [#signatures]_ you
built in the previous step onto your board!

(If you want to know more, see :ref:`rtos-flash`.)

Test the Application
--------------------

You're now ready to test the application itself.

If you're using a 96Boards Nitrogen:

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
   [MCUBOOT] [INF] boot_status_source: Scratch: magic=unset, copy_done=0x23, image_ok=0xff
   [MCUBOOT] [INF] boot_status_source: Boot source: slot 0
   [MCUBOOT] [INF] boot_swap_type: Swap type: none
   [MCUBOOT] [INF] main: Bootloader chainload address offset: 0x8000
   [MCUBOOT] [WRN] zephyr_flash_area_warn_on_open: area 1 has 1 users
   [MCUBOOT] [INF] main: Jumping to the first image slot
   ***** BOOTING ZEPHYR OS v1.8.99 - BUILD: Aug 15 2017 19:41:06 *****
   Hello World from Zephyr on 96b_nitrogen!

If you're using another board, you may need to do something slightly
different, but the basic idea is the same: connect a serial console at
115200 baud, and reset the chip.

That's it! You've successfully installed the Zephyr microPlatform, compiled an
application, flashed it to a device, and seen it work.

Onwards!
--------

You're now ready to take your next steps.

.. todo:: Add links to next steps documents when they're ready.

          Example of tutorials and reference docs:

          - Zephyr microPlatform overview (different projects with links to
            their reference docs, how they tie together, e.g. description of
            boot process with links to mcuboot documentation).
          - Hardware peripheral tutorials (UART, SPI, etc.)
          - Internet connectivity with an Basic IoT Gateway
          - FOTA with hawkBit

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
  - `Sphinx <http://www.sphinx-doc.org/en/stable/>`_
  - `Sphinx RTD theme <http://docs.readthedocs.io/en/latest/theme.html>`_
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

.. _install Docker:
   https://docs.docker.com/engine/installation/

.. _Docker documentation on data management:
   https://docs.docker.com/engine/admin/volumes/

You can install a Docker container based on Ubuntu 16.04 which
provides a Zephyr microPlatform build environment. However,
instructions for flashing binaries you build with this container are
not yet provided.

#. `Install Docker`_.

#. Fetch the container::

     docker pull linarotechnologies/genesis-sdk:latest

#. **Optional**: Create a mount in your host environment to access the
   builds; see the `Docker documentation on data management`_ for more
   details.

   On **macOS only**, you can just create a directory to contain the
   SDK sources and build artifacts in your host file system. For
   example::

     mkdir genesis

#. Run the container as the ``genesis-dev`` user, granting it access
   to the host data area if you created one.

   For example::

     docker run -it -w /home/genesis-dev -u genesis-dev genesis-sdk

   If you created a directory in your macOS environment, it's easier
   to run as the root user in the container::

     docker run -it -v genesis:/root/genesis -w /root/genesis genesis-sdk

#. **Optional**: Set up Git inside the container::

     git config --global user.name "Your Full Name"
     git config --global user.email "your-email-address@example.com"

You can now follow the above instructions to :ref:`install the Zephyr
microPlatform <zephyr-install>` inside the running container.

.. rubric:: Footnotes

.. [#signatures]

   Since this tutorial is meant to help you get started, the binaries
   are signed with keys that aren't secret, and **are not suitable for
   production use**. When it's time to ship, see
   :ref:`zephyr-production-workflow` for more information.

.. [#serial]

   On Linux, with `picocom <http://code.google.com/p/picocom/>`_::

     picocom -b 115200 /dev/ttyACM0

   On Linux or macOS, with `screen
   <http://savannah.gnu.org/projects/screen>`_::

     screen /dev/ttyACM0 115200

   To use `PuTTY <http://www.putty.org/>`_ on another computer running
   Windows, see `Connecting to a local serial line
   <https://the.earth.li/~sgtatham/putty/0.69/htmldoc/Chapter3.html#using-serial>`_
   in the PuTTY documentation.
