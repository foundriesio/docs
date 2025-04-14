i.MX 8M Plus Evaluation Kit With SE050ARD
=========================================

This document walks through the steps of installing a FoundriesFactory™ Platform image with SE050 hardware enabled onto the NXP® ``imx8mp-lpddr4-evk``,
connected to the NXP OM-SE050ARD development platform.

.. note::
    An image created in a Factory with SE050 enabled does not boot on boards without the SE050 properly attached.

Attaching the SE050
-------------------

Using four male to male jumper wires (Arduino Compatible Pin size) connect the two boards as shown:

.. figure:: /_static/boards/imx8mp-lpddr4-evk_J22.png
     :width: 400
     :align: center

     imx8mp-lpddr4-evk

.. figure:: /_static/boards/imx8mp-lpddr4-evk_J22_pinout.png
     :width: 400
     :align: center

     imx8mp-lpddr4-evk i2c pinout

.. figure:: /_static/boards/se050ard.png
     :width: 400
     :align: center

     SE050ARD

Connect the signals as follows:

+----------+----------------------+-------------+
|  Signal  |  imx8mp-lpddr4-evk   | OM-SE050ARD |
+==========+======================+=============+
| SCL      |       J22 pin 3      | J2 pin 10   |
+----------+----------------------+-------------+
| SDA      |       J22 pin 5      | J2 pin 9    |
+----------+----------------------+-------------+
| VDD_3V3  |       J22 pin 1      | J8 pin 4    |
+----------+----------------------+-------------+
| GND      |       J22 pin 7      | J2 pin 7    |
+----------+----------------------+-------------+

Be sure that the jumpers on the SE050 evaluation board are set as shown:

.. figure:: /_static/boards/se050ard_jumpers.png
     :width: 400
     :align: center

     SE050 Jumper Settings

The connected boards should look like this:

.. figure:: /_static/boards/se050ard_imx8mp.jpg
     :width: 400
     :align: center

     Wire Connections Between Boards

Installing the FoundriesFactory Image
-------------------------------------

Download the images that have the SE050 enabled from the Factory.
Follow the instructions in :ref:`ref-rm_board_imx8mp-lpddr4-evk`.

.. note::
    A reference on the needed changes to enable the SE050 middleware can be found in :ref:`ref-security_se05x_enablement`.
