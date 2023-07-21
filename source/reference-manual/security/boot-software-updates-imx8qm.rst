.. highlight:: sh

.. _ref-boot-software-updates-imx8qm:

Boot Software Updates on iMX8QM
===============================

Boot artifacts
--------------

imx-boot image
~~~~~~~~~~~~~~

**imx-boot** image is the first boot image container set by CSU ROM.
**imx-boot** image consists of two containers:

-  SECO container for SECO FW
-  SCU container for SCU FW, and optinal AP IPL (Cortex A processing domain),
   CM4 FW and DDR init images

By default U-Boot SPL image is used as the main AP IPL image.
SECO container is always signed and provided by NXP, and SCU container can
be signed by OEM vendor/customer.

Here is an example of typical boot image container set layout:

::

     ---------------------------
    |    1st Container Header   |
     ---------------------------
    |    1st Signature Block    |
     ---------------------------
    | Padding for 1KB alignment |
     ---------------------------
    |    2nd Container Header   |
     ---------------------------
    |    2nd Signature Block    |
     ---------------------------
    |          SECO FW          |
     ---------------------------
    |    SCU FW with DDR init   |
     ---------------------------
    |          CM4 Image        |
     ---------------------------
    |    Cortex-A FW (AP IPL)   |
     ---------------------------

U-Boot FIT image
~~~~~~~~~~~~~~~~

U-boot FIT-image is a generic name for the signed FIT-image that
contains U-Boot proper (u-boot.bin) and a host of other firmware.
This file is verified by SPL via a public key stored in SPL’s dtb.
This artifact may be signed (on closed boards) as a part of CI and
can be included automatically in a boot software OTA package.

-  U-boot-nodtb.bin
-  U-boot.dtb
-  OP-TEE
-  Arm Trusted Firmware (ARMv8)

If the CI signing key has been rotated since the last OTA, then we need
to also update the SPL.dtb verification data prior to trying to boot the
new U-Boot FIT-image.


MMC boot image layout
---------------------

From *5.8.2.2.1 High Level eMMC Boot Flow Note* (iMX8QM Reference manual),
for the eMMC boot scenarios where the images are located in the boot
partition the boot image set selection is done based on
**BOOT_PARTITION_ENABLE** eMMC **ECSD** register values, which means that
secondary boot image set should be flashed to **boot1** hw partition to the
same offset (0x0) as the primary one.

Update procedure
----------------

Primary vs Secondary boot paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

iMX8QM SoC supports two different container sets of boot images:

-  Primary Boot Container set (Set0)
-  Secondary Boot Container set (Set1) (optional)

SCU ROM reads both Image Container Set0’s and Set1’s headers, then select
the container set with the newer SW version for Primary boot path and the
container set with the older SW vesion for Secondary boot path. In case
SW versions are equal, SCU ROM picks Set0.

Unfortunately SoC doesn't provide any mechanisms for user to control in
runtimewhat container set to boot, like setting **PERSIST\_SECONDARY\_BOOT**
bit  **SRC\_GPR10**, so in our setup we don't rely on different SW versions
of Image Container Sets, and use Set0 for as Primary boot path,
and Set1 as a recovery path (Secondary boot path).

register in i.MX8M.

libaktualizr and aktualizr-lite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. aktualizr-lite makes decision if boot firmware needs to be updated based
   on the contents of **${ostree\_root}/usr/lib/firmware/version.txt**,
   where ostree\_root is root of newly deployed ostree sysroot. Example
   of contents: **bootfirmware\_version=10**
2. After parsing bootfirmware\_version, it compares version number with
   the existing one, which is obtained via **fiovb** or **ubootenv**.
3. If bootfirmware\_version from version.txt is higher than existing
   one, aktualizr-lite sets **bootupgrade\_available** via **fiovb** or
   **ubootenv**.
4. Reboot should be performed.

U-Boot boot.cmd script
~~~~~~~~~~~~~~~~~~~~~~

.. figure:: boot-software-updates/upgrade-flow-imx8qm.png
   :alt: Boot firmware upgrade flow for iMX8QM

   Boot firmware upgrade flow for iMX8QM

1. Actual update is done via U-Boot **boot.cmd** (boot.scr) script.
2. **boot.cmd** script checks if primary path is booted.
3. In case **upgrade\_available** is set the check if boot firmware
   upgrade is needed is done by looking into **bootupgrade\_available** flag.
   If both are true, boot firmware images are obtained from newly
   deployed ostree sysroot and then written to the primary boot path offsets.
   After that **bootupgrade\_primary\_updated** is set, and regular reset is
   issued.
