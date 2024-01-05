.. _howto-linux-nfs-boot:

LmP root file-system over NFS
=============================

Introduction
------------
LmP uses OSTree to pack the device root filesystem. In early boot,
initramfs manipulates OSTree storage to layout the target root
filesystem for Linux kernel mounting.

Yocto enables modular initramfs configuration, allowing selective
support for udev, rootfs, ostree, or network filesystem in the
ramdisk. Adding NFS and OSTree ramdisk support permits switch root
scripts to prepare shared network filesystem for mounting on the target.

Generally, NFS booting any LmP system requires configuring NFS support
in the ramdisk, along with a TFTP server and an NFS server.

NFS use case: validation of eMMC card
-------------------------------------
During product development, validating the eMMC card for system boot
might be needed. The Linux kernel eMMC subsystem offers an extensive set
of tests. Unfortunately, many tests require unbinding the eMMC card from
the kernel. In such cases, you can boot the system over NFS, unbind the
eMMC, and run the tests. Here's an example executing eMMC tuning tests:

.. prompt:: text

      $ echo 'mmc0:0001' >  /sys/bus/mmc/drivers/mmcblk/unbind
      $ echo 'mmc0:0001' > /sys/bus/mmc/drivers/mmc_test/bind
      $ echo 52 > /sys/kernel/debug/mmc0/mmc0\:0001/test


Enabling NFS support on initramfs
---------------------------------
To configure the ramdisk for NFS boot using Yocto requires enabling the
``initramfs-module-nfsrootfs`` package.

A reference snippet can be seen below:

.. prompt:: text

     diff --git a/meta-lmp-base/recipes-core/images/initramfs-ostree-lmp-image.bb b/meta-lmp-base/recipes-core/images/initramfs-ostree-lmp-image.bb
     index f4f2e505..99b801ca 100644
     --- a/meta-lmp-base/recipes-core/images/initramfs-ostree-lmp-image.bb
     +++ b/meta-lmp-base/recipes-core/images/initramfs-ostree-lmp-image.bb
     @@ -4,6 +4,7 @@ PACKAGE_INSTALL = "initramfs-framework-base \
     initramfs-module-udev \
     initramfs-module-rootfs \
     initramfs-module-ostree \
     + initramfs-module-nfsrootfs \
     initramfs-module-ostree-factory-reset \
     ${VIRTUAL-RUNTIME_base-utils} \
     ${@bb.utils.contains('DISTRO_FEATURES', 'ima', 'initramfs-framework-ima', '', d)} \

Then rebuild LmP as usual.

Access to the LmP released WIC file, the kernel Image for booting, the
board's device tree blob, and the generated ramdisk is necessary for the
following sections.

Preparing the NFS server
------------------------
Copy the WIC image created during the build step to the NFS shared
folder and mount it for simplicity. Alternatively, you can extract and
copy all its contents based on your use case.

To mount the WIC, use the fdisk utility to determine the start sector
and length of the rootfs image in the file (i.e., the number of
sectors).

.. prompt:: text

    $ fdisk -l lmp-base-console-image-${platform-name}.wic

Then create the ``rootfs`` directory and mount it:

.. prompt:: text

    #!/bin/bash
    mkdir rootfs
    read -p "Enter linux start sector: " lsector
    read -p "Enter linux number of sectors: " lnsectors
    let "offset=`expr ${lsector}*512`"
    let "sizelimit=`expr ${lnsectors}*512`"
    mount -o loop,offset=$offset,sizelimit=$sizelimit -tauto lmp-base-console-image.wic rootfs/


It is this ``rootfs`` mount-point - which shall contain ``boot/`` and ``ostree/``
directories - what you should export via NFS.

Inspecting the ``ostree/`` directory and in this particular case, you should
expect something as follows:

.. prompt:: text

    ostree/boot.1/lmp/180c0adc612a144a262f15e6c124cc3ac22260b7b2897832a1228da2d3e359a5/0


