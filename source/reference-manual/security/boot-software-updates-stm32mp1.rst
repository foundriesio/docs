.. highlight:: sh

.. _ref-boot-software-updates-stm32mp1:

Boot Software Updates on STM32MP1
=================================

Boot Artifacts
--------------

STM32 TF-A BL2 Image
~~~~~~~~~~~~~~~~~~~~

The **TF-A BL2** image is the first boot image loaded by the application processor's
trusted ROM. It is in charge of loading the next-stage images (secure and
non-secure) and preliminary initialization of required peripherals:

- SoC clocks, DRAM
- Security IPs: memory firewalls, crypto engines
- Storage (MMC, QSPI etc).

The image is prepended with `STM32 header <https://wiki.st.com/stm32mpu/wiki/STM32_header_for_binary_files>`_.

It can also be signed using the STM32 Signing tool.

TF-A FIP Image
~~~~~~~~~~~~~~

The Trusted Firmware-A Firmware Image Package (TF-A FIP) the signed
FIP-image that contains U-Boot proper (``u-boot.bin``) and other firmware.
This file is verified by TF-A BL2 using RoT HASH (of the public key) in the BL2
device tree blob and public key, which are provided by the FIP image.
This artifact may be signed (on closed boards) as a part of CI and
can be included automatically in a boot software OTA package.

List of images inside FIP Image container:

-  U-boot-nodtb.bin (U-Boot proper binary)
-  U-boot.dtb (U-Boot device tree)
-  OP-TEE runtime (OP-TEE core, which provides PSCI and secure services)

If the CI signing key has been rotated since the last OTA,
update the BL2 verification data prior to trying to boot the
new FIP-image.

MMC Boot Image Layout
---------------------

The location of the boot image depends on what boot media is being used.
For eMMC, the initial boot images are flashed to a *0x0* offset of the boot
hw partitions.

When using a SD as boot media, boot images of different offsets are used within
the same HW partition. For additional details see :ref:`flash-layout-emmc`
and :ref:`wks-layout-sd`.

Update Procedure
----------------

Primary vs Secondary Boot Paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The STM32MP1 SoC supports booting from two copies of First Stage Boot Loaders:

-  First Stage Boot Loader Copy 1 (FSBL1)
-  First Stage Boot Loader Copy 2 (FSBL2)

Unfortunately, the SoC does not provide any mechanisms for a user to control in
runtime what FSBL copy to boot —only the SoC ROM can make this decision based
on image authentication/checksum results. As such, the setup for FSBL1
is treated as the primary boot path, with FSBL2 as a recovery path (secondary
boot path) in case the authentication/loading of FSBL1 fails.

Libaktualizr and Aktualizr-lite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Libaktualizr and Aktualizr-lite make decisions during the boot
phase. Those decisions are listed below, ordered as they appear in the source code:

