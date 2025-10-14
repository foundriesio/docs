.. _gs-arduino-uno-q:

Arduino UNO Q
=============

The `Arduino UNO Q`_ is a single-board computer based on the Qualcomm Dragonwing™ QRB2210 System-on-Chip
(SoC) / Microprocessor (MPU), running a full Debian-based Linux environment.
It is paired with a dedicated STM32U585 Microcontroller (MCU) that allows for running Arduino sketches over Zephyr OS.

Available with 2GB RAM and 16GB built-in eMMC storage.

.. figure:: /_static/getting-started/arduino-uno-q/005_ARDUINO_UNO-Q_Front_500x386.png
   :width: 500
   :align: center
   :alt: Arduino UNO Q
   :class: dark-light

   Arduino UNO Q

.. _gs-using-uno-q-with-ff:

Using the Arduino UNO Q with FoundriesFactory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

    This section is specific to Arduino UNO Q users. Other users can skip to :ref:`tutorials`.

.. _gs-using-uno-q-with-ff-signup:

Sign Up
----------

To begin using the FoundriesFactory™ Platform, start with `creating an account <signup_>`_ with us.

.. _gs-using-uno-q-with-ff-create-factory:

Create Your Factory
-------------------

The FoundriesFactory™ Community Edition is a Factory workspace which enables you to quickly build managed applications on your Linux-based device without needing to re-flash the OS.

When your account is created, it is not associated with any factories.
The next step is to `create a Community Edition Factory for the Arduino UNO Q`_.

.. _gs-using-uno-q-with-ff-install-client:

Install the OTA Client
----------------------

The OTA update client that performs container-only management is called `Fioup`_ and it supports both Arm64 and x86 systems.

Please follow the complete instructions for setting up `Fioup`_. They include steps for installing, registering your device, performing an update and configuring `Fioup`_ to run automatically.

.. note::

    To make sure your UNO Q has the latest base OS installed, checking the `Flashing a New Image to the UNO Q`_ documentation.

.. _gs-using-uno-q-with-ff-next-steps:

Next Steps
----------

Once the OTA update client is registered with your Factory, proceed with :ref:`gs-install-fioctl` and then continue on to :ref:`gs-building-deploying-app`.

.. _Arduino UNO Q: https://docs.arduino.cc/hardware/uno-q/
.. _signup: https://app.foundries.io/signup
.. _create a Community Edition Factory for the Arduino UNO Q: https://app.foundries.io/factories/+/arduino-uno-q
.. _Fioup: https://github.com/foundriesio/fioup/blob/main/docs/README.md
.. _GitHub Release: https://github.com/foundriesio/fioup/releases
.. _Flashing a New Image to the UNO Q: https://docs.arduino.cc/tutorials/uno-q/update-image/
