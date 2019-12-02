.. highlight:: sh

.. _ref-secure-boot:

Secure Boot on IMX
==================
On the IMX platforms, secure boot is implemented via the High Availability Boot component of the on-chip ROM. The ROM is responsible for loading the initial program image, the bootloader; HAB then enables the ROM to authenticate it using digital signatures.
 
HAB also provides a mechanism to establish a root of trust for the remaining software components and stablishes a secure state - the close state - on the IMX IC secure state machine in hardware.

Our implementation
------------------
Foundries LMP uses U-Boot as the bootloader with SPL being its first stage loader. Our secure boot implementation will put the IC in a secure state accepting only signed SPL firmware.

SPL then boots the trusted execution environment - OP-TEE - where we run an 'early' trusted application, fiovb - Foundries.IO verified Boot. This trusted application provides secure access to the Replay Protected Memory Block partition in MMC which is used to store keys and firmware and rollback information.

OP-TEE also prepares the next stage bootloader - U-Boot - and generates an overlay DTS for the Linux kernel consumption. Then it jumps to U-Boot which controls the M4 firmware upgrade process using the fiovb trusted application. U-boot also implements the fiovb command to validate the trusted application functionality. 

U-boot then jumps to the kernel entry point.

HAB Architecture Overview
-------------------------
HAB authentication is based on public key cryptography using the RSA algorithm in which image data is signed offline using a series of private keys. The resulting signed image data is then verified on the i.MX processor using the corresponding public keys. 

This key structure is known as a PKI tree; super root keys, or SRK, are components of the PKI tree: HAB relies on a table of the public SRKs to be hashed and placed in fuses on the target. 
The i.MX Code Signing Tool (CST) is used to generate the HABv4 signatures for images using the PKI tree data and SRK table. 

On the target, HAB evaluates the SRK table included in the signature by hashing it and comparing the result to the SRK fuse values: if the SRK verification is successful, this establishes the root of trust, and the remainder of the signature can be processed to authenticate the image. 

How to Secure the Platform
--------------------------
The first step is to generate the PKI tree and commit the fuse table to the hardware.

 .. warning::

   Once the fuses have been programmed they can't be modified.


Please refer to NXP's `Secure Boot Using HABv4 Guide`_ for a detailed description on how to generate the PKI tree.

For development purposes, we keep iMX HAB4 sample keys and certificates at ``lmp-manifest/conf/imx_hab4``. The fuse table can be inspected by executing the ``print_fuses`` script in that same directory. The output should be::

	0xEA2F0B50
	0x871167F7
	0xF5CECF5D
	0x364727C3
	0x8DD52832
	0xF158F65F
	0xA71BBE78
	0xA3AD024A

The Security Reference Manual for your specific SoC will indicate which fuses need to be programed with the SRK fuse information. On the i.MX7ULP these are stored in the fuse bank 5, words 0 to 7.

To program these fuses you could use U-Boot's fuse command as follows::

	=> fuse prog 5 0 0xEA2F0B50
	=> fuse prog 5 1 0x871167F7
	=> fuse prog 5 2 0xF5CECF5D
	=> fuse prog 5 3 0x364727C3
	=> fuse prog 5 4 0x8DD52832
	=> fuse prog 5 5 0xF158F65F
	=> fuse prog 5 6 0xA71BBE78
	=> fuse prog 5 7 0xA3AD024A

Alternatively, use the kernel to do that or SDP via NXP's Universal Update Utility with a script as follows::

	uuu_version 1.0.1
	
	SDP: boot -f SPL-@@MACHINE@@
	
	SDPU: delay 1000
	SDPU: write -f u-boot-@@MACHINE@@.itb
	SDPU: jump
	
	FB: ucmd fuse prog -y 5 0 0xEA2F0B50
	FB: ucmd fuse prog -y 5 1 0x871167F7
	FB: ucmd fuse prog -y 5 2 0xF5CECF5D
	FB: ucmd fuse prog -y 5 3 0x364727C3
	FB: ucmd fuse prog -y 5 4 0x8DD52832
	FB: ucmd fuse prog -y 5 5 0xF158F65F
	FB: ucmd fuse prog -y 5 6 0xA71BBE78
	FB: ucmd fuse prog -y 5 7 0xA3AD024A
	
	FBK: DONE