1. aktualizr-lite makes the decision if boot firmware needs to be updated based
   on the contents of ``${ostree_root}/usr/lib/firmware/version.txt`,
   where ``ostree_root`` is root of newly deployed ostree sysroot.
   For example, ``bootfirmware_version=10``.

2. After parsing ``bootfirmware_version``, it compares version number with
   the existing one, which is obtained via **fiovb** or **ubootenv**.

3. If ``bootfirmware_version`` from ``version.txt`` is higher than existing
   one, Aktualizr-lite sets ``bootupgrade_available`` via **fiovb** or **ubootenv**.

4. Reboot is to be performed.

The U-Boot boot.cmd Script
~~~~~~~~~~~~~~~~~~~~~~~~~~

The following steps represent the boot path from U-Boot's perspective.

1. The update is done via the U-Boot **boot.cmd** (boot.scr) script.

2. The **boot.cmd** script checks if the primary path was booted.

3. In case ``upgrade_available`` is set, the script checks if a boot firmware
   upgrade is needed by looking into ``bootupgrade_available`` flag.
   If both are true, boot firmware images are then obtained from the newly
   deployed ostree sysroot and written to the primary boot path offsets.
   Afterwards, ``bootupgrade_primary_updated`` is set, and a regular reset signal is
   issued.

4. After the reboot, the SoC ROM tries to boot newly updated images from the primary
   boot path (FSBL1). If image verification fails, it will automatically fall
   back to FSBL2. When FSBL2 is booted, a rollback procedure will be issued,
   the previous version of FSBL1 will be restored. If FSBL1  *does* boot, but *bootcount*
   hits *bootlimit* (meaning the boot procedure has not finished
   successfully), the rollback procedure will be also issued.

5. After Linux is booted, Aktualizr-lite confirms a successful update by clearing
   the ``upgrade_available`` flag. At this point, new boot firmware images are
   already validated. An additional reboot is needed after this step.

6. After rebooting, U-Boot checks if ``bootupgrade_primary_updated`` is set and
   if ``upgrade_available`` is cleared. This means that Aktualizr-lite
   has confirmed a successful boot, and U-Boot clears
   ``bootupgrade_primary_updated`` flag. Otherwise the ``bootcount`` value is
   incremented.

Adding a new Board
------------------

meta-lmp
~~~~~~~~

.. _flash-layout-emmc:

Flash Layout File (eMMC Boot)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To deploy boot images to the destination board, **STM32CubeProg** is used.
This tool uses a special configuration file (with a **tsv** extension) that contains
the eMMC flash layout. For additional details, refer to the official
`documentation <https://wiki.st.com/stm32mpu/wiki/STM32CubeProgrammer_flashlayout>`_.

As **STM32CubeProg** does not support defining offsets
inside boot0/boot1 hw partitions, **TF-A BL2** and **FIP** are both combined
into one image in advance. This is done with correct padding between them,
so they are flashed to the correct offsets during STM32CubeProg execution:

::

    $ cp tf-a-stm32mp157c-ev1-emmc.stm32 combo-emmc-tfa-fip-stm32mp157c-ev1.bin
    $ dd if=fip-stm32mp157c-ev1-optee.bin combo-emmc-tfa-fip-stm32mp157c-ev1.bin bs=1024 seek=256 conv=notrunc

.. note::

    Concatenation is done automatically via the flashlayouts-stm32mp1.bb recipe.

Example of TSV file:

::

   #Opt	Id	Name		Type		IP	Offset		Binary
   -	0x01	fsbl-boot	Binary		none	0x0		tf-a-stm32mp157c-ev1-usb.stm32
   -	0x03	fip-boot	Binary		none	0x0		fip-stm32mp157c-ev1-optee.bin
   PD	0x04	fsbl1		Binary		mmc1	boot1		combo-emmc-tfa-fip-stm32mp157c-ev1.bin
   PD	0x05	fsbl2		Binary		mmc1	boot2		combo-emmc-tfa-fip-stm32mp157c-ev1.bin
   PED	0x06	u-boot-env	Binary		mmc1	0x00080000	none
   P	0x10	rootfs		System		mmc1	0x00100000	lmp-base-console-image-stm32mp15-eval.ext4

.. _wks-layout-sd:

WKS Layout (SD Boot)
^^^^^^^^^^^^^^^^^^^^

In a SD setup, two sets of FSBL images are stored, each with different offsets:

- FSBL1 *17KB*
- FSBL2 *256KB*

To support both images, the WKS file should be adjusted so that both copies
are placed at the correct offsets:

::

    part fsbl1 --source rawcopy --fstype=ext4 --fsoptions "noauto" --part-name=fsbl1 --sourceparams="file=tf-a-stm32mp157c-dk2-sdcard.stm32" --ondisk mmcblk --part-type 0x8301 --fixed-size 256K --align 17
    part fsbl2 --source rawcopy --fstype=ext4 --fsoptions "noauto" --part-name=fsbl2 --sourceparams="file=tf-a-stm32mp157c-dk2-sdcard.stm32" --ondisk mmcblk --part-type 0x8301 --fixed-size 256K
    part fip1 --source rawcopy --fstype=ext4 --fsoptions "noauto" --part-name=fip-a --sourceparams="file=fip-stm32mp157c-dk2-optee.bin" --ondisk mmcblk --part-type 0x8301 --fixed-size 4096K
    part fip2 --source rawcopy --fstype=ext4 --fsoptions "noauto" --part-name=fip-b --sourceparams="file=fip-stm32mp157c-dk2-optee.bin" --ondisk mmcblk --part-type 0x8301 --fixed-size 4096K
    part u-boot-env --source empty --part-name=uboot-env --ondisk mmcblk --part-type 0x8301 --fixed-size 16K --align 8192
    part / --source otaimage --ondisk mmcblk --fstype=ext4 --align 4096
    bootloader --ptable gpt

