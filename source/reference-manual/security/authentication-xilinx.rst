.. highlight:: sh


.. _ref-authentication-xilinx:

Secure Boot on Zynq UltraScale+ MPSoC
=====================================
This is a simple guide on how to provision a device enabling the bootloader hardware authentication.

.. note::

   Helper scripts are also available at the `lmp-tools`_ repository.

Get the PMU firmware
--------------------
Get a valid version of the PMU firmware for the hardware ``pmu.bin`` (also available at the deploy folder if built with LmP).

Build the bootloader
--------------------
Build U-boot for the ZynqMP SoC platform including SPL support ``u-boot-spl.bin`` (also available at the deploy folder if built with LmP).

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
At the time of writing, there is not an open source solution that allows the user to read/write to the ZynqMP SoC eFUSEs. A good alternative to other GUI based tools from Xilinx is to use the Xilinx Lightweight Provisioning Tool, since it allows requests to be scripted: use this tool to write the content of ``fuse-ppk.txt`` to the PPK eFUSE. Notice that this tool is only shared on demand from your Xilinx support representative.

For more information on how to program the eFUSEs, please have a look at `XAPP1319`_.

If you want to roll-out your own solution to read or write to the eFUSES, please have a look at the `Xilskey service`_ and the relevant `documentation`_; be aware however that these registers are only accessible from exception level 3 (EL3).

A simple solution if you wanted to pass some of those eFUSE values to TF-A or OP-TEE would be to read them from SPL and then add them to the ``secure-chosen`` node in the device tree which would then be shared with those executables.

Program the bootable image
--------------------------
Unless you are booting from SD or eMMC devices, chances are that you will need to use the JTAG interface for that first write to QSPI. JTAG accessibility however seems to be only viable using the Xilinx VIVADO SDK which is big commitment in terms of storage.

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

Now extend the `bitstream-signed`_ recipe including your signed bitstream, then select it as the preferred provider for ``virtual/bitstream`` and specify the right binary and compatible string, such as::

       $ cat meta-lmp-bsp/conf/machine/uz3eg-iocc-sec.conf

       # Signed FPGA bitstream is needed on secure/closed targets
       PREFERRED_PROVIDER_virtual/bitstream = "bitstream-signed"
       SPL_FPGA_BINARY = "bitstream-signed.bit.bin"
       SPL_FPGA_COMPATIBLE = "u-boot,zynqmp-fpga-ddrauth"

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

Secure Storage (RPMB) using the PUF
===================================

The PUF can be used to generate a hardware unique key (HUK) at OP-TEE for secure storage via the eMMC RPMB partition.

For PUF to be functional you will need to fuse PPK and RSA_EN (for secure boot), register the PUF and program the syndrome data (via Red AES key).

We recommend using the XLWPT tool (as described at `XAPP1319`_) for registering PUF::

          ___  ___ _ __        _ ____
         /   /\  /| |\ \      / /  _ \
        /___/  \/ | | \ \ /\ / /| |_) |
        \   \     | |__\ |  | / |  __/
         \   \    \_____\_/\_/  |_|
         /   /     Zynq UltraScale+ MPSoC: ZU3EG
        /__ /      Lightweight Provisioning Tool
        \   \  /\  XLWP Tool Version: 1.9
         \___\/__\ ::: PUF Menu :::
        _________________________________________

         1. Register the PUF
         2. Encrypt Red AES Key w/ PUF Key
         3. Display Bootheader Mode PUF Data
         4. Program PUF-related eFUSEs
         5. Read & Display PUF-related eFUSEs

         x. Exit sub-menu

         Please make a selection -> 1 (registering the PUF)

         Please make a selection -> 2 (encrypting red AES key w/ PUF key)

         > Enter the 256-bit Red AES key (64 hex characters):
         ----------------------------------------------------------------
         0123456789012345678901234567890123456789012345678901234567890123
         Is the key correct?! (y/[n]) -> y

         > Enter the 96-bit AES IV (24 hex characters):
         ------------------------
         012345678901234567890123
         Is the IV correct?! (y/[n]) -> y

         *** Red AES Key and IV for Black Key Captured OK! ***
         *** Black Key Created OK! ***

         Press any key to continue...

         Please make a selection -> 4 (program PUF-related eFUSEs)

         1. Syndrome, AUX, CHASH & Black Key eFUSEs
         2. SYN_INVLD eFUSE
         3. SYN_WR_LOCK eFUSE
         4. REG_DIS eFUSE

         Please make a selection -> 1

         Program Syndrome, AUX, CHASH & Black Key eFUSEs...are you sure?! (y/[n]) -> y

         *** Syndrome, AUX, CHASH & Black Key eFUSEs programmed OK! ***

         Press any key to continue...

         PUF syndrome (helper data) read from eFUSEs:
         ----------------------------------------------------------------
         C6F960D575ACB5E2BCDDFF4BEE586E8F35EB2231BA7F9A55263431BF382673AE
         0E774B4FA35165166025228F8F6A699D469AF76409D789A0C35F7D12B74A9AB8
         2CCD677BF770DBA0522431806955EE7614E5795FACB28F4CAED5B27206737968
         45F367953804F46626D6D69003F68EAFA0653E79FBAEAD854369F7959858117A
         169D11305DEF45F54056F2C39714FEB36364E1F9C82C6861ADB0B83FE59F0585
         C69E4CE96DB4328FA98E9CB0CAF9DCE50F793582160AD6E6CB9A9E54D24F82D8
         30A22ECEE5AA24AF4B689D53F76D89B1ADA695FC5AA722967F20B6D827F5E18C
         13D76F08D34EFC7E2C0FFB261E0AC2A310B4E88BFACAED6C2E964EFF2701ED15
         2825CA046B159FA63470166DF82912A7F983733AA73C03A6ED6F63CB70CC9761
         791B5BD5BE7EB2681C95F447C707B416F688DA5C34C627113F8DABB0AA2A6424
         72F57E9CF797574402BFFDBFBCC947BD9EACC18BB0A55CF0B2D024BE25B81022
         69CDD2EAE3BACF415B28AA310AA9941ACCA5E7C64BBAA1878D55FB7666B93B46
         BFDA36E8E8B49DF5243F6B217970408ED101DD6977933474AD5178B41517D825
         868A5DB679E66752AA7CBA300B700C0BD1DDE6A7E3528BD2FBFA24031D971CCE
         0BA2944FA09AD655204068744F3D401033BACBE849A69360A4077F5DB230E01D
         9278AF71941D711215FFA89CD3F73DC976EC2DC8D5B6BB1AD0618B3F

         PUF AUX value read from eFUSEs   : 0x0062C179
         PUF CHASH value read from eFUSEs : 0x8D22500B

For more information on registering the PUF and how it is used by OP-TEE for generating a hardware unique key, please have a look at `XAPP1333`_ and https://github.com/OP-TEE/optee_os/pull/4874.

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

.. _XAPP1319:
   https://www.xilinx.com/support/documentation/application_notes/xapp1319-zynq-usp-prog-nvm.pdf

.. _XAPP1333:
   https://www.xilinx.com/support/documentation/application_notes/xapp1333-external-storage-puf.pdf

.. _bitstream-signed:
   https://github.com/foundriesio/meta-lmp/blob/master/meta-lmp-bsp/dynamic-layers/xilinx-tools/recipes-bsp/bitstream/bitstream-signed_git.bb

.. _lmp-tools:
   https://github.com/foundriesio/lmp-tools/tree/master/security/zynqmp

.. _RFC:
   https://lists.denx.de/pipermail/u-boot/2021-October/462571.html