4. After reboot SCU ROM tries to boot newly updated images from the primary
   boot path (Set0). If image verification fails, it automatically will fall
   back to Set1. If Set1 is booted (which means that verification of Set0
   failed), rollback procedure will be issued, and previous version of
   Set0 will be restored. If on the conntrary Set0 is booted, but bootcount
   hits bootlimit (that means that boot procedure haven't finished
   succesfully), rollback procedure will be also issued.
5. After Linux is booted aktualizr-lite confirms successful update by clearing
   **upgrade\_available** flag. At this point new boot firmware images are
   already validated. Additional reboot is needed after this step.
6. After reboot U-Boot checks if **bootupgrade\_primary\_updated** is set and
   **upgrade\_available** is cleared. This means that aktualizr-lite
   has confirmed succesful boot, and U-Boot clears
   **bootupgrade\_primary\_updated** flag. Otherwise **bootcount** value is
   incremented.


Add new board
-------------

meta-lmp
~~~~~~~~

mfgtool scripts
^^^^^^^^^^^^^^^

To deploy boot images to the destination board mfgtools package is used.
It uses special configuration file with uuu extensions, that contains
all needed instructions for correct deployment of boot images. Current
uuu files don't support flashing images for secondary boot path, so
appropriate adjustments should be made, adding secondary imx-boot
and U-Boot FIT deployment steps:

::

    +FB: flash bootloader2 ../u-boot-@@MACHINE@@.itb
    +FB: flash bootloader2_s ../u-boot-@@MACHINE@@.itb

So the final uuu script looks like:

::

    uuu_version 1.3.102

    SDPS: boot -f imx-boot-mfgtool
    CFG: FB: -vid 0x0525 -pid 0x4000
    CFG: FB: -vid 0x0525 -pid 0x4025
    CFG: FB: -vid 0x0525 -pid 0x402F
    CFG: FB: -vid 0x0525 -pid 0x4030
    CFG: FB: -vid 0x0525 -pid 0x4031

    SDPU: delay 1000
    SDPU: write -f imx-boot-mfgtool -offset 0x57c00
    SDPU: jump

    # These commands will be run when use SPL and will be skipped if no spl
    # if (SPL support SDPV)
    # {
    SDPV: delay 1000
    SDPV: write -f u-boot-mfgtool.itb
    SDPV: jump
    # }

    FB: ucmd setenv fastboot_dev mmc
    FB: ucmd setenv mmcdev 0
    FB: ucmd mmc dev ${mmcdev} 1; mmc erase 0 0x3FFE
    FB: flash -raw2sparse all ../@@MFGTOOL_FLASH_IMAGE@@-@@MACHINE@@.wic
    FB: flash bootloader ../imx-boot-@@MACHINE@@
    FB: flash bootloader_s ../imx-boot-@@MACHINE@@
    FB: flash bootloader2 ../u-boot-@@MACHINE@@.itb
    FB: flash bootloader2_s ../u-boot-@@MACHINE@@.itb
    FB: ucmd mmc partconf 0 0 1 0
    FB: done


lmp.cfg files
^^^^^^^^^^^^^

To enable support for flashing/booting secondary boot images, just
adjust regular **lmp.cfg** and the one for mfgtools for your board enabling
support of secondary boot path. These config options should be added to
regular **lmp.cfg**:

::

    CONFIG_CMD_SECONDARY_BOOT=y
    CONFIG_SECONDARY_BOOT_SECTOR_OFFSET=0x0
    CONFIG_SECONDARY_BOOT_RUNTIME_DETECTION=y

And to mfgtool **lmp.cfg**:

::

    CONFIG_FSL_FASTBOOT_BOOTLOADER_SECONDARY=y
    CONFIG_SECONDARY_BOOT_SECTOR_OFFSET=0x0

As secondary boot path is mainly used for boot firmware update image
validation, sometimes in exceptional cases it behaves incorrectly,
causing hangs etc. To cover such cases watchdog support has to be
enabled in SPL by adding these config options to **lmp.cfg** of your
board:

::

    CONFIG_IMX_WATCHDOG=y
    CONFIG_SPL_HW_WATCHDOG=y
    # CONFIG_SPL_WDT is not set
    CONFIG_SPL_WATCHDOG_SUPPORT=y


