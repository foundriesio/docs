.. _ref-rm_board_am62xx-sk:

Texas Instruments AM62x SKEVM
=============================

.. include:: am62xx-sk-prepare.rst

Hardware Preparation
--------------------

Set up the board for booting from USB DFU mode:

#. Ensure that the power is off (remove cable from **J11**):

.. figure:: /_static/boards/am62xx-sk-top.png
     :width: 600
     :align: center

     AM62xx-sk top view

#. Put the am62xx-sk into boot from USB DFU Mode,
   changing boot switches to: ``00000000 11001010``

Flashing
--------

#. Power on the board and flash it using ``flash.sh`` from the ``ti-mfgtool-files-am62xx-evm`` directory.
   This copies the ``lmp-factory-image-am62xx-evm.wic`` image.
   The wic image contains the :term:`system image` that the device will boot.
   With ``--mmc-id 0`` param explicitly specify eMMC (id = 0) as a boot media,
   where wic image will be flashed.

.. prompt:: bash host:~$, auto

    host:~$ sudo ./ti-mfgtool-files-am62xx-evm/flash.sh --wic lmp-factory-image-am62xx-evm.wic --mmc-id 0
     Load U-Boot via DFU...
     ------------------------------------------
     DFU BOOT TIBOOT3: TIFS and R5
     ------------------------------------------
     ------------------------------------------
     DFU BOOT TISPL: TFA/OPTEE/ and A53 SPL
     ------------------------------------------
     ------------------------------------------
     DFU BOOT UBOOT: A53 UBOOT
     ------------------------------------------
     ------------------------------------------
     Exposing MMC ID = 0 via USB using UMS
     ------------------------------------------
     Detected device: /dev/sda
     Confirm flashing lmp-factory-image-am62xx-evm.wic to /dev/sda (y/N) >y
     ------------------------------------------
     Flashing /dev/sda via UMS
     ------------------------------------------
     844103680 bytes (844 MB, 805 MiB) copied, 57 s, 14,8 MB/s
     814+1 records in
     814+1 records out
     854511616 bytes (855 MB, 815 MiB) copied, 57,7472 s, 14,8 MB/s
     Flashing is finished

2. Power off the board.

Configure eMMC UDA Boot
-----------------------

#. Put the am62xx-sk into boot from eMMC UDA mode,
   changing boot switches to: ``00000000 11000010``.

#. Power on the board.
