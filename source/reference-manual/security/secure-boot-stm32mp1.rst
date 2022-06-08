.. highlight:: console

.. _ref-secure-boot-stm32mp1:

Secure Boot on STM32MP1
=======================

Secure boot is a key feature to guarantee a secure platform. STM32MP1 boot
sequence supports a trusted boot chain that ensures that the loaded images
are authenticated and checked in integrity before being used.

Our Implementation
------------------

Foundries.io LmP uses U-Boot as the bootloader with TF-A BL2 being its first
stage loader. The secure boot implementation will put the IC in a secure state
accepting only signed TF-A BL2 firmware.

TF-A then boots the trusted execution environment - OP-TEE - where we run an
'early' trusted application, fiovb - Foundries.io Verified Boot. This trusted
application provides secure access to the Replay Protected Memory Block partition
in eMMC which is used to store keys, firmware and rollback information.

OP-TEE also prepares the next stage bootloader - U-Boot - and generates an
overlay DTS for the Linux kernel consumption. U-boot also implements the fiovb
command to validate the trusted application functionality. U-boot then jumps to
the kernel entry point.

How to Secure the Platform
--------------------------

The first step is to generate the ECC key pair and commit the fuse table
to the hardware. This can be done with the STM32 KeyGen tool, which is part of
the `STM32CubeProgrammer SDK`_ software package.

Here is an example of generating a key pair using KeyGen tool::

        $ cd STM32CubeProgrammer
        STM32CubeProgrammer$ ./bin/STM32MP_KeyGen_CLI
        -------------------------------------------------------------------
                        STM32MP Key Generator v2.10.0
        -------------------------------------------------------------------

        STM32AP Key Generator [Version v2.10.0] <'-? for help>
        Copyright (c) 2018 STMicroelectronics. All rights reserved.
        Please enter Path for output files  < /tmp/ >
        /tmp/
        Please enter Password
        Please re-enter your Password
        Please select algorithm:  1. prime256v1   2. brainpoolP256t1 (1/2)?
        1
        Please select encrypting algorithm:  1. aes256   2. aes128 (1/2)?
        1
        Prime256v1 curve is selected.
        AES_256_cbc algorithm is selected for private key encryption
        Generating Prime256v1 keys...
        Private key PEM file created
        Public key PEM file created
        public key hash file created
        Keys generated successfully.
        + public key:       /tmp/publicKey.pem
        + private key:      /tmp/privateKey.pem
        + public hash key:  /tmp/publicKeyhash.bin

The tool also generates a third file containing the public key hash (PKH) that
should be fused to OTP and  used to authenticate the public key on the
target. For more details refer to ST's `STM32 KeyGen tool`_ guide.

To fuse the public key hash, copy it to the first FAT partition of your SD
boot card. During the boot process stop in U-Boot console and run these
commands::

        => mmc rescan
        => STM32MP> fatls mmc 0:4
           3007   boot.itb
             32   publicKeyhash.bin
        => load mmc 0:4 0xc0000000 publicKeyhash.bin
        => stm32key read 0xc0000000
        Read KEY at 0xc0000000
        OTP value 24: 1ce94f90
        OTP value 25: 971d082f
        OTP value 26: d443cf29
        OTP value 27: f7c345d4
        OTP value 28: 14873635
        OTP value 29: b288ad40
        OTP value 30: 38841b57
        OTP value 31: b7a16954

 .. warning::

   Once the fuses have been programmed they can't be modified.

Verify that ``stm32key`` command has printed valid key hashes, and if
everything is correct fuse these values to OTP::

        => stm32key fuse 0xc0000000

The device now contains public key hashes to authenticate boot images.
To validate, read back the OTP, using the same ``stm32key`` command::

        => stm32key read
        OTP HASH 24: 1ce94f90 lock : 0
        OTP HASH 25: 971d082f lock : 0
        OTP HASH 26: d443cf29 lock : 0
        OTP HASH 27: f7c345d4 lock : 0
        OTP HASH 28: 14873635 lock : 0
        OTP HASH 29: b288ad40 lock : 0
        OTP HASH 30: 38841b57 lock : 0
        OTP HASH 31: b7a16954 lock : 0
        OTP 0: closed status: 0 lock : 0
        HASK key is not locked!


Sign and Deploy the BL2 image
-----------------------------

The FSBL binary (TF-A BL2) must be signed. `STM32 Signing tool`_ allows to
fill the STM32 binary header that is parsed by the embedded software to
authenticate each binary.

