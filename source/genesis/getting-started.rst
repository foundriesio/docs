.. highlight:: sh

.. _genesis-getting-started:

Getting Started With Genesis
============================

All you need to get started is a development board supported by
Genesis, a computer to develop on, and an Internet connection.

.. todo::

   Replace DUMMY-APP with the real "Hello World" Genesis application.
   For now, replace DUMMY-APP with "zephyr-fota-hawkbit"
   below (https://trello.com/c/Yj5vW4zf).

   (We don't want to use zephyr-fota-hawkbit because setting up a
   gateway, Hawkbit server, etc. is enough response effort to scare
   first-time users off.)

.. todo::

   Add link to a top-level "supported boards" page when that's
   ready. We can repurpose the device-support directory for that.

Get Hardware
------------

Here's what you'll need:

- A computer with a 64-bit Linux operating system (we currently test
  on `Ubuntu <https://www.ubuntu.com/download/desktop>`_ 16.04. Mac OS
  X support will be added next, and Windows support is planned.)

- A development board supported by Genesis. We recommend the `96Boards
  Nitrogen <https://www.seeedstudio.com/BLE-Nitrogen-p-2711.html>`_.

.. _install-genesis:

Install Genesis
---------------

1. Install Genesis's dependencies.

   On Ubuntu, run::

     sudo add-apt-repository ppa:linaro-maintainers/ltd
     sudo apt-get update
     sudo apt-get install genesis-dev

   (See :ref:`genesis-dependencies` for more information.)

#. Install the Zephyr SDK::


     wget -O /tmp/zephyr-sdk-setup.run https://github.com/zephyrproject-rtos/meta-zephyr-sdk/releases/download/0.9.1/zephyr-sdk-0.9.1-setup.run
     chmod +x /tmp/zephyr-sdk-setup.run
     /tmp/zephyr-sdk-setup.run

   Then set these environment variables:

   - Set ``ZEPHYR_SDK_INSTALL_DIR`` to the directory where you
     installed the SDK. The default is ``/opt/zephyr-sdk``.

   - Set ``ZEPHYR_GCC_VARIANT`` to ``zephyr``.

   |

   For example, run this, then open a new shell::

     cat >>~/.bashrc <<EOF
     export ZEPHYR_SDK_INSTALL_DIR=/opt/zephyr-sdk
     export ZEPHYR_GCC_VARIANT=zephyr
     EOF

   .. todo:: Delete if a prebuilt SDK (https://trello.com/c/Poo4E8ZS)
             is available.

   (If you want to know more, see the `Zephyr Getting Started Guide
   <https://nexus.zephyrproject.org/content/sites/site/org.zephyrproject.zephyr/dev/getting_started/getting_started.html>`_.)


#. Install software needed to flash binaries to your board.

   For 96Boards Nitrogen, see :ref:`these instructions
   <device-support-nrf52-96b_nitrogen>`.

   .. todo:: Delete if pyOCD gets bundled in Genesis
             (https://trello.com/c/wQgewcdI).

#. Set up Git\ [#gitcredentials]_::

     git config --global user.name "Your Full Name"
     git config --global user.email "your-email-address@example.com"
     git config --global credential.helper 'cache --timeout=3600'

#. Create a `GitHub <https://github.com/>`_ account if you don't have
   one already (it's free).

   - Make sure you can see the `Genesis SDK manifest repository
     <https://github.com/linaro-technologies/genesis-sdk-manifest>`_
     when you're logged in.

   - If you enabled `two-factor authentication
     <https://github.com/blog/1614-two-factor-authentication>`_ on
     your GitHub account, you also need a `personal access token
     <https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/>`_.
     Give this token at least "repo" access, and make sure you keep a
     copy.

   .. todo:: Handle the "public" versus "private" cases. The above is
             needed for the "private" case.

#. Fetch the Genesis repositories::

     mkdir genesis && cd genesis
     repo init -u https://github.com/linaro-technologies/genesis-sdk-manifest
     repo sync

   When prompted by ``repo init``, enter your GitHub username and
   password (or access token).

   .. note::

      If you're new to repo, the basic idea is that the manifest has
      an XML file which describes where the Genesis code,
      documentation, and other Git repositories are.

      Running ``repo init`` with the Genesis manifest sets up the
      ``genesis`` directory to house the Genesis repositories, and
      ``repo sync`` clones the repositories onto your computer.

Build an Application
--------------------

Now that you've installed Genesis, it's time to build a demonstration
application.

If you're using 96Boards Nitrogen, run this from the ``genesis``
directory you made earlier::

  ./genesis build DUMMY-APP

If you're using another board, run this instead::

  ./genesis build -b your_board DUMMY-APP

Where ``your_board`` is Zephyr's name for your board. (Here's a `list
of Zephyr boards
<https://www.zephyrproject.org/doc/boards/boards.html>`_, but some of
them may not work with Genesis.)

(If you want to know more, see :ref:`genesis-build`.)

Flash the Application
---------------------

.. warning:: This functionality isn't supported yet, but will work
             this way when it's ready.

Now you'll flash the application to your board.

If you're using 96Boards Nitrogen, plug it into your computer via USB,
then run this from the Genesis directory::

  ./genesis flash DUMMY-APP

If you're using another board, make sure it's connected, and use this
instead::

  ./genesis flash -b your_board DUMMY-APP

Congratulations; you've just flashed a bootloader and
cryptographically signed application binaries\ [#signatures]_ you
built in the previous step onto your board!

From now on, when you power on or reset the board, the bootloader will
run first. It will check the signature on the application binary
(DUMMY-APP in this case), and if it's valid, will run the application
itself.

Test the Application
--------------------

.. Note that this section doesn't apply if you're using
   zephyr-fota-hawkbit.

You're now ready to test the application itself.

If you're using a 96Boards Nitrogen:

- Make sure it's plugged into computer via USB. A serial port device
  (usually named ``/dev/ttyACM0`` on Linux, but the number may change
  if you've got other devices plugged in) will be created when the
  board enumerates.
- Open the device with your favorite serial console program\
  [#serial]_ at 115200 baud.
- Reset the chip by pressing the RST button on the board.

You should see the message printed in the serial console.

If you're using another board, you may need to do something slightly
different, but the basic idea is the same: connect a serial console at
115200 baud, and reset the chip.

That's it! You've successfully installed Genesis, compiled an
application, flashed it to a device, and seen it work.

Onwards!
--------

You're now ready to take your next steps.

.. todo:: Add links to next steps documents when they're ready.

          Example of tutorials and reference docs:

          - Genesis overview (different projects with links to their
            reference docs, how they tie together, e.g. description of
            boot process with links to mcuboot documentation).
          - Hardware peripheral tutorials (UART, SPI, etc.)
          - Internet connectivity with an Exodus gateway
          - FOTA with hawkBit

.. _genesis-dependencies:

Appendix: Genesis Dependencies
------------------------------

Here is a list of dependencies needed to install Genesis with these
instructions, which may be useful on other development platforms.

- `Git <https://git-scm.com/>`_
- `GNU Make <https://www.gnu.org/software/make/>`_
- `GCC and G++ <https://gcc.gnu.org/>`_ with 32-bit application support
- `bzip2 <http://www.bzip.org/>`_
- `Python 3 <https://www.python.org/>`_ with the following packages:

  - `setuptools <https://packaging.python.org/installing/>`_
  - `Sphinx <http://www.sphinx-doc.org/en/stable/>`_
  - `PLY <http://www.dabeaz.com/ply/>`_
  - `PyYaml <http://pyyaml.org/wiki/PyYAML>`_
  - `Crypto <https://www.dlitz.net/software/pycrypto/>`_

- `Google Repo <https://gerrit.googlesource.com/git-repo/>`_
- `wget <https://www.gnu.org/software/wget/>`_

.. rubric:: Footnotes

.. [#gitcredentials]

   The last line caches Git usernames and passwords you enter in
   memory for one hour; this allows ``repo sync`` to work unprompted
   in the next step. If you don't want to do this, see
   https://git-scm.com/docs/gitcredentials for alternatives.

.. [#signatures]

   Since this tutorial is meant to help you get started, the binaries
   are signed with keys that aren't secret, and **are not suitable for
   production use**. When it's time to ship, see
   :ref:`genesis-production-workflow` for more information.

.. [#serial]

   On Linux, with `picocom <http://code.google.com/p/picocom/>`_::

     picocom -b 115200 /dev/ttyACM0

   On Linux, with `screen <http://savannah.gnu.org/projects/screen>`_::

     screen /dev/ttyACM0 115200

   To use `PuTTY <http://www.putty.org/>`_ on another computer running
   Windows, see `Connecting to a local serial line
   <https://the.earth.li/~sgtatham/putty/0.69/htmldoc/Chapter3.html#using-serial>`_
   in the PuTTY documentation.
