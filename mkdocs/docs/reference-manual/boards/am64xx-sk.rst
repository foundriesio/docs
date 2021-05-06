Texas Instruments AM64x SKEVM
=============================

.. include:: am64xx-sk-prepare.rst

Hardware Preparation
--------------------

Set up the board for booting from MMC1 - SDCard:

#. Ensure that the power is off (remove cable from J8)

.. figure:: /_static/boards/am64xx-sk-top.png
     :width: 600
     :align: center

     AM64xx-sk top view

2. Put the am64xx-sk into boot from SDCard Mode:

.. figure:: /_static/boards/am64xx-sk-switches.png
     :width: 300
     :align: center

     Switch settings


Flashing
--------

.. include:: generic-flashing.rst

1. Remove the micro SDCard from the host and insert it into the socket on the bottom of the board.

.. figure:: /_static/boards/am64xx-sk-bottom.png
     :width: 600
     :align: center

     SDCard location

2. Power on the board to boot the new image.
