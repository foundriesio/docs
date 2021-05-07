# OpenEmbedded / Yocto Project Layers

The Linux microPlatform is composed of several OpenEmbedded and Yocto
Project layers, including the core build system, distribution, images
and BSPs.

## Linux microPlatform Base Layers

<table>
<thead>
<tr class="header">
<th>Layer</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p><a href="https://github.com/openembedded/openembedded-core">OpenEmbedded-Core</a> (Base)</p></td>
<td><p>This is the main collaboration point when working on OpenEmbedded projects and is part of the core recipes. It is distro-less and contains only emulated machine support. It also provides the default toolchain used by the Linux microPlatform (lmp) distribution.</p></td>
</tr>
<tr class="even">
<td><p><a href="https://github.com/openembedded/meta-openembedded">Meta-OpenEmbedded</a></p></td>
<td><p>This layer houses a collection of layers and recipes for the OE-core universe. Since the reduction in recipes to the core, meta-openembedded was created for everything else. There are currently approximately 650 recipes in this layer. It is used by the Linux microPlatform for additional utilities and network support.</p></td>
</tr>
<tr class="odd">
<td><p><a href="https://git.yoctoproject.org/cgit/cgit.cgi/meta-virtualization/">Meta-Virtualization</a></p></td>
<td><p>This layer provides support for building Docker, LXC, Xen, KVM, Libvirt, and associated packages necessary for constructing OE-based virtualized / container solutions. It is used by the Linux microPlatform for Docker container runtime support.</p></td>
</tr>
<tr class="even">
<td><p><a href="https://github.com/kraj/meta-clang">Meta-Clang</a></p></td>
<td><p>This layer provides clang/llvm as alternative to system C/C++ compiler for OpenEmbedded/Yocto Project based distributions.</p></td>
</tr>
<tr class="odd">
<td><p><a href="https://github.com/advancedtelematic/meta-updater">Meta-Updater</a></p></td>
<td><p>This layer provides support for OTA Software Updates using OSTree and TUF / Uptane.</p></td>
</tr>
<tr class="even">
<td><p><a href="https://git.yoctoproject.org/cgit/cgit.cgi/meta-security">Meta-Security</a></p></td>
<td><p>This layer provides security tools, hardening tools for Linux kernels and libraries for implementing security mechanisms.</p></td>
</tr>
<tr class="odd">
<td><p><a href="https://github.com/foundriesio/meta-lmp/">Meta-LMP</a> (Base)</p></td>
<td><p>This layer provides the Linux microPlatform distribution configuration, unified Kernel and images.</p></td>
</tr>
</tbody>
</table>

## Linux microPlatform BSP Layers

<table>
<thead>
<tr class="header">
<th>Layer</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p><a href="https://github.com/foundriesio/meta-lmp/">Meta-LMP</a> (BSP)</p></td>
<td><p>This layer provides the Linux microPlatform BSP definitions and configurations for the officially supported targets.</p></td>
</tr>
<tr class="even">
<td><p><a href="https://git.yoctoproject.org/cgit/cgit.cgi/meta-arm/">Meta-ARM</a></p></td>
<td><p>This layer provides support for general recipes for the ARM architecture and BSP support for ARM reference platforms.</p></td>
</tr>
<tr class="odd">
<td><a href="https://git.yoctoproject.org/cgit.cgi/meta-intel/">Meta-Intel</a></td>
<td>This is the board support layer for Intel based devices.</td>
</tr>
<tr class="even">
<td><a href="https://git.yoctoproject.org/cgit/cgit.cgi/meta-raspberrypi/">Meta-RaspberryPi</a></td>
<td>This is the board support layer for the Raspberry Pi boards.</td>
</tr>
<tr class="odd">
<td><p><a href="https://github.com/riscv/meta-riscv">Meta-RISC-V</a></p></td>
<td><p>This is the general hardware specific BSP overlay for RISC-V based devices.</p></td>
</tr>
<tr class="even">
<td><p><a href="https://git.yoctoproject.org/cgit/cgit.cgi/meta-yocto/">Meta-Yocto</a></p></td>
<td><p>This is the board support layer for the Yocto Project hardware references, such as BeagleBone Black.</p></td>
</tr>
<tr class="odd">
<td><a href="https://git.yoctoproject.org/cgit/cgit.cgi/meta-freescale/">Meta-Freescale</a></td>
<td>This is the board support layer for the Freescale platforms.</td>
</tr>
<tr class="even">
<td><p><a href="https://github.com/Freescale/meta-freescale-3rdparty">Meta-Freescale-3rdparty</a></p></td>
<td><p>This is an additional board support layer for Freescale platforms (not officially supported by Meta-Freescale maintainers).</p></td>
</tr>
<tr class="odd">
<td><a href="https://github.com/Xilinx/meta-xilinx">Meta-Xilinx</a></td>
<td>This layer provides support for Xilinx BSPs (e.g. ZynqMP).</td>
</tr>
<tr class="even">
<td><p><a href="https://github.com/Xilinx/meta-xilinx-tools">Meta-Xilinx-Tools</a></p></td>
<td><p>This layer provides support for using Xilinx tools on supported architectures (e.g. ZynqMP).</p></td>
</tr>
</tbody>
</table>

