.. _ref-pg-description:

Requirements Before Porting to the LmP
======================================

It is out of the scope of this guide to detail the steps of creating a BSP with
bootloader, operating system support, and other critical packages.
The recommendation is to search for the SoC vendor porting guide.
This usually details how to port the default BSP to another board.

LmP provides a set of bootloaders and operating systems updated with the latest known vulnerability fixes.
The recommendation is to use these packages as a base for creating the new BSP.
This leads to the creation of append files (`.bbappend``) for the recipes of the packages.

LmP supports a wide variety of SoC families—from different vendors with different boot flows.
The following image shows three examples of boot flow currently supported by LmP:

.. _ref-pg-boot-flow-diagram:

.. figure:: /_static/porting-guide/boot-flow-diagram.jpg
   :align: center
   :width: 300

   Different boot flow being executed by machines supported by LmP