Pre-load boot.cmd by SPL
^^^^^^^^^^^^^^^^^^^^^^^^

As boot.cmd script depends on U-Boot cmds for booting Linux, it should be
aligned with U-Boot version. By default in regular setups without boot firmware
update support boot.cmd is stored in first FAT partition in eMMC/SD.
So to get boot.cmd updates together with other boot software images,
it should be moved from FAT partition to U-Boot FIT image. To do that edit
**lmp-machine-custom.inc** adding this line for your board (imx8qmevk as
an example):

::

    BOOTSCR_LOAD_ADDR_imx8qmmek = "0x44800000"

This change will include Linux **boot.cmd** into U-Boot FIT image
alongside with TF-A/OP-TEE/U-Boot proper/U-Boot dtb images. When SPL
parses U-Boot FIT image (u-boot.itb) it will pre-load **boot.itb**
(compiled and wrapped **boot.cmd**) to the address specified in
**BOOTSCR\_LOAD\_ADDR** variable.

To let U-Boot know where to take boot script from, you should also
adjust **CONFIG\_BOOTCOMMAND** param in your U-Boot **lmp.cfg** of your
board.

::

    CONFIG_BOOTCOMMAND="setenv verify 1; source 0x44800000; reset"


Test basic API
~~~~~~~~~~~~~~

After applying all updates from previous steps, we should validate that
everything is in place. Basically this consists of two basic steps:

- Boot container set detection (primary or secondary)
- Obtain board security state (open/closed states)

So to test Boot container set detection use this U-Boot command
**imx\_secondary\_boot**.

Example of test:

::

    u-boot=> imx_secondary_boot
    Secondary boot bit = 0

To check if the security status of your board is detected correctly, use
**imx\_is\_closed** command:

::

    u-boot=> imx_is_closed
    Board is in open state


boot.cmd
~~~~~~~~

Currently LmP uses template-based way of generation of final boot.cmd.
It's constructed from common boot files
(``./meta-lmp-base/recipes-bsp/u-boot/u-boot-ostree-scr-fit``),
which contains all SoC agnostic DEFINEs and common functionality, and board
specific boot.cmd, which includes the common scripts.

Example of board boot.cmd
(``./meta-lmp-bsp/recipes-bsp/u-boot/u-boot-ostree-scr-fit/imx8qm-mek/boot.cmd``):