Upon reboot, if **CONFIG_IMX_HAB** was enabled in U-boot and since we still didn't close the secure state of the platform, HAB will raise events to indicate that an unsigned image has been executed. Those events can be inspected by running U-Boot's command ``hab_status``.

To secure the platform, there is an extra fuse that needs to be programmed: we will only take that step once we are sure that we can successfully sign and boot a signed image with a matching set of keys (containing the same public key hashes as those stored in the SRK fuses).

How to sign an SPL image (I)
----------------------------
To build a signed image, you need to create a Command Sequence File - CSF - describing all the commands that the ROM will execute during secure boot. These commands instruct HAB on which memory areas of the image to authenticate, which keys to install and use, what data to write to a register and so on. In addition, the necessary certificates and signatures involved in the verification of the image are attached to the CSF generated binary output.

We keep a template at ``lmp-manifest/conf/imx_hab4/u-boot-spl-sign.csf-template``. You must provide the necessary tables and the keys for your product. 

The authenticate data command "blocks" line contains three values and the file containing the data being signed:

- The first value is the address on the target where HAB expects the signed image data to begin.
 
- The second value is the offset into the file where CST will begin signing. 

- The third value is length in bytes of the data to sign starting from the offset. 


It is also required that the IVT and DCD regions are signed. HAB will verify the DCD and IVT fall in an authenticated region: The CSF will not successfully authenticate unless all commands are successful and all required regions are signed.

The information required to fill the data command block line can be retrieved from the SPL binary. Once SPL has been built with **CONFIG_IMX_HAB** enabled, either use mkimage to retrive the information or inspect the SPL log file::

	$ tools/mkimage -l SPL | grep HAB
	HAB Blocks: 0x2f010400 0x00000000 0x00016c00

Once the CSF file has been edited to include this information you will just need to execute NXP's Code Signing Tool and append the generated binary to the SPL image. Notice that the @@KEY_ROOT@@ values in the template file need to be changed to the full path of the key files::

	$ cst -o csf-spl.bin -i u-boot-spl-sign.csf-template
	$ cat SPL csf-spl.bin > SPL.signed


Booting this signed SPL image and inspecting the HAB status should give no HAB events indicating that the image was correctly signed::

	=> hab_status
	Secure boot disabled
	HAB Configuration: 0xf0, HAB State: 0x66
	No HAB Events Found!

.. warning::
    The next fuse instruction will close the board for unsigned images: make sure you can rebuild the signed images before programing that fuse.


Now we can close the device meaning that from thereon only signed images can be booted on this platform. For that, on the i.MX7ULP we need to fuse bit31 of word 6 from bank 29 (SEC_CONFIG[1] in the documentation)::

	=> fuse prog 29 6 0x80000000


Rebooting the board and checking the HAB status should give::

	=> hab_status
	Secure boot enabled
	HAB Configuration: 0xcc, HAB State: 0x99
	No HAB Events Found!

How to sign an SPL image for SDP (II)
-------------------------------------
Once the device has been closed only signed images will be able to run on the processor: this means that upgrades via UUU/SDP will stop working unless the SPL it uses is properly signed.
The following restrictions need to be applied to this signed image:

 - SDP requires that the CSF is modified to include a check for the DCD table 

 - SDP requires that the DCD address of the image is cleared from the header

DCD table to the CSF
~~~~~~~~~~~~~~~~~~~~
To add the DCD table to the CSF begin by inspecting the SPL image looking for the DCD table information::

	/tools/mkimage -l SPL

	Image Type:   Freescale IMX Boot Image
	Image Ver:    2 (i.MX53/6/7 compatible)
	Mode:         DCD
	Data Size:    147552 Bytes = 144.09 KiB = 0.14 MiB
	Load Address: 2f010420
	Entry Point:  2f011000
	HAB Blocks:   0x2f010400 0x00000000 0x00021c00
	DCD Blocks:   0x00910000 0x0000002c 0x00000258

The DCD is always programmed to OCRAM.

