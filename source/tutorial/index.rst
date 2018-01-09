.. _tutorial:

Getting Started Tutorial
========================

Start here for a step by step tutorial on how to install the
microPlatforms, then use them to set up an end-to-end IoT
demonstration system using the OMA Lightweight M2M (LWM2M) protocol.

A block diagram of this system is shown here, and though it is not
explicitly shown, one or more IoT devices can connect to the network
through the same gateway.

.. figure:: /_static/tutorial/lwm2m-system-diagram.svg
   :alt: LWM2M System Diagram
   :align: center
   :figwidth: 5in

Using this demonstration system, you can:

- See live data readings from your devices using the Leshan web application.

- Send commands to the device, such as turning on and off an LED.

- Use Leshan to update your IoT device firmware.

- Secure your network communication using the DTLS protocol.

To set up and use this system, follow these pages in order.

.. toctree::
   dependencies
   installation
   basic-system
   dtls-system
   other-zephyr-boards
