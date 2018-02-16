.. _ref-linux-layers:

Linux microPlatform OpenEmbedded / Yocto Layers
===============================================

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
`Meta-Linaro`_                        This layer provides OP-TEE support.
`Meta-Virtualization`_                This layer provides support for building Docker, LXC, Xen, KVM,
                                      Libvirt, and associated packages necessary for constructing
                                      OE-based virtualized / container solutions. It is used by the
                                      Linux microPlatform for Docker container runtime support.
`Meta-OSF`_ (Distro)                  This layer provides the Linux microPlatform distribution
                                      configuration, unified Kernel and images.
`Meta-RaspberryPi`_ (BSP)             This is the board support layer for the Raspberry Pi boards.
`Meta-Yocto`_ (BSP)                   This is the board support layer for the Yocto Project hardware
                                      references, such as BeagleBone Black.
`Meta-96boards`_ (BSP)                This layer is managed by Linaro and intended for boards that do
                                      not have their own board support layer repository. Currently used
                                      for HiKey / HiKey960 Consumer Edition board support.
`Meta-Qcom`_ (BSP)                    This is the board support layer for Qualcomm boards. Currently
                                      supports DragonBoard 410c and DragonBoard 820c.
`Meta-Freescale`_ (BSP)               This is the board support layer for the Freescale platforms.
`Meta-Freescale-3rdparty`_ (BSP)      This is an additional board support layer for Freescale platforms
                                      (not officially supported by Meta-Freescale maintainers).
==================================    ============================================================

.. _ref-linux-layers-meta-osf:

Linux microPlatform Meta-OSF Layer
----------------------------------

The Meta-OSF layer provides the Linux microPlatform distribution
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
.. _Meta-Linaro:
   https://git.linaro.org/openembedded/meta-linaro.git/
.. _Meta-Virtualization:
   https://git.yoctoproject.org/cgit/cgit.cgi/meta-virtualization/
.. _Meta-OSF:
   https://github.com/opensourcefoundries/meta-osf
.. _Meta-RaspberryPi:
   https://git.yoctoproject.org/cgit/cgit.cgi/meta-raspberrypi/
.. _Meta-Yocto:
   https://git.yoctoproject.org/cgit/cgit.cgi/meta-yocto/
.. _Meta-96boards:
   https://github.com/96boards/meta-96boards
.. _Meta-Qcom:
   https://github.com/ndechesne/meta-qcom
.. _Meta-Freescale:
   https://git.yoctoproject.org/cgit/cgit.cgi/meta-freescale/
.. _Meta-Freescale-3rdparty:
   https://github.com/Freescale/meta-freescale-3rdparty
