.. _ref-rm_board_imx8mp-lpddr4-evk:

i.MX 8M Plus Evaluation Kit
===========================

.. include:: imx8mm-prepare.rst

Hardware Preparation
--------------------

Set up the board for updating using the manufacturing tools:

.. figure:: /_static/boards/imx8mp-lpddr4-evk.png
     :width: 600
     :align: center

     imx8mp-lpddr4-evk

#. **OPTIONAL** - Only required if you have problems and/or want to see the boot console output.

     Connect the micro-B end of the USB cable into debug port J23.
     Connect the other end of the cable to a PC acting as a host
     terminal. Four UART connections will appear on the PC.
     On a Linux host for example::

          $ ls -l /dev/serial/by-id/
          total 0
          lrwxrwxrwx 1 root root 13 jan 24 10:24 usb-FTDI_Quad_RS232-HS-if00-port0 -> ../../ttyUSB0
          lrwxrwxrwx 1 root root 13 jan 24 10:24 usb-FTDI_Quad_RS232-HS-if01-port0 -> ../../ttyUSB1
          lrwxrwxrwx 1 root root 13 jan 24 10:24 usb-FTDI_Quad_RS232-HS-if02-port0 -> ../../ttyUSB2
          lrwxrwxrwx 1 root root 13 jan 24 10:24 usb-FTDI_Quad_RS232-HS-if03-port0 -> ../../ttyUSB3

     Using a serial terminal program like minicom, connect to the port
     with ``if02`` in the name (in this example ttyUSB2) and apply the
     following configuration

          - Baud rate: 115200
          - Data bits: 8
          - Stop bit: 1
          - Parity: None
          - Flow control: None

#. Ensure that the power is off (SW3)

#. Put the imx8mp-lpddr4-evk into programing mode:

     Switch SW4 to OFF, OFF, OFF, ON (from 1-4 bit) as shown below.

     .. figure:: /_static/boards/imx8mp-lpddr4-evk_SW.png
          :width: 600
          :align: center

          SW4 programing settings

#. Connect your computer to the EVK board via the USB Type-C port 1 ``Download`` J6 jack.
#. Connect the USB Type-C power plug to the port 2 ``Power`` J5 jack.

#. Power on the EVK board by sliding power switch SW3 to ON.

Flashing
--------

Once in serial downloader mode and connected to your PC the evaluation board should show up as an NXP USB device.

.. include:: imx8-flashing.rst

To put the EVK into run mode, switch SW3 to eMMC setting (OFF, OFF, ON, OFF).

Power on the EVK board by sliding power switch SW3 to ON.
