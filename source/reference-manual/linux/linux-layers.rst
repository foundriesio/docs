.. _ref-linux-layers:

OpenEmbedded / Yocto Layers
===========================

The Linux microPlatform is composed of several OpenEmbedded and Yocto
Project layers, including the core build system, distribution, images
and BSPs.

Linux microPlatform Layers
--------------------------

==================================    ============================================================
Layer                                 Description
==================================    ============================================================
`OpenEmbedded-Core`_ (Base)           This is the main collaboration point when working on
                                      OpenEmbedded projects and is part of the core recipes. It is
                                      distro-less and contains only emulated machine support.
                                      It also provides the default toolchain used by the Linux
                                      microPlatform (lmp) distribution.
`Meta-OpenEmbedded`_                  This layer houses a collection of layers and recipes for the
                                      OE-core universe. Since the reduction in recipes to the core,
                                      meta-openembedded was created for everything else. There are
                                      currently approximately 650 recipes in this layer. It is used by
                                      the Linux microPlatform for additional utilities and network
                                      support.
`Meta-Virtualization`_                This layer provides support for building Docker, LXC, Xen, KVM,
                                      Libvirt, and associated packages necessary for constructing
                                      OE-based virtualized / container solutions. It is used by the
                                      Linux microPlatform for Docker container runtime support.
`Meta-Updater`_                       This layer provides support for OTA Software Updates using
                                      OSTree and TUF / Uptane.
`Meta-LMP`_ (Distro)                  This layer provides the Linux microPlatform distribution
                                      configuration, unified Kernel and images.
`Meta-Intel`_ (BSP)                   This is the board support layer for Intel based devices.
`Meta-RaspberryPi`_ (BSP)             This is the board support layer for the Raspberry Pi boards.
`Meta-RISC-V`_ (BSP)                  This is the general hardware specific BSP overlay for RISC-V
                                      based devices.
`Meta-Yocto`_ (BSP)                   This is the board support layer for the Yocto Project hardware
                                      references, such as BeagleBone Black.
`Meta-Freescale`_ (BSP)               This is the board support layer for the Freescale platforms.
`Meta-Freescale-3rdparty`_ (BSP)      This is an additional board support layer for Freescale platforms
                                      (not officially supported by Meta-Freescale maintainers).
==================================    ============================================================

.. _ref-linux-layers-meta-lmp:

Linux microPlatform Meta-LMP Layer
----------------------------------

The Meta-LMP layer provides the Linux microPlatform distribution
configuration and a base set of recipes and configs, such as a unified
Linux kernel and a gateway image.

The Linux microPlatform distribution configuration can be found at
``conf/distro/lmp.conf`` and ``conf/distro/include/lmp.inc``.

The ``lmp-gateway-image`` recipe can be found at
``recipes-samples/images/lmp-gateway-image.bb``. You can find the
default set of packages used by the image via the
``CORE_IMAGE_BASE_INSTALL`` variable.

.. _OpenEmbedded-Core:
   https://github.com/openembedded/openembedded-core
.. _Meta-OpenEmbedded:
   https://github.com/openembedded/meta-openembedded
.. _Meta-Virtualization:
   https://git.yoctoproject.org/cgit/cgit.cgi/meta-virtualization/
.. _Meta-Updater:
   https://github.com/advancedtelematic/meta-updater
.. _Meta-LMP:
   https://github.com/foundriesio/meta-lmp/
.. _Meta-Intel:
   https://git.yoctoproject.org/cgit.cgi/meta-intel/
.. _Meta-RaspberryPi:
   https://git.yoctoproject.org/cgit/cgit.cgi/meta-raspberrypi/
.. _Meta-RISC-V:
   https://github.com/riscv/meta-riscv
.. _Meta-Yocto:
   https://git.yoctoproject.org/cgit/cgit.cgi/meta-yocto/
.. _Meta-Freescale:
   https://git.yoctoproject.org/cgit/cgit.cgi/meta-freescale/
.. _Meta-Freescale-3rdparty:
   https://github.com/Freescale/meta-freescale-3rdparty