Make sure the address on the target where HAB expects the data is consistent with the debug information provided by mkimage: for example on the i.MX7ULP case which we are documenting, we should replace 0x0091000 with 0x2f010000 - a fix to display the right DCD block information using mkimag has been sent to upstream U-boot and is under review.

In order for HAB to check the DCD register map we need to extend the CSF authentication tag as follows::

	[Authenticate Data]
	Verification index = 2
	Blocks = 0x2f010000 0x02c 0x00258 "SPL.bin"

	[Authenticate Data]
	Verification index = 2
	Blocks = 0x2f010400 0x000 0x21c00 "SPL.bin"	

You could check ``lmp-manifest/conf/imx_hab4/u-boot-spl-mfg-sign.csf-template`` for the functional template we have used for development.


Clear the DCD address from the header
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To clear and set the DCD address from the header we use ``conf/imx_hab4/mod_4_mfgtool.sh`` on the SPL image::

 	#!/bin/bash
	if [ $# -lt 2 ] || [ ! -e $2 ]; then
	        echo You must provide an action and a valid u-boot file as parameters
	        echo Example: $0 clear_dcd_addr u-boot.imx
	        exit 1
	fi

	# DCD address must be cleared for signature, as mfgtool will clear it.
	if [ "$1" == "clear_dcd_addr" ]; then
        	# store the DCD address
	        dd if=$2 of=dcd_addr.bin bs=1 count=4 skip=12
	        # generate a NULL address for the DCD
	        dd if=/dev/zero of=zero.bin bs=1 count=4
	        # replace the DCD address with the NULL address
	        dd if=zero.bin of=$2 seek=12 bs=1 conv=notrunc
	        rm zero.bin
	fi

	# DCD address must be set for mfgtool to localize the DCD table.
	if [ "$1" == "set_dcd_addr" ]; then
	        # restore the DCD address with the original address
	        dd if=dcd_addr.bin of=$2 seek=12 bs=1 conv=notrunc
	        rm dcd_addr.bin
	fi


Sign the image for SDP
~~~~~~~~~~~~~~~~~~~~~~
Finally, putting it all together, signing the image for SDP could be sumarized as follows::

	#!/bin/bash
	PROG_NAME=SPL

	# Clear the DCD address
	./mod_4_mfgtool.sh clear_dcd_addr SPL.bin

	# Generate the signatures 
	./cst_64 --o SPL_csf.bin --i SPL.csf

	# Set the DCD address
	./mod_4_mfgtool.sh set_dcd_addr SPL.bin

	# Append the signature to the SPL binary
	cat SPL.bin SPL_csf.bin > SPL_signed.bin

Booting signed images with the `Universal Update Utility`_
-----------------------------------------------------------
When booting signed images we need to let SDP know the the DCD location as well as inform that the DCD has been cleared.
So a tipycal UUU boot script would be as::

	uuu_version 1.0.1
	
	SDP: boot -f SPL-@@MACHINE@@ -dcdaddr 0x2f010000 -cleardcd
	
	SDPU: delay 1000
	SDPU: write -f u-boot-@@MACHINE@@.itb

Moreover, if the device has been closed and it is only accepting signed images, **it is recommended that UUU is started before powering the board and before connecting it to the host PC so that UUU polls for the connection and responds to it as soon as possible**. To that effect we need to make sure of UUU's polling period flag::

	$ uuu -pp 1 file.uuu

.. note::
	All these flags `-dcdaddr`_, `-cleardcd`_ and `-pp`_ required for SDP have been contributed to the Universal Update Utility by Foundries.IO. Make sure your UUU release is up-to-date with these changes.


.. _Secure Boot Using HABv4 Guide:
   https://www.nxp.com/docs/en/application-note/AN4581.pdf

.. _Universal Update Utility:
   https://github.com/NXPmicro/mfgtools

.. _-dcdaddr:
   https://github.com/NXPmicro/mfgtools/commit/003b6cb7a98ba36d78d591b5c1ef8e42423f1b90

.. _-cleardcd:
   https://github.com/NXPmicro/mfgtools/commit/a3e9f5b84d28666d53f565abecf59996b7810aca

.. _-pp:
   https://github.com/NXPmicro/mfgtools/commit/5a790eae0a0f424e145171681e1a3a4f3fa47904

