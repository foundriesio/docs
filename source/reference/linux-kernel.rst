.. _ref-linux-kernel:

Linux microPlatform Kernel
==========================

A common and unified Linux Kernel source tree is provided and used by
the Linux microPlatform. The latest continuous release is available
at `source.foundries.io/linux.git`_.

The Linux Kernel recipe can be found in the :ref:`Meta-LMP layer
<ref-linux-layers-meta-lmp>`, under the ``meta-lmp/recipes-kernel/linux``
directory.

Linux microPlatform Kernel Configuration Fragments
--------------------------------------------------

Together with the unified Linux Kernel tree, the Linux microPlatform also
provides an additional repository for the kernel configuration fragments.
The latest continuous release for the kernel configuration fragments is
available at `source.foundries.io/lmp-kernel-cache.git`_.

You can find the list of supported BSP definitions and configuration fragments
used under the ``lmp-kernel-cache/bsp`` directory.

The fragments repository works similarly to the upstream ``yocto-kernel-cache``
repository, so the same development workflow and documentation applies.
See the `Yocto Project Linux Kernel Development Manual`_ for more information
on how to work and manage the kernel metadata and configuration fragments.

.. _source.foundries.io/linux.git: https://source.foundries.io/linux.git
.. _source.foundries.io/lmp-kernel-cache.git: https://source.foundries.io/lmp-kernel-cache.git
.. _Yocto Project Linux Kernel Development Manual: https://www.yoctoproject.org/docs/2.5/kernel-dev/kernel-dev.html#kernel-dev-advanced
