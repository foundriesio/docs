.. _ref-rm_board_am62xx-sk:

Texas Instruments AM62x SKEVM
=============================

.. include:: am62xx-sk-prepare.rst

Hardware Preparation
--------------------

Set up the board for booting from MMC1 - SDCard:

#. Ensure that the power is off (remove cable from J11)

.. figure:: /_static/boards/am62xx-sk-top.png
     :width: 600
     :align: center

     AM62xx-sk top view

2. Put the am62xx-sk into boot from SDCard Mode:

.. figure:: /_static/boards/am62xx-sk-switches.png
     :width: 300
     :align: center

     Switch settings


Flashing
--------

Now, flash the ``lmp-factory-image-am62xx-evm.wic.gz`` retrieved from the
previous section to an SD Card. This contains the :term:`system image` that the
device will boot.

.. include:: generic-flashing.rst

.. figure:: /_static/boards/am62xx-sk-bottom.png
     :width: 600
     :align: center

     SDCard location