## Linux microPlatform Meta-LMP Base Layer

The Meta-LMP-Base layer provides the Linux microPlatform distribution
configuration and a base set of recipes and configs, such as a unified
Linux kernel and a set of standard images.

The Linux microPlatform distribution configuration can be found at
`conf/distro/lmp.conf` and `conf/distro/include/lmp.inc`.

The `lmp-base-console-image` recipe can be found at
`recipes-samples/images/lmp-base-console-image.bb`. You can find the
default set of packages used by the image via the
`CORE_IMAGE_BASE_INSTALL` variable.

## Linux microPlatform Meta-LMP BSP Layer

The Meta-LMP-BSP layer provides the Linux microPlatform BSP support for
the supported targets, by providing kernel recipes, u-boot configuration
fragments, WIC files, manufacturing tools scripts and so on.

This layer is meant to be used as an extension of the vendor BSP layers
(e.g. meta-freescale), but it can also handle board configuration files
for cases where the vendor layer can't be easily compatible with LmP
(e.g. layer based on an older Yocto Project release).

The main configuration file provided by this layer can be found at
`conf/machine/include/lmp-machine-custom.inc`, which gets included by
`meta-lmp-base/classes/lmp.bbclass` if available (users can decide to
use meta-lmp-base only).

Here is an example of how a BSP configuration gets extended from the
vendor BSP layer:

    # Beaglebone
    PREFERRED_PROVIDER_virtual/bootloader_beaglebone-yocto = "u-boot-fio"
    PREFERRED_PROVIDER_u-boot_beaglebone-yocto = "u-boot-fio"
    WKS_FILE_DEPENDS_append_beaglebone-yocto = " u-boot-default-script"
    PREFERRED_PROVIDER_u-boot-default-script_beaglebone-yocto = "u-boot-ostree-scr-fit"
    SOTA_CLIENT_FEATURES_append_beaglebone-yocto = " ubootenv"
    OSTREE_KERNEL_ARGS_beaglebone-yocto ?= "console=ttyS0,115200n8 ${OSTREE_KERNEL_ARGS_COMMON}"
    KERNEL_DEVICETREE_append_beaglebone-yocto = " am335x-boneblack-wireless.dtb"
    IMAGE_BOOT_FILES_beaglebone-yocto = "u-boot.img MLO boot.itb"
    KERNEL_IMAGETYPE_beaglebone-yocto = "fitImage"
    KERNEL_CLASSES_beaglebone-yocto = " kernel-lmp-fitimage "

When adding or changing the LmP BSP configuration values, please use
`meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc`
instead, which gets parsed after `lmp-machine-custom.inc` and is factory
specific.

`lmp-machine-custom.inc` should be used for LmP upstream BSP support
only.

## Customizing Linux microPlatform BSP layers list

The Linux microPlatform is composed by a set of base layers plus an
extensive list of BSP layers that are all enabled by default (see
`ref-linux-layers-meta-lmp-bsp-layers`).

As this might not necessarily be desired by everyone, LmP also allows
any Factory user to easily customize the default BSP layers enabled and
used by a Factory.

To define your own set of BSP layers (used by Bitbake), modify (or
create if your Factory was created before LmP v76) the
`lmp-manifest/conf/bblayers-factory.inc` bblayers include fragment,
replacing the BSPLAYERS variable with your own list of BSP layers. Make
sure `meta-lmp-bsp` is also included by default, unless you want to
completely define your own BSP configuration.

An example for enabling only the `meta-intel` BSP layer:

    $ cat conf/bblayers-factory.inc
    # This is a FoundriesFactory bblayers include file

    # Meta-subscriber-overrides is the main FoundriesFactory layer
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
