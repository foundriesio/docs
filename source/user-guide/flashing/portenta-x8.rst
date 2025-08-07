.. _ref-rm_board_portenta-x8:

Arduino Portenta X8
===================

.. include:: secure-boot-note.rst

.. include:: portenta-x8-prepare.rst

Hardware Preparation
--------------------

Set up the board for updating using the manufacturing tools:

.. figure:: /_static/boards/portenta-x8.png
     :width: 600
     :align: center

     portenta-x8

#. **OPTIONAL**: Only required if you have problems and/or want to see the boot console output.

   .. figure:: /_static/boards/portenta-x8-uart.png
       :width: 600
       :align: center

       UART 2 Pins

#. You may need to solder a six pin header to the **UART2** pad.

#. Connect a TTL USB to UART 3v3 adapter to the corresponding UART 2 pins on the breakout board.

#. Connect the other end of the cable to a PC acting as a host terminal. 

#. A UART connection will appear on the PC.

   On a Linux host for example:

   .. code-block:: console

      $ ls -l /dev/serial/by-id/
      total 0
      lrwxrwxrwx 1 root root 13 Dec 18 11:09 usb-FTDI_TTL_RS232-if00-port0 -> ../../ttyUSB0

   Using a serial terminal program like minicom, connect to the port
   with ``if00`` in the name (in this example ttyUSB0) and apply the
   following configuration:

      - Baud rate: 115200
      - Data bits: 8
      - Stop bit: 1
      - Parity: None
      - Flow control: None

   .. tip::
      If you are not receiving console output to swap the TX and RX pins. Most TTL
      USB to UART adaptors do not provide the cross over function.

#. Ensure that the power is off—no power input connected.

#. Put the Portenta x8 into programming mode:

     Switch **BT_SEL** to **ON** and switch **BOOT** to **ON** as shown below.

     .. figure:: /_static/boards/portenta-x8-boot.png
          :width: 600
          :align: center

          BT_SEL and BOOT programming settings

#. Connect your computer to the Portenta X8 board via either USB-C® to USB-A or USB-C® to USB-C®.
   This connection will power your board ON. It is best to use 5V supply with at least 2A via
   a USB-C® connector. Negotiating power supplies do not always work and frequent reboots
   can be detected.

Flashing
--------

Once in serial downloader mode and connected to your PC the evaluation board should show up as an NXP® USB device.

.. include:: secure-boot-pre-flash-note.rst

.. include:: imx8-flashing.rst

To put the Portenta X8 into run mode, switch **BT_SEL** and **BOOT** to **OFF**.
