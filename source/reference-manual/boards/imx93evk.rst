.. _ref-rm_board_imx93evk:

i.MX 93 Evaluation Kit
======================

.. |board_name| replace:: i.MX 93 EVK
.. |debug_port| replace:: **J1401**
.. |download_port| replace:: **J401**
.. |power_jack| replace:: **J301**
.. |power_switch| replace:: **SW301**
.. |boot_mode_switch| replace:: **SW1301**
.. |boot_mode_sdp| replace:: OFF, OFF, ON, ON
.. |boot_mode_emmc| replace:: ON, ON, ON, ON
.. |boot_mode_bits| replace:: 1-4


.. include:: imx8-prepare.rst

Hardware Preparation
--------------------

Set up the board for updating using the manufacturing tools:

.. figure:: /_static/boards/imx93evk.png
     :width: 600
     :align: center

     |board_name|

#. **OPTIONAL**—Only required if you have problems and/or want to see the boot console output.

     Connect the micro-B end of the USB cable into debug port |debug_port|.
     Connect the other end of the cable to a PC acting as a host
     terminal. Four UART connections will appear on the PC.
     On a Linux host for example::

          $ ls -l /dev/serial/by-id/
          total 0
          lrwxrwxrwx 1 root root 13 abr 20 16:20 usb-FTDI_Quad_RS232-HS-if00-port0 -> ../../ttyUSB0
          lrwxrwxrwx 1 root root 13 abr 20 16:20 usb-FTDI_Quad_RS232-HS-if01-port0 -> ../../ttyUSB1
          lrwxrwxrwx 1 root root 13 abr 20 16:20 usb-FTDI_Quad_RS232-HS-if02-port0 -> ../../ttyUSB2
          lrwxrwxrwx 1 root root 13 abr 20 16:20 usb-FTDI_Quad_RS232-HS-if03-port0 -> ../../ttyUSB3

     Using a serial terminal program like `minicom <https://salsa.debian.org/minicom-team/minicom>`_, connect to the port
     with ``if02`` in the name (in this example ttyUSB2) and apply the
     following configuration:

          - Baud rate: 115200
          - Data bits: 8
          - Stop bit: 1
          - Parity: None
          - Flow control: None

#. Ensure that the power is off (|power_switch|)

#. Put the |board_name| into programing mode:

     Switch |boot_mode_switch| to |boot_mode_sdp| (from |boot_mode_bits| bit) to Download Mode.

     .. figure:: /_static/boards/imx93evk_SW.png
          :width: 600
          :align: center

          |boot_mode_switch| dip switch

#. Connect your computer to the |board_name| board via the USB Type-C port 1 ``Download`` |download_port| jack.
#. Connect the USB Type-C power plug to the port 2 ``Power`` |power_jack| jack.

#. Power on the |board_name| board by sliding power switch |power_switch| to ON.

Flashing
--------

Once in serial downloader mode and connected to your PC the evaluation board should show up as an NXP® USB device.

.. include:: imx9-flashing.rst

To put the |board_name| into run mode by switching |boot_mode_switch| to |boot_mode_emmc| to set Cortex-A to boot from eMMC.

Power on the |board_name| board by sliding power switch |power_switch| to ON.
