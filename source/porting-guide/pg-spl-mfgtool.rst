.. _ref-pg-spl-mfgtool:

MFGTool (for i.MX boards)
=========================

MFGTool is the NXP tool to deploy images to an i.MX-based board. LmP
provides two scripts to deploy the build artifacts using this tool:

-  ``bootloader.uuu``: used to deploy SPL and U-Boot FIT image (u-boot.itb)
-  ``full_image.uuu``: used to deploy the entire image, from SPL to rootfs

This support can be extended to support other features, such as fusing
and closing a board for secure boot. (This case is not covered in this
document at the moment.)

The ``mfgtool-files`` package is built by the CI when the ``mfg_tools`` node is
included in ``factory-config.yml`` :ref:`ref-factory-definition`
or locally when ``DISTRO=lmp-mfgtool`` is set.

To enable a custom ``mfgtool-files`` package, the user must provide the
following configuration:

-  U-Boot: The user needs to provide a configuration file (``lmp.cfg``) to
   be used for the ``mfgtool-files`` U-Boot build (``u-boot-fio-mfgtool``). This
   is similar to the configuration file used by ``DISTRO=lmp``, but should
   include SDP, USB and fastboot support.

-  OP-TEE: Same for the standard ``u-boot-fio support``, the user needs to
   provide machine-specific configuration to OP-TEE for the
   ``mfgtool-files`` building (``optee-os-fio-mfgtool``), such as OP-TEE machine
   name, UART address, overlay address.

-  ``mfgtool-files``: ``bootloader.uuu.in`` and ``full_image.uuu.in``: Input files to
   generate the MFGTool scripts. The user can provide the same files as
   the reference board support in LmP.

.. prompt:: text

	├── recipes-bsp
	│   └── u-boot
	│       ├── u-boot-fio-mfgtool
	│       │   └── <board>
	│       │       └── lmp.cfg
	│       └── u-boot-fio-mfgtool_%.bbappend
	├── recipes-security
	│   └── optee
	│       └── optee-os-fio-mfgtool_3.10.0.bbappend
	└── recipes-support
	    └── mfgtool-files
		├── mfgtool-files
		│   └── <board>
		│       ├── bootloader.uuu.in
		│       └── full_image.uuu.in
		└── mfgtool-files_%.bbappend