Preparing the TFTP server
-------------------------
LmP employs U-boot as both the primary and secondary bootloader on ARM
platforms. The secondary bootloader's role is to boot the Linux kernel.

U-boot can be configured to fetch the Linux image, device tree, and
ramdisk from a TFTP server. For successful booting, the ramdisk must be
in a format that U-boot can parse.

During LmP building, the CI service deploys all the build artifacts. The
kernel and device tree are published in a FIT file (Flattened Image
Tree), while the initial RAM file system is deployed as a
gzip-compressed cpio archive.

To extract the kernel and device tree blob, start by listing the
contents of the FIT file.

The file should be named  ``fitImage-${platform-name}.bin``

.. prompt:: text

    $ dumpimage -l fitImage-uz3cg-dwg-sec.bin
    FIT description: Kernel fitImage for Linux-microPlatform/5.15.64+gitAUTOINC+0d5ce62585_35bc6145aa/uz3cg-dwg-sec
    Created:         Thu Sep  1 04:40:19 2022
     Image 0 (kernel-1)
      Description:  Linux kernel
      Created:      Thu Sep  1 04:40:19 2022
      Type:         Kernel Image
      Compression:  gzip compressed
      Data Size:    9831595 Bytes = 9601.17 KiB = 9.38 MiB
      Architecture: AArch64
      OS:           Linux
      Load Address: 0x18000000
      Entry Point:  0x18000000
      Hash algo:    sha256
      Hash value:   4087645d7b85479e76824652aaf764cb5248ffb07572186553a7cc74a80c7a06
     Image 1 (fdt-system-top.dtb)
      Description:  Flattened Device Tree blob
      Created:      Thu Sep  1 04:40:19 2022
      Type:         Flat Device Tree
      Compression:  uncompressed
      Data Size:    45983 Bytes = 44.91 KiB = 0.04 MiB
      Architecture: AArch64
      Load Address: 0x40000000
      Hash algo:    sha256
      Hash value:   5270804486f9aeed060da21a2879ce21c60b5cb45ffef7b35b1fac3171c6ee81
     Default Configuration: 'conf-system-top.dtb'
     Configuration 0 (conf-system-top.dtb)
      Description:  1 Linux kernel, FDT blob
      Kernel:       kernel-1
      FDT:          fdt-system-top.dtb
      Hash algo:    sha256
      Hash value:   unavailable
      Sign algo:    sha256,rsa2048:ubootdev
      Sign value:   c07a5cd7408836c2e03fb9dce22c7670e87e8a8e2e32676e1d91c853848324fab28fb3fb1e3fda6ea8f6b93c73dd63bbc8877ddcca186cfef1b051d54ddb26a303eea2d66bebe1c1471bd1018b4fc1ef2a53d1d00b540de3c0b15eab3fba4a3767a72a4131f1dd74115e5fd3a79e71acdcee8decd75ca469c97a6713753dcb90dfe114ccc8abb03a84db7ec818123326b0639c85f79379f4d3d63ba495ab1568e62ea2f779bea011a44ce152df286e9039f6ba6a0199632dfa7bfb8794fd5dffed14678a0e5ae009cf07598772178e783930eceee6b48a05c424ac252bd25a6151825d1f3d1747a4bc17847d27e1465590a0dc6b75d8f545b44df1b7407e8b70
      Timestamp:    Thu Sep  1 04:40:19 2022

Then to extract the bootable kernel image (position 0 in the FIT) to a
file named ``Image`` use the dumpimage utility

.. prompt:: text

    $ dumpimage -T flat_dt -p 0 -o Image fitImage-uz3cg-dwg-sec.bin
    Extracted:
     Image 0 (kernel-1)
      Description:  Linux kernel
      Created:      Thu Sep  1 04:40:19 2022
      Type:         Kernel Image
      Compression:  gzip compressed
      Data Size:    9831595 Bytes = 9601.17 KiB = 9.38 MiB
      Architecture: AArch64
      OS:           Linux
      Load Address: 0x18000000
      Entry Point:  0x18000000
      Hash algo:    sha256
      Hash value:   4087645d7b85479e76824652aaf764cb5248ffb07572186553a7cc74a80c7a06


