Introduction
------------

This document includes suggestions and some guidelines on how to add
support for a machine not already supported by FoundriesFactory. The
list of supported machines can be found at :ref:`ref-linux-supported`.

The requirement of a new board could be due to a new project using a new
hardware (not supported yet by any software), or because an existing
project is migrating or including a new hardware.

Another possible reason is to customize hardware aspects of well known
hardware, but with another machine file.

The strategy shown on this document is to use a FoundriesFactory to add
support of a new machine on top of the existing structure provided by
LmP which already provides the needed configuration for the packages,
images and classes along with the container runtime and OTA
infrastructure integration.

The Linux microPlatform (LmP) uses the Yocto Project tools, so the
packages and configurations are a set of files following the Yocto
Project concepts which are used in this guide. Some knowledge of the
Yocto Project and embedded Linux development are required.

A support request can be entered at https://support.foundries.io/ in
case help is needed.

In the next section there is a description on how to find a similar
reference board to base the porting work. After that there is a list of
what is needed before starting and how to plan the porting. The next
part is the list of the needed packages with needed configuration and
suggestions on how to proceed with each one. At the end, a checklist is
provided to help with double checking if there is something missing.