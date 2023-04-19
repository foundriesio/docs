.. _ref-rm_boards_imx8qm-mek:

NXP i.MX 8QuadMax Multisensory Enablement Kit (MEK)
===================================================

.. include:: imx8-prepare.rst

Hardware Preparation
--------------------

Set up the board for updating using the manufacturing tools:

#. Connect the micro-B end of the supplied USB cable into Debug UART port
   J18. Connect the other end of the cable to a host computer.

#. Connect Type-C into USB Type-C port ``J17``. Connect the other end of
   the cable to a host computer.

#. Use boot switch (``SW2``) to configure to boot from SDP
   (``[D1-D6]: 000100``).

     .. figure:: /_static/boards/imx8qm-mek-bootswitches.png
          :width: 300
          :align: center

          Boot switches

#. Power the board by flipping the switch (``SW1``).

Flashing
--------

Once in serial downloader mode and connected to your PC, the evaluation board
should show up as a Freescale USB device.

.. note:: Device names and IDs can slightly differ from the steps below.

.. include:: imx6-flashing.rst

Configure the boot switch (``SW2``) to boot from eMMC (``[D1-D6]: 001000``).
Power on the board to boot the new image.
