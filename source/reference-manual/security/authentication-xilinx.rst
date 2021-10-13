.. highlight:: sh


.. _ref-authentication-xilinx:

Secure Boot on Zynq UltraScale+ MPSoC
=====================================
This is a simple guide on how to provision a device enabling the bootloader hardware authentication.

Get the PMU firmware
--------------------
Get a valid version of the PMU firmware for the hardware ``pmu.bin``

Build the bootloader
--------------------
Build U-boot for the ZynqMP SoC platform including SPL support ``u-boot-spl.bin``

Create the Primary and Secondary keys
-------------------------------------
Create a set of PEM keys that will be used by the hardware to authenticate the bootloader::

       $ cat keys.bif
       keys:
       {
              [ppkfile] <PPK.pem>
              [pskfile] <PSK.pem>
              [spkfile] <SPK.pem>
              [sskfile] <SSK.pem>
       }

       $./bootgen -arch zynqmp -image keys.bif -generate_keys pem

Create the bootable image
-------------------------
Create the bootable image requesting only authentication by using the following BIF. In this example, the PMUFW and SPL would be loaded at specific locations.

It is worth mentioning that whenever authentication is enabled for the bootloader, the PMUFW will also be signed::

       $ cat bootloader.bif
       the_ROM_image:
       {
               [pskfile] PSK.pem
               [sskfile] SSK.pem
               [pmufw_image, load=0xffdc0000] pmu.bin
               [bootloader, authentication=rsa, destination_cpu=a53-0, load=0xfffc0000] u-boot-spl.bin
        }

        $ ./bootgen -arch zynqmp -image bootloader.bif -w on -o boot.bin -efuseppkbits fuse-ppk.txt

Besides ``boot.bin``, bootgen will also generate a SHA-384 of the PPK ``fuse-ppk.txt`` which will need to be written to the PPK fuse so that the hardware can authenticate the image with the public primary key.

Check the bootable image
------------------------
The integrity of the generated image can be checked as follows::

        $ ./bootgen -arch zynqmp -image boot.bin -verify

The layout of the bootable image can be read as follows::

        $ ./bootgen -arch zynqmp -read boot.bin

Fuse the Primary Public Key SHA-384
-----------------------------------
At the time of writing, there is not an open source solution that allows the user to read/write to the ZynqMP SoC eFUSEs. A good alternative to other GUI based tools from Xilinx is to use the Xilinx Lightweight Provisioning Tool, since it allows requests to be scripted: use this tool to write the content of ``fuse-ppk.txt`` to the PPK eFUSE.
Notice that this tool is only shared on demand from your Xilinx support representative.

If you want to roll-out your own solution to read or write to the eFUSES, please have a look at the `Xilskey service`_ and the relevant `documentation`_; be aware however that these registers are only accessible from exception level 3 (EL3).

A simple solution if you wanted to pass some of those eFUSE values to TF-A or OP-TEE would be to read them from SPL and then add them to the ``secure-chosen`` node in the device tree which would then be shared with those executables.

Program the bootable image
--------------------------
Unless you are booting from SD or eMMC devices, chances are that you will need to use the JTAG interface for that first write to QSPI. JTAG accessibility however seems to be only viable using the Xilinx VIVADO SDK which is  big commitment in terms of storage.

One alternative to a full SDK install is running Vivado in a container on your Linux machine. During this development, we used the following `vivado_docker`_ repository.

Sign the FPGA bitstream
-----------------------
When authentication is enabled in the bootable image, the CSU will also authenticate the FPGA bistream before allowing it to load.
Because of this, the bitstream must also be signed before adding it to the FIT image::

       $ cat fpga.bif
       the_ROM_image:
       {
               [auth_params] ppk_select=0; spk_id=0x00000000
               [pskfile] PSK.pem
               [sskfile] SSK.pem
               [destination_device=pl, authentication=rsa] fpga.bit
	}

        $ ./bootgen -arch zynqmp -image fpga.bif -w on -o fpga.bit.bin

U-boot also needs to be modified in order to load an authenticated FPGA image from FIT. We have posted an `RFC`_ to address this situation and we will work towards landing it upstream.

However, if your use case allows to load the signed bitstream from the U-Boot shell you could just use the load secured zynqmp command; in the example below we are loading the unencrypted signed bitstream from DDR at address ``0x10000000`` with a size of ``0x70000`` bytes::

       $ fpga loads 0 0x10000000 0x70000 1 2


Booting SPL
-----------
Applying this `patch`_ to U-boot you should see the following on a successful boot::

        U-Boot SPL 2021.07+xlnx+gb9b970209c (Jul 22 2021 - 10:50:54 +0000)
        PMUFW:  v1.1
        Loading new PMUFW cfg obj (1992 bytes)
        Silicon version:        3
        EL Level:       EL3
        Chip ID:        zu3cg
        Multiboot:      0
        Secure Boot:    authenticated, not encrypted
        Trying to boot from SPI
        ## Checking hash(es) for config config-1 ... OK
        FPGA image loaded from FIT
        ## Checking hash(es) for Image atf ... sha256+ OK
        ## Checking hash(es) for Image uboot ... sha256+ OK
        ## Checking hash(es) for Image ubootfdt ... sha256+ OK
        ## Checking hash(es) for Image optee ... sha256+ OK

        NOTICE:  ATF running on XCZU3CG/silicon v4/RTL5.1 at 0xfffe5000
        NOTICE:  BL31: v2.4(release):xlnx_rebase_v2.4_2021.1
        NOTICE:  BL31: Built : 15:34:08, Jul  9 2021

        I/TC:
        I/TC: Non-secure external DT found
        I/TC: OP-TEE version: 3.10.0-106-g60c99179 (gcc version 10.2.0 (GCC)) #1 Fri Jul  9 15:34:48 UTC 2021 aarch64
        I/TC: Primary CPU initializing
        I/TC: Primary CPU switching to normal world boot

        U-Boot 2021.07+xlnx+gb9b970209c (Jul 22 2021 - 10:54:24 +0000)
        [...]


.. note::
        Booting a secure image disables the JTAG interface even if no JTAG related fuses were written. Use the SPL configuration option `CONFIG_SPL_ZYNQMP_RESTORE_JTAG`_ to re-enable it on boot.

.. _vivado_docker:
   https://github.com/ldts/petalinux-docker.git

.. _CONFIG_SPL_ZYNQMP_RESTORE_JTAG:
   https://lists.denx.de/pipermail/u-boot/2021-July/455132.html

.. _patch:
   https://lists.denx.de/pipermail/u-boot/2021-July/455752.html

.. _Xilskey service:
   https://github.com/Xilinx/embeddedsw/tree/master/lib/sw_services/xilskey

.. _documentation:
   https://github.com/Xilinx/embeddedsw/blob/master/lib/sw_services/xilskey/doc/xilskey.pdf

.. _RFC:
   https://lists.denx.de/pipermail/u-boot/2021-October/462571.html