Testing FSBL Set and Auth Status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After applying the updates from previous steps, we should validate that
everything is in place. This consists of two steps:

- FSBL1 vs FSBL2 detection (primary or secondary path)
- Obtain board security state (results of FSBL authentication)

To test FSBP copy detection, check the ``boot\_part`` variable
using U-Boot shell:

::

    STM32MP> print boot_part
    boot_part=1


To check if the security status of your board is shown correctly, check
the ``boot\_auth`` variable:

::

    STM32MP> print boot_auth
    boot_auth=0

Possible values are:

- **0** - No authentication done
- **1** - Authentication done and failed
- **2** - Authentication done and success

boot.cmd
~~~~~~~~

Currently, LmP uses template-based generation for the final boot.cmd.
It's constructed from common boot files
(``./meta-lmp-base/recipes-bsp/u-boot/u-boot-ostree-scr-fit``),
which contains all SoC agnostic "DEFINEs" and common functionality, and
board-specific ``boot.cmd``, which includes the common scripts.

Example of board boot.cmd
(``./meta-lmp-bsp/recipes-bsp/u-boot/u-boot-ostree-scr-fit/stm32mp15-eval/boot.cmd``):

::

    setenv fdtfile stm32mp157c-ev1-scmi.dtb

    echo "Using ${fdtfile}"

    # Default boot type and device
    setenv bootlimit 3
    setenv devtype ${boot_device}
    setenv devnum ${boot_instance}
    setenv rootpart 2
    setenv fit_addr 0xc4400000
    setenv fdt_file_final ${fdtfile}
    setenv fdt_addr 0xc4000000
    setenv optee_ovl_addr 0xc4300000

    setenv loadaddr 0xc4400000
    setenv do_reboot "reset"
    setenv check_board_closed 'if test "${boot_auth}" = "2"; then setenv board_is_closed 1; else setenv board_is_closed; fi;'
    setenv check_secondary_boot 'if test "${boot_part}" = "2"; then setenv fiovb.is_secondary_boot 1; else setenv fiovb.is_secondary_boot 0; fi;'

    # All values are provided in blocks (512 bytes each)
    setenv bootloader 0x0
    setenv bootloader2 0x200
    setenv bootloader_size 0x1000
    setenv bootloader_s ${bootloader}
    setenv bootloader2_s ${bootloader2}
    setenv bootloader_image "tf-a-stm32mp157c-ev1-emmc.stm32"
    setenv bootloader_s_image ${bootloader_image}
    setenv bootloader2_image "fip-stm32mp157c-ev1-optee.bin"
    setenv bootloader2_s_image ${bootloader2_image}

    setenv update_image_boot0 '\
    	echo "${fio_msg} writing ${image_path} ..."; \
    	run set_blkcnt && \
    	mmc dev ${devnum} && \
    	mmc partconf ${devnum} 1 1 1 && \
    	mmc write ${loadaddr} ${start_blk} ${blkcnt} && \
    	mmc partconf ${devnum} 1 1 0 \
    '

    setenv backup_primary_image '\
    	echo "${fio_msg} backing up primary boot image set ..."; \
    	mmc dev ${devnum} && \
    	mmc partconf ${devnum} 1 1 1 && \
    	mmc read ${loadaddr} ${bootloader} ${bootloader_size} && \
    	mmc partconf ${devnum} 1 1 0 && \
    	mmc dev ${devnum} && \
    	mmc partconf ${devnum} 1 1 2 && \
    	mmc write ${loadaddr} ${bootloader} ${bootloader_size} && \
    	mmc partconf ${devnum} 1 1 0 \
    '

    setenv restore_primary_image '\
    	echo "${fio_msg} restore primary boot image set ..." ; \
    	mmc dev ${devnum} && \
    	mmc partconf ${devnum} 1 1 2 && \
    	mmc read ${loadaddr} ${bootloader} ${bootloader_size} && \
    	mmc partconf ${devnum} 1 1 0 && \
    	mmc dev ${devnum} && \
    	mmc partconf ${devnum} 1 1 1 && \
    	mmc write ${loadaddr} ${bootloader} ${bootloader_size} && \
    	mmc partconf ${devnum} 1 1 0 \
    '

    setenv update_primary_image1 'setenv image_path "${ostree_root}/usr/lib/firmware/${bootloader_s_image}"; setenv start_blk "${bootloader_s}";  run load_image; run update_image_boot0'
    setenv update_primary_image2 'setenv image_path "${ostree_root}/usr/lib/firmware/${bootloader2_s_image}"; setenv start_blk "${bootloader2_s}";  run load_image; run update_image_boot0'

    setenv update_primary_image 'run update_primary_image1 && run update_primary_image2'

    @@INCLUDE_COMMON_ALTERNATIVE@@


