.. _ref-rm_board_imx8mqevk:

i.MX 8M Quad Evaluation Kit
===========================

.. include:: imx8mq-prepare.rst

Hardware Preparation
--------------------

Set up the board for updating using the manufacturing tools:

.. figure:: /_static/boards/imx8mqevk.png
     :width: 400
     :align: center

#. **OPTIONAL** - Only required if you have a problems and/or want to see the boot console output.

     Connect the micro-B end of the USB cable into debug port J1701.
     Connect the other end of the cable to a PC acting as a host
     terminal. Two UART connections will appear on the PC.
     On a Linux host for example::

          $ ls -l /dev/serial/by-id/
          total 0
          lrwxrwxrwx 1 root root 13 Nov 16 23:45 usb-Silicon_Labs_CP2105_Dual_USB_to_UART_Bridge_Controller_007FC3F4-if00-port0 -> ../../ttyUSB0
          lrwxrwxrwx 1 root root 13 Nov 16 23:45 usb-Silicon_Labs_CP2105_Dual_USB_to_UART_Bridge_Controller_007FC3F4-if01-port0 -> ../../ttyUSB2

     Using a serial terminal program like minicom, connect to the port 
     with ``if00`` in the name (in this example ttyUSB0) and apply the
     following configuration

          - Baud rate: 115200
          - Data bits: 8
          - Stop bit: 1
          - Parity: None
          - Flow control: None

#. Ensure that the power is off (SW701)

#. Put the imx8mqevk into programing mode:

     Switch SW801 to OFF, OFF, ON, OFF (from 1-4 bit) to boot from
     the eMMC.

     .. figure:: /_static/boards/imx8mqevk_SW1.png
          :width: 200
          :align: center

     Switch SW802 to boot from serial downloader by setting to OFF, ON (from 1-2 bit)

     .. figure:: /_static/boards/imx8mqevk_SW2.png
          :width: 300
          :align: center

     .. figure:: /_static/boards/imx8mqevk_SW2_table.png
          :width: 600
          :align: center

#. Connect your computer to the EVK board via the USB Type-C jack.

#. Connect the plug of the 12V power supply to the DC power jack J902.

#. Power on the EVK board by sliding power switch SW701 to ON.

Flashing
--------
.. note::

     Removing the power plug will not power off the board if the USB-C cable is still connected.

.. note::

     USB-C may power the board but it is not sufficient to power the board during run time
     and intermittent failures will occur.

Once in serial downloader mode and connected to your PC the evaluation board should show up as an NXP USB device.

.. include:: imx8-flashing.rst

To put the EVK into run mode, switch SW802 to internal boot by setting to
ON, OFF (from 1-2bit). This is the opposite of programming mode described previously.

Power on the EVK board by sliding power switch SW701 to ON.
