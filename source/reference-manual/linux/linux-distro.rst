.. _ref-linux-distro:

LmP Distros
===========

LmP provides reference distros to be used in different use cases. They state the default configuration for the tools used on a FoundriesFactory. The distro definition files are under ``meta-lmp/meta-lmp-base/conf/distro``.

If you are not familiar with the concept of Distro, the Yocto Project definition can help (`term-DISTRO`_), another good document is the `Poky`_ description, which is the default distro reference used by the Yocto Project.

LmP supported distros are:

* ``lmp``
* ``lmp-base``
* ``lmp-mfgtool``
* ``lmp-wayland``
* ``lmp-xwayland``

.. note::
   For guidance on building new targets with a different distro and customizations, see: :ref:`Customizing the Distro <ref-customizing-the-distro>`.

lmp
***

The ``lmp`` is the default distro for a FoundriesFactory. The main point of this distro is to configure the packages for working with OTA, and to organize the boot sequence, including the image architecture using OSTree and installing the needed artifacts.

This is the default distro used when a FoundriesFactory is created.

lmp-base
********

The ``lmp-base`` is the distro recommended for bring up and low level development (when the platform system is being developed or adjusted, for example).

It overrides some configurations from ``lmp`` to generate a friendly system for development, such as:

* It does not support OSTree.

* The rootfs is read-writable (as the Poky's default) and as a consequence, OTA is disabled on this distro.

* The image architecture is different, there are two directories: ``boot`` and ``root``, for the boot files and the rootfs, respectively.

* The U-Boot configuration is defined apart from ``lmp`` which provides flexibility.

* The U-Boot scripts are provided as a package and can be easily changed.

* The Linux Kernel binary, along with the required DTB files, are provided as separate files, instead of inside a boot image. This way the binaries can be replaced for testing purposes.

.. _ref-lmp-mfgtool:

lmp-mfgtool
***********

The distro used to generate the ``mfgtool-files`` artifacts which provide the deploy and update tool for some machines.

.. _ref-lmp-wayland-xwayland:

lmp-wayland/lmp-xwayland
************************

The distros which provide Wayland and XWayland support on top of ``lmp`` distro.

.. _term-DISTRO: https://docs.yoctoproject.org/kirkstone/ref-manual/variables.html#term-DISTRO

.. _Poky: https://www.yoctoproject.org/software-overview/reference-distribution/
