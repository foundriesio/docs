.. _ref-rm_board_imx6ullevk:

i.MX 6ULL Evaluation Kit
========================

.. include:: secure-boot-note.rst

.. include:: imx6-prepare.rst

Hardware Preparation
--------------------

Set up the board for updating using the manufacturing tools:

.. figure:: /_static/boards/imx6ullevk.png
     :width: 400
     :align: center

     imx6ullevk

#. **OPTIONAL** - Only required if you have a problems and/or want to see the boot console output.

     Connect the micro-B end of the USB cable into debug port J1901.
     Connect the other end of the cable to a PC acting as a host
     terminal. One UART connection will appear on the PC.
     On a Linux host for example::

          $ ls -l /dev/serial/by-id/
          total 0
          lrwxrwxrwx 1 root root 13 Dec  3 13:09 usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0 -> ../../ttyUSB2

     Using a serial terminal program like minicom, connect to the port
     with ``if00`` in the name (in this example ttyUSB2) and apply the
     following configuration

          - Baud rate: 115200
          - Data bits: 8
          - Stop bit: 1
          - Parity: None
          - Flow control: None

#. Ensure that the power is off (SW2001)

#. Put the imx6ullevk into programing mode:

     Switch SW602 to boot from serial downloader by setting to OFF, ON (from 1-2 bit)

     .. figure:: /_static/boards/imx6ullevk_SW1.png
          :width: 300
          :align: center

          SW602 settings

+----------+-----------+-----------------------+
| D1/MODE1 | D2/MODE0  |  BOOT MODE            |
+==========+===========+=======================+
|  OFF     |  OFF      | Boot From Fuses       |
+----------+-----------+-----------------------+
| **OFF**  | **ON**    | **Serial Downloader** |
+----------+-----------+-----------------------+
|  ON      |  OFF      | Internal Boot         |
+----------+-----------+-----------------------+
|  ON      |  ON       | Reserved              |
+----------+-----------+-----------------------+

     Switch SW601 to device microSD by setting to OFF, OFF, ON, OFF (from 1-4 bit)

     .. figure:: /_static/boards/imx6_sw601.png
          :width: 300
          :align: center

          SW601 settings

+----------+-----------+----------+-----------+-----------------------+
| D1       | D2        | D3       | D4        |  BOOT MODE            |
+==========+===========+==========+===========+=======================+
| **OFF**  | **OFF**   | **ON**   | **OFF**   | **MicroSD**           |
+----------+-----------+----------+-----------+-----------------------+
| OFF      | OFF       | OFF      | OFF       | QSPI                  |
+----------+-----------+----------+-----------+-----------------------+
| OFF      | ON        | ON       | OFF       | EMMC                  |
+----------+-----------+----------+-----------+-----------------------+
|  ON      |  ON       | OFF      | ON        | NAND                  |
+----------+-----------+----------+-----------+-----------------------+

#. Connect your computer to the EVK board via the USB OTG jack.
#. Connect the plug of the 5V power supply to the DC power jack J2001.
#. Power on the EVK board by sliding power switch SW2001 to ON.

Flashing
--------

Once in serial downloader mode and connected to your PC the evaluation board should show up as a Freescale USB device.

.. include:: secure-boot-pre-flash-note.rst

.. include:: imx6-flashing.rst

To put the EVK into run mode, switch SW602 to ``internal boot`` by setting to
ON, OFF (from 1-2bit). This is the opposite of programming mode described previously.

Power on the EVK board by sliding power switch SW2001 to ON.
