.. _tutorial-basic-other-zephyr:

Using Other Zephyr Boards
=========================

.. warning:: Content in this section is provided on a best-effort basis.

This document contains additional information related to using the
system on other boards.

FRDM-K64F
---------

.. |frdm-k64f-net-file| replace::
   ``zephyr-fota-samples/dm-lwm2m/boards/frdm_k64f-local.conf``

.. include:: frdm-k64f-net.include

In addition, |frdm-k64f-net-file| must contain a line which specifies
the IP address of the COAP proxy. In this case, that's just the IP
address of your gateway device. To use IP address L.M.N.O, add a line
like this after the other networking configuration:

.. code-block:: kconfig

   CONFIG_LWM2M_FIRMWARE_UPDATE_PULL_COAP_PROXY_ADDR="L.M.N.O"

Now you can build the binaries. From the Zephyr microPlatform
installation directory::

    ./zmp build -b frdm_k64f zephyr-fota-samples/dm-lwm2m

.. include:: pyocd.include

To flash the binaries, plug the K64F into your system via the USB
connector labeled "SDA USB". Then, from the Zephyr microPlatform installation
directory::

    ./zmp flash -b frdm_k64f zephyr-fota-samples/dm-lwm2m

96Boards Nitrogen
-----------------

Like FRDM-K64F, this board also requires pyOCD to flash.

To build the binaries, run this from the Zephyr microPlatform
installation directory::

  ./zmp build -b 96b_nitrogen zephyr-fota-samples/dm-lwm2m

To flash the board::

  ./zmp flash -b 96b_nitrogen zephyr-fota-samples/dm-lwm2m

NRF52832 DK
-----------

This requires `nrfjprog`_ to be installed to flash.

To build the binaries, run this from the Zephyr microPlatform
installation directory::

  ./zmp build -b nrf52_pca10040 zephyr-fota-samples/dm-lwm2m

To flash the board::

  ./zmp flash -b nrf52_pca10040 zephyr-fota-samples/dm-lwm2m

Please note that the flash partitions used by this application for the
application and MCUboot override the defaults provided by the board in
upstream Zephyr.

.. _nrfjprog:
    http://infocenter.nordicsemi.com/index.jsp?topic=%2Fcom.nordic.infocenter.tools%2Fdita%2Ftools%2Fnrf5x_command_line_tools%2Fnrf5x_nrfjprogexe.html
