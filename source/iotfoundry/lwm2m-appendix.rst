.. _dm-lwm2m-appendix:

=====================================================
 Appendix to LWM2M FOTA and Data Demonstration System
=====================================================

.. warning:: Content in this section is provided on a best-effort basis.

This document contains additional information related to the
:ref:`dm-lwm2m-demo`.

.. _dm-lwm2m-devices:

Additional IoT Devices
----------------------

96Boards Carbon
~~~~~~~~~~~~~~~

.. include:: carbon-bt.include

Now run this from the Zephyr microPlatform installation directory to
build the main application::

  ./genesis build -b 96b_carbon zephyr-fota-samples/dm-lwm2m

.. include:: dfu-util.include

To flash the STM32, first put your Carbon into DFU mode again. Then,
from the Zephyr microPlatform installation directory, run::

  ./genesis flash -b 96b_carbon zephyr-fota-samples/dm-lwm2m

FRDM-K64F
~~~~~~~~~

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

    ./genesis build -b frdm_k64f zephyr-fota-samples/dm-lwm2m

.. include:: pyocd.include

To flash the binaries, plug the K64F into your system via the USB
connector labeled "SDA USB". Then, from the Zephyr microPlatform installation
directory::

    ./genesis flash -b frdm_k64f zephyr-fota-samples/dm-lwm2m

.. _dm-lwm2m-appendix-leshan:

Additional Leshan Information
------------------------------

This section contains additional information for more complex use
cases or further development.

- Upstream Github:
- Data model:
- Docker container: https://github.com/linaro-technologies
- Docker Hub: https://hub.docker.com/r/linarotechnologies/
