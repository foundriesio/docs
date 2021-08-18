.. _ref-pg-machine-conf:

Machine configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^^

The machine configuration file is where the hardware is described in
terms of variables such as:

.. Glossary::

   SERIAL_CONSOLES
     Describe the serial console used on this machine

   MACHINE_EXTRA_RRECOMMENDS
     List the packages recommended during run time for this machine

   UBOOT_DTB_NAME
     Set the DTB file name used by U-Boot

   UBOOT_CONFIG
     Describe the configuration used for U-Boot on this machine

   MACHINE_FEATURES
     List the machine features for this machine used to configure the
     Yocto Project packages and tools

   IMXBOOT_TARGETS
     State the target name to be used with imx-boot, a
     critical package to the bring up of i.MX8 SoC family boards

The machine configuration file from a reference board can guide as a
reminder on what variable set is important to define.

It is possible that the porting task targets a new machine configuration file.
In this case, any machine related configuration should be placed in the new
machine configuration file.