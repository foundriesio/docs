.. _ref-rm_board_versal:

Versal AI Core Series VCK190 Evaluation Kit
===========================================

.. include:: versal-prepare.rst

Console/JTAG Common Hardware Preparation
----------------------------------------

Set up the board for accessing the console or using the JTAG interface

.. figure:: /_static/boards/vck190.png
     :width: 800
     :align: center

#. Connect the device end of a USB Type-C cable to the board.

#. Connect the other end of the cable to the PC host controlling the device.

#. Four UART connections will appear on the PC: one of them will be the JTAG interface, another one the console.

     On a Linux host for example you will see::

       usb 1-14.4.4.3: new high-speed USB device number 117 using xhci_hcd
       usb 1-14.4.4.3: New USB device found, idVendor=0403, idProduct=6011, bcdDevice= 8.00
       usb 1-14.4.4.3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
       usb 1-14.4.4.3: Product: VCK190
       usb 1-14.4.4.3: Manufacturer: Xilinx
       usb 1-14.4.4.3: SerialNumber: 532143136405
       ftdi_sio 1-14.4.4.3:1.0: FTDI USB Serial Device converter detected
       usb 1-14.4.4.3: Detected FT4232H
       usb 1-14.4.4.3: FTDI USB Serial Device converter now attached to ttyUSB4
       ftdi_sio 1-14.4.4.3:1.1: FTDI USB Serial Device converter detected
       usb 1-14.4.4.3: Detected FT4232H
       usb 1-14.4.4.3: FTDI USB Serial Device converter now attached to ttyUSB5
       ftdi_sio 1-14.4.4.3:1.2: FTDI USB Serial Device converter detected
       usb 1-14.4.4.3: Detected FT4232H
       usb 1-14.4.4.3: FTDI USB Serial Device converter now attached to ttyUSB6
       ftdi_sio 1-14.4.4.3:1.3: FTDI USB Serial Device converter detected
       usb 1-14.4.4.3: Detected FT4232H
       usb 1-14.4.4.3: FTDI USB Serial Device converter now attached to ttyUSB7

     Inspection of these new devices will show::

      $ ls -la /dev/serial/by-id/
      total 0
      lrwxrwxrwx 1 root root  13 sep  5 10:48 usb-Xilinx_VCK190_532143136405-if00-port0 -> ../../ttyUSB4
      lrwxrwxrwx 1 root root  13 sep  5 10:48 usb-Xilinx_VCK190_532143136405-if01-port0 -> ../../ttyUSB5
      lrwxrwxrwx 1 root root  13 sep  5 10:48 usb-Xilinx_VCK190_532143136405-if02-port0 -> ../../ttyUSB6
      lrwxrwxrwx 1 root root  13 sep  5 10:48 usb-Xilinx_VCK190_532143136405-if03-port0 -> ../../ttyUSB7

Console Hardware Configuration
------------------------------

#. Make sure the board is powered off.

#. Using a serial terminal program like minicom, connect to the port
   with ``usb-Xilinx_VCK190_532143136405-if01-port0`` in the name
   (in this example ttyUSB5) and apply the following configuration::

          - Baud rate: 115200
          - Data bits: 8
          - Stop bit: 1
          - Parity: None
          - Flow control: None

#. Power the board on.

#. You should see the Versal console printing out the boot sequence.

JTAG Hardware Preparation
----------------------------

The following steps assume that `Xilinx Serial Software Comamnd-Line Tool`_ has been installed in the system.

#. Configure the boot switches in the VCK190 for JTAG mode:

     .. figure:: /_static/boards/vck190-jtag-boot.png
          :width: 600
          :align: center

#. Prepare the boot script::

     $ cat boot.tcl
     connect
     after 1000
     target 1
     rst
     targets -set -nocase -filter {name =~ "*Versal*"}
     device program "/tmp/boot.bin"

#. Power up the board.

#. Boot the image by executing the tcl script::

     $ xsct boot.tcl

This will boot the system up to the U-boot shell.

If an LmP ready SD card was inserted in the Versal SD slot, at this point you can continue booting the Linux kernel from it.

.. _Xilinx Serial Software Comamnd-Line Tool:
    https://docs.xilinx.com/v/u/en-US/ug1208-xsct-reference-guide
