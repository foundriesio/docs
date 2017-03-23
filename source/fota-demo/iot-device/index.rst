.. _iot-devices:

IoT Devices
===========

From here, you can follow instructions to set up an IoT Device to
perform FOTA updates using the hawkBit server instance you set up
earlier.

Flashing Released Binaries
--------------------------

Released binaries are available for each device in the device-specific
guides below.

.. _iot-devices-build-source:

Building From Source
--------------------

If you'd rather build from source, start by cloning the following
repositories and checking out the given commits. Then, set up a Zephyr
build environment.

Source Code Repositories
~~~~~~~~~~~~~~~~~~~~~~~~

These contain firmware and associated tools you will build and flash
to your IoT Device.

- **Zephyr**:
     - URL: https://github.com/Linaro/zephyr
     - Tag: 2017.02-bud17
- **mcuboot**
     - URL: https://github.com/Linaro/mcuboot/
     - Common bootloader (Mynewt/Zephyr) that supports dual-bank and
       signed updates
     - Tag: 2017.02-bud17
- **zephyr-fota-hawkbit**
     - Linaro firmware over the air update (FOTA) Zephyr application,
       using `hawkBit
       <https://projects.eclipse.org/projects/iot.hawkbit>`_ as
       backend process manager
     - URL: https://github.com/Linaro/zephyr-fota-hawkbit
     - Tag: 2017.02-bud17

Set Up Zephyr Environment
~~~~~~~~~~~~~~~~~~~~~~~~~

Both mcuboot and zephyr-fota-hawkbit are applications using the Zephyr
RTOS. To build them, you next need to follow `Zephyr's getting started
instructions
<https://www.zephyrproject.org/doc/getting_started/getting_started.html>`_.

.. warning::

   Make sure to use the Zephyr tree maintained by Linaro linked to
   above, and not the mainline tree in the Zephyr Getting Started
   Guide.

Signing Zephyr applications also requires the Python Crypto module to be
available in your host system. On Debian-based distributions this module
is provided by the package **python-crypto**.

Device-Specific Guides
----------------------

Now use a device-specific guide to set up your IoT Device.

.. toctree::
   :maxdepth: 2

   96b_nitrogen
   96b_carbon

Experimental ("should" work) Support:

.. toctree::
   :maxdepth: 1

   nxp_k64f

