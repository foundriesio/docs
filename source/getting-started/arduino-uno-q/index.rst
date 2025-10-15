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

    This section is specific to Arduino UNO Q users.

The Arduino UNO Q ships with a Debian base image.
It is supported by the "Container-only Factory" solution.
Follow the :ref:`ref-gs-container-only` guide to get started.

.. note::

    To make sure your UNO Q has the latest base OS installed, checking the `Flashing a New Image to the UNO Q`_ documentation.

.. _Arduino UNO Q: https://docs.arduino.cc/hardware/uno-q/
.. _Flashing a New Image to the UNO Q: https://docs.arduino.cc/tutorials/uno-q/update-image/
