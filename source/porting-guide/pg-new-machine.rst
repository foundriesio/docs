.. _ref-pg-description:

What is needed before porting the board to the LmP
==================================================

It is out of the scope of this guide to detail the steps of creating a
BSP including the bootloader or the operating system support and other
critical packages - the recommendation is to search for the SoC vendor
porting guide which usually details how to port the default BSP to
another board.

LmP provides a set of bootloaders and operating systems updated with the
latest known vulnerability fixes. The recommendation is to have those
packages as a base for creating the new needed BSP which leads to the
creation of append files for the recipes of those packages.

LmP supports a wide variety of SoC families from different vendors with
different boot flows. The following image shows three examples of boot
flow currently supported by LmP:

.. _ref-pg-boot-flow-diagram:

.. figure:: /_static/porting-guide/boot-flow-diagram.jpg
   :align: center
   :width: 300

   Different boot flow being executed by machines supported by LmP