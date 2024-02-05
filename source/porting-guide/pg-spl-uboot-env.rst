.. _ref-pg-uboot-env:

U-Boot Environment and Boot Script
==================================

The last step to configure U-Boot in LmP is to provide the boot environment (for ``lmp-base``) and the boot command.
You can start by using the reference board support, adjusting the files accordingly for the target board.

For the ``lmp-base`` distro, provide the boot environment input file ``uEnv.txt.in``, which sets the needed variables for booting:

``u-boot-base-scr/imx8mmevk/uEnv.txt.in``:

.. prompt:: text

    devnum=2
    devtype=mmc
    bootcmd_args=setenv bootargs console=tty1 console=${console} root=/dev/mmcblk2p2 rootfstype=ext4 rootwait rw
    bootcmd_dtb=fatload ${devtype} ${devnum}:1 ${fdt_addr} ${fdt_file}
    bootcmd_load_k=fatload ${devtype} ${devnum}:1 ${loadaddr} ${image}
    bootcmd_run=booti ${loadaddr} - ${fdt_addr}
    bootcmd=run bootcmd_args; run bootcmd_dtb; run bootcmd_load_k; run bootcmd_run

You will need to define the ``devnum`` and ``bootcmd_args`` root parameters to meet the eMMC index on your board.
Other board specific variables can be set in this file if needed, like ``fdt_file`` or console configurations.

After ``uEnv.txt.in`` is in place, provide ``boot.cmd``.
This loads this environment and boots to kernel:

``u-boot-base-scr/imx8mmevk/boot.cmd``:

.. prompt:: text

    fatload mmc ${emmc_dev}:1 ${loadaddr} /uEnv.txt
    env import -t ${loadaddr} ${filesize}
    run bootcmd

For the ``lmp-base`` distro, these files live in ``u-boot-base-scr``:

.. prompt:: text

    recipes-bsp/u-boot/
    ├── u-boot-base-scr
    │ └── <board>
    │     ├── boot.cmd
    │     └── uEnv.txt.in
    └── u-boot-base-scr.bbappend

Also for the ``lmp`` distro, the only file that needs to be provided is ``boot.cmd``.
Note that in this case, it handles both the environment and the boot command:

``u-boot-ostree-scr-fit/imx8mmevk/boot.cmd``:

.. prompt:: text

    echo "Using freescale_${fdt_file}"

    # Default boot type and device
    setenv bootlimit 3
    setenv devtype mmc
    setenv devnum 2
    setenv bootpart 1
    setenv rootpart 2

    # Boot image files
    setenv fdt_file_final freescale_${fdt_file}
    setenv fit_addr ${initrd_addr}

    # Boot firmware updates
    setenv bootloader 42
    setenv bootloader2 300
    setenv bootloader_s 1042
    setenv bootloader2_s 1300
    setenv bootloader_image "imx-boot"
    setenv bootloader_s_image ${bootloader_image}
    setenv bootloader2_image "u-boot.itb"
    setenv bootloader2_s_image ${bootloader2_image}
    setenv uboot_hwpart 1

    @@INCLUDE_COMMON@@

You will need to define ``devnum`` as expected by the board.
Make sure the ``initrd_addr`` is set in U-Boot correctly.
Otherwise you may need to set the ``initrd_addr`` (as well as any other missing addresses) in this file.


.. note::

    If porting to a new SoC not supported in LmP,
    the boot firmware offsets also need to be calculated and adjusted as described under :ref:`ref-sec-tfa-optee`.

The boot.cmd for the ``lmp`` distro lives in:

.. prompt:: text

    recipes-bsp/u-boot/
    ├── u-boot-ostree-scr-fit
    │   └── <board>
    │       └── boot.cmd
    └── u-boot-ostree-scr-fit.bbappend

After providing these files, LmP has all the needed configuration to boot U-Boot and get to the kernel.
