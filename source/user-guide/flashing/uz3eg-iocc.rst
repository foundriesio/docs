.. _ref-rm_boards_uz3eg-iocc:

Avnet UltraZed SOM with UltraZed-EG IO Carrier Card
===================================================

.. include:: generic-prepare.rst

Hardware Preparation
--------------------

#. Ensure that the power switch is off (``SW8`` switch is off).

#. Install UltraZed SOM on UltraZed-EG carrier.

#. Connect the Micro-USB cable to the ``J11`` (``DUAL USB UART`` label)
   connector.

#. Connect power cord.

#. Set boot switch, which is located on SOM, to ``[1:4]`` to
   ``OFF,ON,OFF,ON``, so it boots from SD by default.


Flashing and boot
-----------------

.. note:: Device names and IDs can slightly differ from the steps below.

.. include:: generic-flashing.rst
