.. _ref-zephyr:

Zephyr microPlatform Reference Manual
=====================================

The Open Source Foundries Zephyr microPlatform is an extensible
software and hardware platform that makes it easier to develop,
secure, and maintain Internet-connected microcontroller-based embedded
devices.

The Zephyr microPlatform is based on the `Zephyr`_ real-time operating
system, and the `MCUBoot`_ secure bootloader.

It significantly simplifies the process of setting up a development
environment compared to the "vanilla" Zephyr distribution by providing:

- A `Repo`_ manifest, which automates fetching and synchronization of
  known-good combinations of source trees and build toolchains.

- A tool called ``zmp``, which acts as an optional front-end to the
  Zephyr and MCUBoot build and flash systems, and turns common tasks
  requiring multiple steps in the vanilla distributions into one-line
  shell commands.

- Reference applications which can be used in concert with the Linux
  microPlatform and cloud system containers provided by Open Source
  Foundries to create functional IOT systems to use as a basis for
  development.

.. toctree::

   zephyr-zmp
   zephyr-repo

.. _Zephyr:
   https://www.zephyrproject.org/

.. _MCUBoot:
   https://mcuboot.com/

.. _Repo:
   https://gerrit.googlesource.com/git-repo/