And to extract the device tree blob (position 1 in the FIT) to a file named ``system.dtb``:

.. prompt:: text

    $ dumpimage -T flat_dt -p 1 -o system.dtb fitImage-uz3cg-dwg-sec.bin
    Extracted:
     Image 1 (fdt-system-top.dtb)
      Description:  Flattened Device Tree blob
      Created:      Thu Sep  1 04:40:19 2022
      Type:         Flat Device Tree
      Compression:  uncompressed
      Data Size:    45983 Bytes = 44.91 KiB = 0.04 MiB
      Architecture: AArch64
      Load Address: 0x40000000
      Hash algo:    sha256
      Hash value:   5270804486f9aeed060da21a2879ce21c60b5cb45ffef7b35b1fac3171c6ee81


The ramdisk is deployed as
``initramfs-ostree-lmp-image-${platform-name}.cpio.gz``. In order for
U-boot to consume it we need to convert the archive to a ramdisk
image. For that, U-boot provides the mkimage Linux utility.

Run the following command to generate the ``ramdisk`` file:

.. prompt:: text

    $ mkimage -A arm -O linux -T ramdisk -d initramfs-ostree-lmp-image-uz3cg-dwg-sec.cpio.gz ramdisk

At this point, we have all the components to boot over NFS. The TFTP
server shall export ``Image``, ``system.dtb`` and ``ramdisk``.


Using U-boot to boot the NFS
-----------------------------
For the first boot you will have to flash the WIC image as per the LmP
instructions. Then boot the system and dump the command line:

.. prompt:: text

    root@uz3cg-dwg-sec:~# cat /proc/cmdline
    earlycon console=ttyPS0,115200 clk_ignore_unused root=/dev/mmcblk0p2 rootfstype=ext4 ostree=/ostree/boot.1/lmp/180c0adc612a144a262f15e6c124cc3ac22260b7b2897832a1228da2d3e359a5/0


Since we will need to halt the boot sequence at the U-boot prompt, you
might have to set the ``bootdelay`` U-boot variable. This could be done
either in your build or at this time from the LmP linux shell.

To do this from the Linux shell, use the ``fw_setenv`` utility.

After re-booting to the U-boot prompt, modify the ``bootargs``
environment variable with the NFS enabled command line. Also use the
``tftpboot`` u-boot shell command to pull ``Image``, ``system.dtb`` and
``ramdisk`` from the TFTP server into memory.


1. bootargs for NFS server at 192.168.1.8

   Replace the pointers to persistent storage in the previous command line with the NFS information.
   ``root=/dev/nfs nfsroot=192.168.1.8:/srv/nfs/rootfs rootwait rw ip=dhcp``

.. prompt:: text

    uboot> setenv bootargs "earlycon console=ttyPS0,115200 clk_ignore_unused root=/dev/nfs rootfstype=ext4 ostree=/ostree/boot.1/lmp/180c0adc612a144a262f15e6c124cc3ac22260b7b2897832a1228da2d3e359a5/0 nfsroot=192.168.1.99:/srv/nfs/rootfs rootwait rw ip=dhcp"

2. tftp server at 192.168.1.7 and various memory addresses for the
   different files to download.

.. prompt:: text

    uboot> setenv tftpserverip 192.168.1.7; setenv ipaddr=dhcp;
    uboot> setenv initrd 0x10A00000; setenv imgaddr 0x800000000; setenv dtaddr 0x10000000;
    uboot> tftpboot ${dtaddr}  ${tftpserverip}:system.dtb
    uboot> tftpboot ${initrd}  ${tftpserverip}:ramdisk
    uboot> tftpboot ${imgaddr} ${tftpserverip}:Image;


3. Finally boot the image:

.. prompt:: text

    uboot> booti ${imgaddr} ${initrd} ${dtaddr}
