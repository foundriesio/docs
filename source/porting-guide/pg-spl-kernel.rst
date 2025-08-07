.. _ref-pg-spl-kernel:

Kernel and Device Tree
======================

A goal of the LmP is to be as close as possible to the mainline kernel when possible,
or to use the community kernel support, depending on the board vendor.
See `supported kernel trees <https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-bsp/recipes-kernel/linux>`_.

Unlike U-Boot, not all patches need to be appended to the kernel recipe.
You need to append patches only to include features or drivers that are not upstreamed to the mainline kernel.
The device tree files can be deployed to the ``lmp-device-tree`` directory in ``meta-subscriber-overrides``.
The build generates the output ``.dtb`` file.

.. code-block:: none

    recipes-bsp/device-tree/
    ├── lmp-device-tree
    │   └── <board>.dts
    └── lmp-device-tree.bbappend

The strategy of using the dts file separate from the Linux® Kernel source helps to avoid forking the kernel when including any new dtb.
For this, LmP relies on ``lmp-device-tree``, which is based on the Yocto Project device-tree class.


For the kernel configuration, LmP makes use of the kernel fragments, using the Yocto Project mechanism also present in ``linux-yocto``.
This is different from the also common “in-tree” configuration, which uses the file ``defconfig`` to configure the kernel.

.. _ref-pg-how-to-configure-linux:

How To Configure the Linux Kernel
---------------------------------

The kernel configuration files are part of the ``lmp-kernel-cache`` repo, which have a helpful ``README`` file, and is also described in the :ref:`ref-linux-fragments`.


In short, there are several well known kernel features defined in fragment files (such as the bluetooth feature) alongside other configurations.
The ``bsp`` directory is where fragments related to the BSP are stored.

The goal is to create a ``.bbappend`` to include the fragments which define the target machine.
The set of files should look like the following:

.. code-block:: none

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

Where ``<name>`` is the kernel name for the particular kernel recipe being used.
The patch files are potential patches applied by the ``.bbappend`` file on top of the kernel source code. 
``<machine>`` is the machine name.

The ``<sub-group>`` is a BSP subgroup, following the lmp-kernel-cache directory organization.
For example, ``imx`` or ``raspberrypi``, depending on
the target machine.

It is common that the BSP fragment is defined in a ``<machine>-standard.scc`` file,
with features and configurations being organized between the other files.

The ``linux-<name>_%.bbappend`` looks like:

.. code-block:: none

    FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"
    SRC_URI += " \
       file://kernel-meta/bsp/<sub-group>/<machine>.cfg \
       file://kernel-meta/bsp/<sub-group>/<machine>.scc \
       file://kernel-meta/bsp/<sub-group>/<machine>-standard.scc \
    “

Start from the BSP kernel fragment from a close reference board, copy over those files relevant to the board.
Change the file name, and review the content configurations while reviewing the schematics or a list of needed configurations.

.. _ref-pg-new-driver:

Adding a New Kernel Driver
--------------------------

.. note::
    Out of tree kernel drivers are not supported by Foundries.io™. New modules should be fully supported by the customer.

The recommended way to add a driver or module to the Linux kernel source is by creating a recipe file under ``recipes-kernel/kernel-modules/``:

.. code-block:: none

    recipes-kernel/kernel-modules/
    └── <module>
        ├── <module>
        │   ├── COPYING
        │   ├── Makefile
        │   ├── <module>.c
        │   └── <module>.h
        └── <module>_<pv>.bb

Where ``<module>_<pv>.bb`` is:

.. code-block:: none

    SUMMARY = "Module summary"
    LICENSE = "GPLv2"
    LIC_FILES_CHKSUM = "file://COPYING;md5=12f884d2ae1ff87c09e5b7ccc2c4ca7e"

    inherit module

    SRC_URI = " \
      file://Makefile \
      file://<module>.c \
      file://<module>.h \
      file://COPYING \
    "

    S = "${WORKDIR}"

    KERNEL_MODULE_AUTOLOAD:append = "<module>"

Make sure to provide the source code and header for the new module, as well as the license and Makefile.
Also make sure to adjust the provided values as needed by the recipe (``LICENSE``, ``PV``).