To sign the image run::

        STM32CubeProgrammer$ ./bin/STM32MP_SigningTool_CLI -bin /build-lmp/deploy/images/stm32mp15-disco/arm-trusted-firmware/tf-a-stm32mp157c-dk2-sync -pubk /tmp/publicKey.pem -prvk /tmp/privateKey.pem -iv 5 -pwd qwerty123 -t fsbl
        -------------------------------------------------------------------
                   STM32MP Signing Tool v2.10.0
        -------------------------------------------------------------------

        Prime256v1 curve is selected.
        Header version 1 preparation ...
        Reading Private Key File...
        ECDSA signature generated.
        Signature verification:  SUCCESS
        The Signed image file generated successfully:  /build-lmp/deploy/images/stm32mp15-disco/arm-trusted-firmware/tf-a-stm32mp157c-dk2-sdcard_Signed.stm32

Validate that signature and sign info (algo etc.) were added to the image::

        STM32CubeProgrammer$ ./bin/STM32MP_SigningTool_CLI -dump /build-lmp/deploy/images/stm32mp15-disco/arm-trusted-firmware/tf-a-stm32mp157c-dk2-sdcard_Signed.stm32
        Magic: 0x53544d32
        Signature: f1 f7 3e 73 35 38 a5 00 43 b2 78 fe cd 12 0a ec 39 2e 8a c7 60 35 f4 1f 7f 47 1a 99 11 8a 5b 07
                   9e dc 1c 51 27 bc e2 e0 4c cf 23 6d 87 92 cb c9 a6 ea a1 7f b0 30 18 f4 73 d5 18 ef 50 c6 56 e3
        Checksum: 0x6d09b9
        Header version: 0x10000
        Size: 0x36fd1
        Load address: 0x2ffc2500
        Entry point: 0x2ffe9000
        Image version: 0x5
        Option flags: 0x0
        ECDSA Algo: 0x1
        ECDSA pub key: f9 0e db 1b d6 91 a5 9d 9f d9 0a a8 63 f2 8b 4c ca 37 c6 65 48 e3 5b 5a 69 b8 8f a9 72 b1 3f 44
                       01 df ae 4c cd 99 12 bc d3 fc 9b 30 7a 77 c5 2b f0 5b 01 f3 2e bb c3 71 db a4 40 93 2c 01 3f a2
        Binary type: 0x10

To deploy signed image to the SD card existing non signed images
must be replaced. That can be achieved with a simple ``dd`` command as well
(instead of mmcblkx specify correct device)::

        $ sudo dd if=/build-lmp/deploy/images/stm32mp15-disco/arm-trusted-firmware/tf-a-stm32mp157c-dk2-sdcard_Signed.stm32 bs=1024 seek=17 of=/dev/mmcblkx
        $ sudo dd if=/build-lmp/deploy/images/stm32mp15-disco/arm-trusted-firmware/tf-a-stm32mp157c-dk2-sdcard_Signed.stm32 bs=1024 seek=273 of=/dev/mmcblkx

Booting Signed Images
---------------------

When a signed binary is used, the BootROM code will authenticate and
start the FSBL, which will report authentication status::

        NOTICE:  CPU: STM32MP157CAC Rev.B
        NOTICE:  Model: STMicroelectronics STM32MP157C-DK2 Discovery Board
        NOTICE:  Board: MB1272 Var2.0 Rev.C-01
        NOTICE:  Bootrom authentication succeeded <------- auth confirmation

A `Bootrom authentication succeeded` message means that BootROM managed
to authenticate the FSBL image and the device can be closed. If the device is
not closed, it will be still able to perform image authentication, but will
boot the image regardless of the result of that authentication.

Closing the Device
------------------

As soon as the authentication process is confirmed, the device can be closed
and the user must use signed images.

OTP ``WORD0`` bit 6 is the OTP bit that closes the device. Fusing this bit
will lock authentication processing and force authentication from the BootROM.
Non signed binaries will not be supported anymore on the target.

To close the device by fusing OTP WORD0 bit 6 run `stm32key` cmd in U-Boot::

        => stm32key close

.. _STM32MPU Security overview:
   https://wiki.st.com/stm32mpu/wiki/Security_overview

.. _STM32 KeyGen tool:
   https://wiki.st.com/stm32mpu/wiki/KeyGen_tool

.. _STM32 Signing tool:
   https://wiki.st.com/stm32mpu/wiki/Signing_tool

.. _STM32CubeProgrammer SDK:
   https://www.st.com/en/development-tools/stm32cubeprog.html
