.. _lmp-appendix-kernel:

Appendix: Linux microPlatform Kernel
====================================

A common and unified Linux Kernel source tree is provided and used by
Linux microPlatform.

**Subscribers**:

The latest continuous release is available to Linux microPlatform
subscribers from source.foundries.io, and available at
https://source.foundries.io/linux.git.

**Public**:

A public release will be made available at a later date.

.. todo:: add link to public LMP kernel on OSF github when available.

The Linux Kernel recipe can be found in the :ref:`Meta-OSF layer
<lmp-appendix-meta-osf>`, under the ``meta-osf/recipes-kernel/linux``
directory (linux-osf). You can find the common Linux distro config at
``meta-osf/recipes-kernel/linux/linux-osf/distro.config``, which
provides the base configs required by systemd, the Docker runtime, and
drivers for additional WiFi / Bluetooth adapters.
