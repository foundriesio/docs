i.MX 6ULL Evaluation Kit with SE050ARD
========================================

This document will walk a developer through the steps of installing a
FoundriesFactory image with the SE050 hardware enabled onto the NXP
``imx6ullevk`` that is connected to the NXP OM-SE050ARD development platform.

.. note::
    An image created in the factory with the SE050 enabled will not boot on
    boards without the SE050 properly attached.

Attaching the SE050
-------------------

Using four male to male jumper wires (Arduino Compatible Pin size)
connect the two boards as follows:

.. figure:: /_static/boards/imx6ullevk.png
     :width: 400
     :align: center

     imx6ullevk

.. figure:: /_static/boards/se050ard.png
     :width: 400
     :align: center

     SE050ARD

Connect the signals as follows:

+----------+--------------+-------------+
|  Signal  |  imx6ullevk  | OM-SE050ARD |
+==========+==============+=============+
| SCL      | J1704 pin 10 | J2 pin 10   |
+----------+--------------+-------------+
| SDA      | J1704 pin 9  | J2 pin 9    |
+----------+--------------+-------------+
| VDD_3V3  | J1705 pin 4  | J8 pin 4    |
+----------+--------------+-------------+
| GND      | J1704 pin 7  | J2 pin 7    |
+----------+--------------+-------------+

.. note::
    The ``J1704`` and ``J1705`` headers are located in the center of the
    imx6ullevk board (Arduino headers).

Be sure that the jumpers on the SE050 evaluation board are set as follows:

.. figure:: /_static/boards/se050ard_jumpers.png
     :width: 400
     :align: center

     SE050 Jumper Settings

Lastly the connected boards should look like this:

.. figure:: /_static/boards/se050ard_imx6ull.jpg
     :width: 400
     :align: center

     Wire Connections Between Boards

Installing the FoundriesFactory Image
-------------------------------------

Download the images that have the SE050 enabled from the factory following
the instructions in :ref:`ref-rm_board_imx6ullevk`.

.. note::
    A reference on the needed changes to enable the SE050 middleware can be
    found in :ref:`ref-security_se050_enablement`.
