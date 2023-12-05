.. _ref-linux-distro:

LmP Distros
===========

LmP provides reference distros for different use cases.
These state the default configuration for the tools used by an image.
The distro definition files are under ``meta-lmp/meta-lmp-base/conf/distro``.

If you are not familiar with the concept of a *distro*, see the Yocto Project variable definition for `DISTRO`_.
Also helpful is the description of  `Poky`_ , the default reference distro used by the Yocto Project.

The LmP supported distros are:

* ``lmp``
* ``lmp-base``
* ``lmp-mfgtool``
* ``lmp-wayland``
* ``lmp-xwayland``

.. note::
   For guidance on building Targets with a different distro and customizations, read :ref:`Customizing the Distro <ref-customizing-the-distro>`.

lmp
---

The ``lmp`` is the default distro for a Factory.
The main point of this distro is to configure the packages for working with OTA, and to organize the boot sequence.
This includes the image architecture using OSTree, and installing the needed artifacts.

This is the default distro used when a Factory is created.

lmp-base
--------

``lmp-base`` is the recommended distro for bring up and low level development.
An example use case would be when the platform system is being developed or adjusted.

It overrides some configurations from ``lmp`` to generate a friendly system for development, such as:

* No support for OSTree.

* The rootfs is read-writable, and as a consequence, OTA is disabled.

* The image architecture is different. There are two directories: ``boot`` and ``root``, for the boot files and the rootfs, respectively.

* The U-Boot configuration is defined apart from ``lmp`` which provides flexibility.

* The U-Boot scripts are provided as a package and can be easily changed.

* The Linux Kernel binary, along with the required DTB files, are provided as separate files, instead of inside a boot image.
  This lets the binaries be replaced for testing purposes.

.. _ref-lmp-mfgtool:

lmp-mfgtool
-----------

The distro used to generate the ``mfgtool-files`` which provide the deploy and update tool for some machines.

.. _ref-lmp-wayland-xwayland:

lmp-wayland/lmp-xwayland
------------------------

These distros provide Wayland and XWayland support on top of the ``lmp`` distro.

.. _DISTRO: https://docs.yoctoproject.org/kirkstone/ref-manual/variables.html#term-DISTRO

.. _Poky: https://www.yoctoproject.org/software-overview/reference-distribution/
