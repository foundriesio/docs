.. _ref-linux-layers:

OpenEmbedded / Yocto Project Layers
===================================

The Linux microPlatform (LmP) is composed of several OpenEmbedded and Yocto
Project layers, including the core build system, distribution, images,
and Board Support Packages (BSPs).

.. _ref-linux-layers-meta-lmp-base-layers:

LmP Base Layers
-------------------------------

==================================    ============================================================
Layer                                 Description
==================================    ============================================================
`openembedded-core`_ (Base)           Main collaboration point when working on
                                      OpenEmbedded projects, and part of the core recipes. It is
                                      distro-less and contains only emulated machine support.
                                      Provides the default toolchain used by the LmP
                                      distribution.
`meta-openembedded`_                  A collection of layers and recipes for the
                                      OE-core universe. Since the reduction in recipes to the core,
                                      meta-openembedded was created for everything else. There are
                                      currently approximately 650 recipes in this layer. It is used by
                                      the LmP for additional utilities and network
                                      support.
`meta-virtualization`_                Provides support for building Docker, LXC, Xen, KVM,
                                      Libvirt, and associated packages necessary for constructing
                                      OE-based virtualized / container solutions. It is used by the
                                      LmP for Docker container runtime support.
`meta-clang`_                         Provides clang/llvm as alternative to system C/C++
                                      compiler for OpenEmbedded/Yocto Project based distributions.
`meta-updater`_                       Provides support for OTA Software Updates using
                                      OSTree and TUF / Uptane.
`meta-security`_                      Provides security tools, hardening tools for Linux
                                      kernels and libraries for implementing security mechanisms.
`meta-lmp`_ (Base)                    This layer provides the LmP distribution
                                      configuration, unified kernel, and images.
==================================    ============================================================

.. _ref-linux-layers-meta-lmp-bsp-layers:

LmP BSP Layers
------------------------------

==================================    ============================================================
Layer                                 Description
==================================    ============================================================
`meta-lmp`_ (BSP)                     LmP BSP definitions and
                                      configurations for officially supported targets.
`meta-arm`_                           Provides support for general recipes for the ARM
                                      architecture and BSP support for ARM reference platforms.
`meta-intel`_                         Board support layer for Intel based devices.
`meta-raspberrypi`_                   Board support layer for the Raspberry Pi boards.
                                      based devices.
`meta-yocto`_                         Board support layer for the Yocto Project hardware
                                      references, such as BeagleBone Black.
`meta-freescale`_                     Board support layer for the Freescale platforms.
`meta-freescale-3rdparty`_            Additional board support layer for Freescale platforms
                                      (not officially supported by meta-Freescale maintainers).
`meta-st-stm32mp`_                    Board support layer for STMicroelectronics based devices.
`meta-tegra`_                         Board support layer for NVIDIA based devices.
`meta-ti`_                            Board support layer for Texas Instruments based devices.
`meta-xilinx`_                        Provides support for Xilinx BSPs (e.g. ZynqMP).
`meta-xilinx-tools`_                  Provides support for using Xilinx tools on supported
                                      architectures (e.g. ZynqMP).
==================================    ============================================================


.. _ref-linux-layers-meta-lmp:

The meta-lmp Base Layer
---------------------------------------

The ``meta-lmp-base`` layer provides the LmP distribution
configuration and a base set of recipes and config files, such as a unified
Linux kernel and a set of standard images.

Configuration for the LmP distro can be found at
``conf/distro/lmp.conf`` and ``conf/distro/include/lmp.inc``.

The ``lmp-base-console-image`` recipe can be found at
``recipes-samples/images/lmp-base-console-image.bb``. You can find the
default set of packages used by the image via the
``CORE_IMAGE_BASE_INSTALL`` variable.

The meta-lmp-bsp Layer
--------------------------------------

``meta-lmp-bsp`` provides the kernel recipes, u-boot configuration
fragments, WIC files, and so on for supported targets.

While primarily used as an extension of the vendor BSP layers (e.g. meta-freescale),
it can also handle board configuration for cases where the vendor layer
is not easily compatible with LmP (e.g. a layer based on an older Yocto Project release).

The main configuration can be found at ``conf/machine/include/lmp-machine-custom.inc``.
This gets included by ``meta-lmp-base/classes/lmp.bbclass`` if available (users can decide
to use ``meta-lmp-base`` only).

