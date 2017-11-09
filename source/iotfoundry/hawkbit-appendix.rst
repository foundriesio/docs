.. _dm-hawkbit-mqtt-appendix:

========================================================
 Appendix to hawkBit FOTA and MQTT Demonstration System
========================================================

.. warning:: Content in this section is provided on a best-effort basis.

This document contains additional information related to the
:ref:`dm-hawkbit-mqtt-demo`.

.. _dm-hawkbit-mqtt-devices:

Additional IoT Devices
----------------------

96Boards Carbon
~~~~~~~~~~~~~~~

.. include:: carbon-bt.include

Now run this from the Zephyr microPlatform installation directory to
build the main application::

  ./zmp build -b 96b_carbon zephyr-fota-samples/dm-hawkbit-mqtt

.. include:: dfu-util.include

To flash the STM32, first put your Carbon into DFU mode again. Then,
from the Zephyr microPlatform installation directory, run::

  ./zmp flash -b 96b_carbon zephyr-fota-samples/dm-hawkbit-mqtt

FRDM-K64F
~~~~~~~~~

.. |frdm-k64f-net-file| replace::
   ``zephyr-fota-samples/dm-hawkbit-mqtt/boards/frdm_k64f-local.conf``

.. include:: frdm-k64f-net.include

Now you can build the binaries. From the Zephyr microPlatform
installation directory::

    ./zmp build -b frdm_k64f zephyr-fota-samples/dm-hawkbit-mqtt

.. include:: pyocd.include

To flash the binaries, plug the K64F into your system via the USB
connector labeled "SDA USB". Then, from the Zephyr microPlatform installation
directory::

    ./zmp flash -b frdm_k64f zephyr-fota-samples/dm-hawkbit-mqtt

96Boards Nitrogen
~~~~~~~~~~~~~~~~~

Like FRDM-K64F, this board also requires pyOCD to flash.

To build the binaries, run this from the Zephyr microPlatform
installation directory::

  ./zmp build -b 96b_nitrogen zephyr-fota-samples/dm-hawkbit-mqtt

To flash the board::

  ./zmp flash -b 96b_nitrogen zephyr-fota-samples/dm-hawkbit-mqtt

.. _dm-hawkbit-mqtt-appendix-hawkbit:

Additional hawkBit Information
------------------------------

This section contains additional information for more complex use
cases or further development.

.. todo:: add directive for container and hub to swap in subscriber info

- Upstream Github: https://github.com/eclipse/hawkbit
- Data model: https://github.com/eclipse/hawkbit/wiki/Data-model
- Docker container: https://github.com/OpenSourceFoundries/core-containers
- Docker Hub: https://hub.docker.com/r/opensourcefoundries/hawkbit-update-server/
