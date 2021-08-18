.. _ref-pg-spl-flow-index:

Checklist
=========

The checklist goal is to make sure everything needed is in place:

1.  Find the similar reference board (:ref:`ref-pg-reference-board`)
2.  Change distro from ``lmp`` to ``lmp-base`` (:ref:`ref-pg-lmp-base`)
3.  Create the machine configuration file (:ref:`ref-pg-machine-conf`)
4.  Port u-boot (:ref:`ref-pg-spl-uboot`)

    a. Enable SPL

5.  Enable MFGTool (:ref:`ref-pg-spl-mfgtool`)
6.  Port OP-TEE (:ref:`ref-pg-spl-optee`)
7.  Configure TF-A (:ref:`ref-pg-spl-uboot`)
8.  Test the first boot, check the images being loaded
9.  Port the Linux Kernel (:ref:`ref-pg-spl-kernel`)
10. Port the Device tree (:ref:`ref-pg-spl-kernel`)
11. Port the Linux Kernel BSP configuration fragment (:ref:`ref-pg-spl-kernel`)
12. When the port is done, go back to ``lmp`` distro and start to configure the platform as needed
