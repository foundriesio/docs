
.. _ref-secure-boot-ti-am62x.rst:

Secure Boot on TI AM62x
=======================

Secure TI devices require all images in the boot chain (``tiboot3.bin``, ``tispl.bin``, and ``u-boot.img``) be authenticated by ROM.

In order to create valid boot images, the initial public software images must be signed and combined with various headers, certificates, and other binary images.

Secure Board Provisioning
-------------------------

Fusing Keys
^^^^^^^^^^^

At the time of this writing, provisioning the RoT keys requires software only available under an NDA: the **One Time Programmable Key Writer**.

The non-secure component of this software executes on the R5 core and handles the certificate for the secure binary running on one of the M4 cores.
The secure binary will perform the writing of the fuses.

The software accepts either one or two private RSA 4096 keys to generate a PEM certificate:

.. code-block:: console

  gen_keywr_cert.sh -t tifek/ti_fek_public.pem       \ # TI SoC specific key
                    --msv 0xC0FFE                    \ #
                    -b keys_devel/bmpk.pem           \ # back up sign
		    --bmek keys_devel/bmek.key       \ # back up encrypt
		    -s keys_devel/smpk.pem           \ # primary sign
		    --smek keys_devel/smek.key       \ # primary encrypt
		    --keycnt 2                       \ # number of keys
		    --keyrev 1                       \ # active key

.. warning::

   If the generated certificate is above 5.4KB, the user will have to program it incrementally.
   This means invoking the certification generation script and programming the final binary image a number of times.
   The board will be secured the moment ``keyrev`` is set.

Either one of the keys will be used by the ROM to perform signature verification.
Even if not necessary, fusing two keys is recommended.
The ROM can be reverted in the field to use the secondary key in case the primary one is suspected of being compromised.

Once generated, the certificate needs to be transformed into a C header file.
This file is then included in a board specific build process, which generates the final boot-able image.

As described below, this header file can be distributed to non-secure environments, since critical fields are ultimately encrypted with the TI FEK public key.

Building the boot-able image requires standard development tools publicly available from Texas Instruments:  Code Composer Studio, Sysconfig, and the SDK.

On boot, this image will program the SoC fuses required to enable secured boot.
As the am62x supports DFU boot, fusing a board only requires a single command:

.. code-block:: console

   $ dfu-util -R -a bootloader -D fuse.bin

The following strings should be displayed on your host when the device is plugged in with DFU mode::

   New USB device number 87 using xhci_hcd
   New USB device found, idVendor=0451, idProduct=6165, bcdDevice= 2.00
   New USB device strings: Mfr=1, Product=2, SerialNumber=3
   Product: AM62x DFU
   Manufacturer: Texas Instruments, Inc.
   SerialNumber: 01.00.00.00

Certificate Generation in the OTP KeyWriter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The process requires the OEM to generate a random 256-bit number.
This number will be the AES symmetric encryption key, used to protect sensitive information in the X509 certificate extension fields.

   1. SMPK/BMPK: Public key hash (512 bits)
                 The hash of the RSA-4096 firmware sign key
   2. SMEK/BPMK: Symmetric encryption key
                 A 256 bit encryption key if encrypted boot is configured

.. note::

   If the user does not generate one, the tool shall do it on their behalf.

To protect the AES encryption key and the hash, two additional extensions are created:

   1. AES-256 key
   2. AES-256 key signature generated using the SMPK private key

These are protected/encrypted with the TI FEK public key (also RSA-4096).

All four extensions are then combined into an X.509 configuration certificate.
This configuration certificate is signed with the SMPK private key to create the final X509 certificate.

The OTP Keywriter project needs access to the keys to be fused, as well as the TI FEK key.

 - ``TI FEK`` : ``tifek/ti_fek_public.pem``
 - ``SMPK``   : ``keys_devel/smpk.pem``
 - ``SMEK``   : ``keys_devel/smek.key``
 - ``BMPK``   : ``keys_devel/bmpk.pem``
 - ``BMEK``   : ``keys_devel/bmek.key``


Installing Software on Secured Boards
-------------------------------------

The boot-chain is well described in Texas Instruments U-boot's `documentation`_ page for the am62x platform.
In summary, the following images need to be build and signed.

- ``tiboot3.bin``:

.. code-block:: text

                +-----------------------+
                |        X.509          |
                |      Certificate      |
                | +-------------------+ |
                | |                   | |
                | |        R5         | |
                | |   u-boot-spl.bin  | |
                | |                   | |
                | +-------------------+ |
                | |                   | |
                | |TIFS with board cfg| |
                | |                   | |
                | +-------------------+ |
                | |                   | |
                | |                   | |
                | |     FIT header    | |
                | | +---------------+ | |
                | | |               | | |
                | | |   DTB 1...N   | | |
                | | +---------------+ | |
                | +-------------------+ |
                +-----------------------+

- ``tispl.bin``

.. code-block:: text

                +-----------------------+
                |                       |
                |       FIT HEADER      |
                | +-------------------+ |
                | |                   | |
                | |      A53 ATF      | |
                | +-------------------+ |
                | |                   | |
                | |     A53 OPTEE     | |
                | +-------------------+ |
                | |                   | |
                | |      R5 DM FW     | |
                | +-------------------+ |
                | |                   | |
                | |      A53 SPL      | |
                | +-------------------+ |
                | |                   | |
                | |   SPL DTB 1...N   | |
                | +-------------------+ |
                +-----------------------+

- ``u-boot.img``

.. code-block:: text

                +-----------------------+
                |                       |
                |       FIT HEADER      |
                | +-------------------+ |
                | |                   | |
                | |      U-Boot       | |
                | +-------------------+ |
                | |                   | |
                | |     U-Boot dtb    | |
                | +-------------------+ |
                +-----------------------+


Signing the different components of the boot-chain has been `integrated`_ in U-Boot's binman, simplifying the previous process.
At the time of this writing, the code is only available in the vendor's repository hence why this page uses hyperlinks to vendor software and not upstream.

Compiling U-Boot will take care of signing not only the binaries it generates,
but the rest of the firmware images that need to be included in the final images.

As a user, you will need to **replace** U-Boot's ``arch/arm/mach-k3/keys/custMpk.pem`` with the RSA-4096 key that was fused during provisioning.
This will sign all other binaries and firmwares, including the externally generated TF-A, OP-TEE.

.. _documentation:
   https://git.ti.com/cgit/ti-u-boot/ti-u-boot/tree/doc/board/ti/am62x_sk.rst?h=ti-u-boot-2023.04

.. _integrated:
   https://git.ti.com/cgit/ti-u-boot/ti-u-boot/commit/?h=ti-u-boot-2023.04&id=dd467d4f53808c92dd4b47d7e3f57825607670cf
