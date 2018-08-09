.. _ref-linux-kernel:

Linux microPlatform Kernel
==========================

A common and unified Linux Kernel source tree is provided and used by
the Linux microPlatform. The latest continuous release is available to
subscribers at `source.foundries.io/linux.git`_.

The Linux Kernel recipe can be found in the :ref:`Meta-LMP layer
<ref-linux-layers-meta-lmp>`, under the ``meta-lmp/recipes-kernel/linux``
directory. You can find the common Linux distro config at
``meta-lmp/recipes-kernel/linux/linux-lmp/distro.cfg``, which
provides the base configs required by systemd, the Docker runtime, and
drivers for additional WiFi / Bluetooth adapters.

.. _source.foundries.io/linux.git: https://source.foundries.io/linux.git