Here is an example of how a BSP configuration gets extended from the
vendor BSP layer::

  # Beaglebone
  PREFERRED_PROVIDER_virtual/bootloader:beaglebone-yocto = "u-boot-fio"
  PREFERRED_PROVIDER_u-boot:beaglebone-yocto = "u-boot-fio"
  WKS_FILE_DEPENDS:append:beaglebone-yocto = " u-boot-default-script"
  PREFERRED_PROVIDER_u-boot-default-script:beaglebone-yocto = "u-boot-ostree-scr-fit"
  SOTA_CLIENT_FEATURES:append:beaglebone-yocto = " ubootenv"
  OSTREE_KERNEL_ARGS:beaglebone-yocto ?= "console=ttyS0,115200n8 ${OSTREE_KERNEL_ARGS_COMMON}"
  KERNEL_DEVICETREE:append:beaglebone-yocto = " am335x-boneblack-wireless.dtb"
  IMAGE_BOOT_FILES:beaglebone-yocto = "u-boot.img MLO boot.itb"
  KERNEL_IMAGETYPE:beaglebone-yocto = "fitImage"
  KERNEL_CLASSES:beaglebone-yocto = " kernel-lmp-fitimage "

When adding or changing the LmP BSP configuration values, please use
``meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc``
instead, which gets parsed after ``lmp-machine-custom.inc`` and is
factory specific.

``lmp-machine-custom.inc`` should be used for LmP upstream BSP support
only.


Customizing the LmP BSP Layers List
-----------------------------------------------

LmP is composed of a set of base layers plus an extensive
list of BSP layers that are all enabled by default
(see :ref:`ref-linux-layers-meta-lmp-bsp-layers`).

As this is not desired by everyone, any
FoundriesFactory user can easily customize the BSP layers enabled and used
by a Factory.

To define your own set of BSP layers (used by Bitbake), modify (or
create if your Factory was created before LmP v76) the
``lmp-manifest/conf/bblayers-factory.inc`` bblayers include fragment,
replacing the ``BSPLAYERS`` variable with your own list of BSP layers.
Make sure ``meta-lmp-bsp`` is also included by default, unless you
want to completely define your own BSP configuration.

An example for enabling only the ``meta-intel`` BSP layer::

  $ cat conf/bblayers-factory.inc
  # This is a FoundriesFactory bblayers include file

  # meta-subscriber-overrides is the main FoundriesFactory layer
  # Do not remove unless you really know what you are doing.
  BASELAYERS += "${OEROOT}/layers/meta-subscriber-overrides"

  # Customize list of default BSP layers included by LMP by uncommenting
  # the following lines and manually including your own list (= to replace).
  # You can find the standard BSP list at the bblayers-bsp.inc file, which
  # gets parsed before this file.
  #
  BSPLAYERS = " \
    ${OEROOT}/layers/meta-intel \
    ${OEROOT}/layers/meta-lmp/meta-lmp-bsp \
  "

.. _OpenEmbedded-Core:
   https://github.com/openembedded/openembedded-core
.. _meta-OpenEmbedded:
   https://github.com/openembedded/meta-openembedded
.. _meta-Clang:
   https://github.com/kraj/meta-clang
.. _meta-Virtualization:
   https://git.yoctoproject.org/meta-virtualization/
.. _meta-Updater:
   https://github.com/uptane/meta-updater
.. _meta-Security:
   https://git.yoctoproject.org/meta-security
.. _meta-LMP:
   https://github.com/foundriesio/meta-lmp/
.. _meta-ARM:
   https://git.yoctoproject.org/meta-arm/
.. _meta-Intel:
   https://git.yoctoproject.org/meta-intel/
.. _meta-RaspberryPi:
   https://git.yoctoproject.org/meta-raspberrypi/
.. _meta-Yocto:
   https://git.yoctoproject.org/meta-yocto/
.. _meta-Freescale:
   https://git.yoctoproject.org/meta-freescale/
.. _meta-Freescale-3rdparty:
   https://github.com/Freescale/meta-freescale-3rdparty
.. _meta-ST-Stm32mp:
   https://github.com/STMicroelectronics/meta-st-stm32mp
.. _meta-Tegra:
   https://github.com/OE4T/meta-tegra
.. _meta-Ti:
   https://git.yoctoproject.org/meta-ti/
.. _meta-Xilinx:
   https://github.com/Xilinx/meta-xilinx
.. _meta-Xilinx-Tools:
   https://github.com/Xilinx/meta-xilinx-tools