Sysroot and Signed Boot Artifacts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Boot artifacts (TF-A BL2 and FIP) are automatically deployed
to sysroot during build time. On closed boards however, where the initial boot
image has to be signed in advance by a subscriber private key, there is a way to
add a signed binary instead of relying on the automatic inclusion of unsigned boot artifacts.

To do that, just add ``lmp-boot-firmware.bbappend`` to your *meta-subscriber-overrides*
layer, adding the path to the signed binary and the signed binary itself.

Then define boot firmware version number by setting ``LMP_BOOT_FIRMWARE_VERSION``
global variable in your ``lmp-factory-custom.inc``. Boot firmware version
information will be automatically added to `${osroot}/usr/lib/firmware/version.txt`
file and U-Boot Device Tree Blob.

Versioning convention is up to user, the only requirement is that the version
string should be unique and there should not be duplicates.

Example:
::

    diff --git a/recipes-bsp/lmp-boot-firmware/lmp-boot-firmware.bbappend b/recipes-bsp/lmp-boot-firmware/lmp-boot-firmware.bbappend
    new file mode 100644
    index 0000000..6c11380
    --- /dev/null
    +++ b/recipes-bsp/lmp-boot-firmware/lmp-boot-firmware.bbappend
    @@ -0,0 +1,7 @@
    +FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"
    +
    +SRC_URI = " \
    +       file://tf-a-stm32mp157c-ev1-mmc.stm32 \
    +"
    diff --git a/recipes-bsp/lmp-boot-firmware/lmp-boot-firmware/tf-a-stm32mp157c-ev1-mmc.stm32 b/recipes-bsp/lmp-boot-firmware/lmp-boot-firmware/tf-a-stm32mp157c-ev1-mmc.stm32
    new file mode 100644
    index 0000000..50f5013
    Binary files /dev/null and b/recipes-bsp/lmp-boot-firmware/lmp-boot-firmware/tf-a-stm32mp157c-ev1-mmc.stm32 differ
    --- a/conf/machine/include/lmp-factory-custom.inc
    +++ b/conf/machine/include/lmp-factory-custom.inc
    @@ -22,4 +22,4 @@ UEFI_SIGN_KEYDIR = "${TOPDIR}/conf/factory-keys/uefi"
     # TF-A Trusted Boot
     TF_A_SIGN_KEY_PATH = "${TOPDIR}/conf/factory-keys/tf-a/privkey_ec_prime256v1.pem"

    +LMP_BOOT_FIRMWARE_VERSION:stm32mp15-eval = "3"

.. note::

    As ``LMP_BOOT_FIRMWARE_VERSION`` is now a preferable way to set boot firmware version, defining ``PV`` in ``lmp-boot-firmware.bbappend``
    is deprecated and should not be used. To switch to a new approach just remove ``PV = "<version>"`` line from
    ``lmp-boot-firmware.bbappend`` and define ``LMP_BOOT_FIRMWARE_VERSION`` with appropriate version value as shown above in the example.

.. seealso::
   * :ref:`ref-secure-boot-stm32mp1`
