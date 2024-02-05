.. _ref-pg:

Factory Porting Guide
======================

Introduction
------------

This section provides guidelines and suggestions on how to add support for a machine not already supported by FoundriesFactory.
The list of currently supported machines can be found under :ref:`ref-linux-supported`.

Needing to port a board could be due to:

* A new project bringing new hardware to their Factory,
* An existing project that is migrating
* Adding new hardware.

Another possible reason is to customize hardware aspects of well known hardware, but with another machine file.

The strategy used in this guide is to add support on top of the existing structure provided by the Linux® micro Platform (LmP).
The LmP  provides the needed configuration for the packages, images, and classes.
Also provided is the container runtime and OTA infrastructure integration.

As the LmP uses the Yocto Project tools, the packages and configuration files follow the Yocto Project concepts,
and are used in this guide.
Some knowledge of the Yocto Project and embedded Linux development are required.

.. tip::
   
   A `support request <https://support.foundries.io>`_ can be submitted in case help is needed.
   

In the next section, there is a description on how to find a similar reference board to base the porting work.
After that, there is a list of what is needed before starting, and how to plan the porting.
This is followed by the list of the needed packages and configurations, with suggestions on how to proceed with each one.
Lastly, a checklist is provided to help ensure all required steps have been taken.

.. toctree::
   :maxdepth: 3

   pg-reference
   pg-new-machine
   pg-distro-lmp-base
   pg-how-to-plan
   pg-machine-conf
   pg-lmp-factory-custom
   pg-spl-uboot
   pg-spl-kernel
   pg-spl-mfgtool
   pg-spl-checklist


