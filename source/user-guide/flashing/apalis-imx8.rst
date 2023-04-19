.. _ref-rm_boards_apalis-imx8:

Apalis iMX8 with the Ixora Carrier Board
========================================

.. include:: imx8-prepare.rst

.. include:: apalis-ixora-recovery.rst

Flashing
--------

Once in serial downloader mode and connected to your PC, the evaluation board
should show up as a Freescale USB device.

.. note:: Device names and IDs can slightly differ from the steps below.

.. include:: imx6-flashing.rst

To go back to run mode, disconnect the jumper from the recovery pads (JP4) and
reconnect the JP2 jumper.

Power on the board to boot the new image.
