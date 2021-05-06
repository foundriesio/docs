i.MX 8MQuad Evaluation Kit with SE050ARD
========================================

This document will walk a developer through the steps of installing a
FoundriesFactory image with the SE050 hardware enabled onto the NXP
imx8mqevk that is connected to the NXP OM-SE050ARD development platform.

An image created in the factory with the SE050 enabled will not boot on boards
without the SE050 properly attached.

Attaching the SE050
-------------------
Connect the OM-SE050ARD Arduino Compatible Development Kit to the
imx8mqevk as follows:

Using four male to male jumper wires (Arduino Compatible Pin size)
connect the two boards.

.. figure:: /_static/boards/imx8mqevk_J801.png
     :width: 400
     :align: center

     imx8mqevk

.. figure:: /_static/boards/imx8mqevk_J801_pinout.png
     :width: 400
     :align: center

     imx8mqevk i2c pinout

.. figure:: /_static/boards/se050ard.png
     :width: 400
     :align: center

     SE050ARD

Connect the signals as follows:

+----------+-------------+-------------+
|  Signal  |  imx8mqevk  | OM-SE050ARD |
+==========+=============+=============+
| SCL      | J801 pin 1  | J2 pin 10   |
+----------+-------------+-------------+
| SDA      | J801 pin 3  | J2 pin 9    |
+----------+-------------+-------------+
| VDD_3V3  | J801 pin 5  | J8 pin 5    |
+----------+-------------+-------------+
| GND      | J801 pin 2  | J2 pin 7    |
+----------+-------------+-------------+

Be sure that the jumpers on the SE050 evaluation board are
set as follows:

.. figure:: /_static/boards/se050ard_jumpers.png
     :width: 400
     :align: center

     SE050 Jumper Settings

Lastly the connected boards should look like this:

.. figure:: /_static/boards/se050ard_imx8mq.png
     :width: 400
     :align: center

     Wire Connections Between Boards

Installing the FoundriesFactory Image
-------------------------------------

Download the images that have the SE050 enabled from the factory following
the instructions in the iMX8MQevk board.
