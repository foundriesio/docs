.. _ref-rm_boards_imx6ullevk-sec:

Apalis iMX6 with the Ixora Carrier Board
========================================

.. include:: apalis-imx6-prepare.rst

Hardware Preparation
--------------------

Set up the board for updating using the manufacturing tools:

#. Ensure that the power is off (SW1)

#. Put the apalis-imx6 into Recovery Mode:

     Remove the JP2 jumper from the board

     .. figure:: /_static/boards/apalis-imx6-jp2.png
          :width: 300
          :align: center

          JP2 location

     Connect the Micro-USB cable to the X9 connector

     .. figure:: /_static/boards/apalis-imx6-usb.png
          :width: 300
          :align: center

          USB location

     Connect the two bottom pads of JP4 as in the following images

     .. figure:: /_static/boards/apalis-imx6-jp4.png
          :width: 300
          :align: center

          Recovery jumper location

     .. figure:: /_static/boards/apalis-imx6-jp4-close.jpeg
          :width: 300
          :align: center

          Recovery jumper setup

#. Power on the board by pressing the SW1 button.

Flashing
--------

Once in serial downloader mode and connected to your PC, the evaluation board
should show up as a Freescale USB device.

.. note:: Device names and IDs can slightly differ from the steps below.

.. include:: imx6-flashing.rst

To go back to run mode, disconnect the jumper from the recovery pads (JP4) and
reconnect the JP2 jumper.

Power on the board to boot the new image.
