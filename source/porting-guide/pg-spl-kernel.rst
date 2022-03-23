.. _ref-pg-spl-kernel:

Kernel and Device Tree
======================

The LmP goal is to be as close as possible to the mainline kernel when
possible, or to use the community kernel support, depending on the board
vendor. Supported kernel trees can be found `here <https://github.com/foundriesio/meta-lmp/tree/master/meta-lmp-bsp/recipes-kernel/linux>`_.

Unlike U-Boot, not all patches need to be appended to the kernel recipe.
The user needs to append patches only to include features or drivers
that are not upstreamed to the mainline kernel. The device tree files
can be deployed to the ``lmp-device-tree`` directory in
meta-subscriber-overrides so the build generates the output ``.dtb`` file.

.. prompt:: text

    recipes-bsp/device-tree/
    ├── lmp-device-tree
    │   └── <board>.dts
    └── lmp-device-tree.bbappend

The strategy of using the dts file separate from the Linux Kernel
source helps to avoid forking the kernel when including any new
dtb, so LmP relies on ``lmp-device-tree`` which is based on the Yocto Project
device-tree class.

For the kernel configuration, LmP makes use of the kernel fragments,
using the Yocto Project mechanism also present on linux-yocto. This is
different from the also common “in-tree” configuration, which uses the
file ``defconfig`` to configure the kernel.

Creating the Kernel fragments
-----------------------------

The kernel configuration files are part of the ``lmp-kernel-cache``
repository which have a helpful README file, and is also described in
the :ref:`ref-linux-fragments`.

In short, there are several well known kernel features defined in
fragment files (such as the bluetooth feature) alongside other
configurations. The ``bsp`` directory is where fragments related
to the BSP are stored.

The goal is to create a .bbappend to include the fragments which define
the target machine. The set of files should look like the following:

.. prompt:: text

    ├── linux-<name>
    │   ├── patch-file.patch
    │   ├── another-patch-file.patch
    │   └── kernel-meta
    │       └── bsp
    │           └── <sub-group>
    │               ├── <machine>.cfg
    │               ├── <machine>.scc
    │               └── <machine>-standard.scc
    └── linux-<name>_%.bbappend

Where ``<name>`` is the kernel name for the particular kernel recipe being
used. The patch files are potential patches applied by the .bbappend
file on top of the kernel source code and ``<machine>`` is the machine name.
The ``<sub-group>`` is a BSP subgroup, following the lmp-kernel-cache
directory organization. For example, ``imx`` or ``raspberrypi``, depending on
the target machine.

It is common that the BSP fragment is defined in a
``<machine>-standard.scc`` file, with features and configurations being
organized between the other files.

The ``linux-<name>_%.bbappend`` looks like:

.. prompt:: text

    FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"
    SRC_URI += " \
       file://kernel-meta/bsp/<sub-group>/<machine>.cfg \
       file://kernel-meta/bsp/<sub-group>/<machine>.scc \
       file://kernel-meta/bsp/<sub-group>/<machine>-standard.scc \
    “

Start from the BSP kernel fragment from a close reference board, copy
over those files relevant to the reference board, change the file name,
and review the content configurations while reviewing the schematics or
a list of needed configurations.