::

    setenv fdt_file imx8qm-mek.dtb
    echo "Using freescale_${fdt_file}"

    # Default boot type and device
    setenv bootlimit 3
    setenv devtype mmc
    setenv devnum 0
    setenv bootpart 1
    setenv rootpart 2
    setenv hdmi_image hdmitxfw.bin
    setenv m4_0_image core0_m4_image.bin
    setenv m4_1_image core1_m4_image.bin
    setenv ramdisk_addr_r 0x8a000000
    # enable relocation of ramdisk
    setenv initrd_high

    # Boot image files
    setenv fit_addr ${ramdisk_addr_r}
    setenv fdt_file_final freescale_${fdt_file}

    setenv bootcmd_boot_hdmi 'hdp load ${loadaddr}'
    setenv bootcmd_boot_m4_0 'dcache flush; bootaux ${loadaddr} 0'
    setenv bootcmd_boot_m4_1 'dcache flush; bootaux ${loadaddr} 1'
    setenv bootcmd_load_hdmi 'if imxtract ${ramdisk_addr_r}#conf@@FIT_NODE_SEPARATOR@@freescale_${fdt_file} loadable@@FIT_NODE_SEPARATOR@@${hdmi_image} ${loadaddr}; then run bootcmd_boot_hdmi; fi'
    setenv bootcmd_load_m4_0 'if imxtract ${ramdisk_addr_r}#conf@@FIT_NODE_SEPARATOR@@freescale_${fdt_file} loadable@@FIT_NODE_SEPARATOR@@${m4_0_image} ${loadaddr}; then run bootcmd_boot_m4_0; fi;'
    setenv bootcmd_load_m4_1 'if imxtract ${ramdisk_addr_r}#conf@@FIT_NODE_SEPARATOR@@freescale_${fdt_file} loadable@@FIT_NODE_SEPARATOR@@${m4_1_image} ${loadaddr}; then run bootcmd_boot_m4_1; fi;'
    setenv bootcmd_load_fw 'run bootcmd_load_hdmi; run bootcmd_load_m4_0; run bootcmd_load_m4_1;'

    # Boot firmware updates

    # Offsets are in blocks (512 bytes each)
    setenv bootloader 0x0
    setenv bootloader2 0x400
    setenv bootloader_s ${bootloader}
    setenv bootloader2_s ${bootloader2}
    setenv bootloader_image "imx-boot"
    setenv bootloader_s_image ${bootloader_image}
    setenv bootloader2_image "u-boot.itb"
    setenv bootloader2_s_image ${bootloader2_image}

    setenv update_image_boot0 'echo "${fio_msg} writing ${image_path} ..."; run set_blkcnt && mmc dev ${devnum} 1 && mmc write ${loadaddr} ${start_blk} ${blkcnt}'

    setenv backup_primary_image 'echo "${fio_msg} backing up primary boot image set ..."; mmc dev ${devnum} 1 && mmc read ${loadaddr} 0x0 0x3FFE && mmc dev ${devnum} 2 && mmc write ${loadaddr} 0x0 0x3FFE'
    setenv restore_primary_image 'echo "${fio_msg} restore primary boot image set ..."; mmc dev ${devnum} 2 && mmc read ${loadaddr} 0x0 0x3FFE && mmc dev ${devnum} 1 && mmc write ${loadaddr} 0x0 0x3FFE'

    setenv update_primary_image1 'if test "${ostree_deploy_usr}" = "1"; then setenv image_path "${bootdir}/${bootloader_s_image}"; else setenv image_path "${ostree_root}/usr/lib/firmware/${bootloader_s_image}"; fi; setenv start_blk "${bootloader_s}";  run load_image; run update_image_boot0'
    setenv update_primary_image2 'if test "${ostree_deploy_usr}" = "1"; then setenv image_path "${bootdir}/${bootloader2_s_image}"; else setenv image_path "${ostree_root}/usr/lib/firmware/${bootloader2_s_image}"; fi; setenv start_blk "${bootloader2_s}";  run load_image; run update_image_boot0'

    setenv update_primary_image 'run update_primary_image1; run update_primary_image2'

    setenv do_reboot "reboot"

    @@INCLUDE_COMMON_IMX@@
    @@INCLUDE_COMMON_ALTERNATIVE@@


sysroot and signed boot artifacts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All boot artifacts (imx-boot and U-Boot FIT) are automatically deployed
to sysroot during build time, however on closed boards, where initial boot
image has to be signed in advance by a subscriber private key, there is way to
add signed binary instead of automatic inclusion of unsigned boot artifacts.

To do that, just add ``lmp-boot-firmware.bbappend`` to your *meta-subscriber-overrides*
layer, adding the path to the signed binary and the signed binary itself.

Then define boot firmware version number by setting ``LMP_BOOT_FIRMWARE_VERSION``
global variable in your ``lmp-factory-custom.inc``. Boot firmware version
information will be automatically added to `${osroot}/usr/lib/firmware/version.txt`
file and U-Boot Device Tree Blob.

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
    +       file://imx-boot \
    +"
    diff --git a/recipes-bsp/lmp-boot-firmware/lmp-boot-firmware/imx-boot b/recipes-bsp/lmp-boot-firmware/lmp-boot-firmware/imx-boot
    new file mode 100644
    index 0000000..50f5013
    Binary files /dev/null and b/recipes-bsp/lmp-boot-firmware/lmp-boot-firmware/imx-boot differ
    --- a/conf/machine/include/lmp-factory-custom.inc
    +++ b/conf/machine/include/lmp-factory-custom.inc
    @@ -22,4 +22,4 @@ UEFI_SIGN_KEYDIR = "${TOPDIR}/conf/factory-keys/uefi"
     # TF-A Trusted Boot
     TF_A_SIGN_KEY_PATH = "${TOPDIR}/conf/factory-keys/tf-a/privkey_ec_prime256v1.pem"

    +LMP_BOOT_FIRMWARE_VERSION:imx8qm-mek = "3"

.. note::

    As ``LMP_BOOT_FIRMWARE_VERSION`` is now a preferable way to set boot firmware version, defining ``PV`` in ``lmp-boot-firmware.bbappend``
    is deprecated and should not be used. To switch to a new approach just remove ``PV = "<version>"`` line from
    ``lmp-boot-firmware.bbappend`` and define ``LMP_BOOT_FIRMWARE_VERSION`` with appropriate version value as shown above in the example.

.. seealso::
   * :ref:`ref-secure-boot-imx-ahab`
