.. _ref-pg-lmp-base:

``DISTRO lmp-base`` for Easy Kernel Image Access
---------------------------------------------------

The default :term:`distro` used by a Factory is ``lmp``.
It is designed to provide the secure and updatable environment needed for the operation of an end product.
However, this distro configuration is not ideal during the porting process.
Therefore we also support another distro configuration: ``lmp-base``.
This provides an easier development environment,
as it has a boot directory which includes the Linux Kernel image and the DTB file, and a read-writable :term:`rootfs`.
See detailed information on how lmp and lmp-base differ under :ref:`ref-linux-distro`.

In the following sections, the focus is on the boot flow (1) shown previous on :numref:`ref-pg-boot-flow-diagram`.
This boot flow is common on the i.MX8 and i.MX8M SoC families.
It is also common for i.MX6 and i.MX7 SoC families, however TF-A is not supported for these SoC families,
and is excluded from the boot flow.
