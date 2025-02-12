.. highlight:: sh

.. _ref-secure-boot-imx-habv4:

Secure Boot on i.MX 6/8M Using HABv4
======================================

On the i.MX 6/8M platforms, Secure Boot is implemented via the High Availability Boot (HABv4) component of the on-chip ROM.
The ROM is responsible for loading the initial program image, the bootloader; HABv4 then enables the ROM to authenticate it using digital signatures.

HABv4 also provides a mechanism to establish a root of trust for the remaining software components and establishes a secure state—the close state—on the i.MX IC secure state machine in hardware.

Our Implementation
------------------

The LmP uses U-Boot as the bootloader, with SPL being its first stage loader.
Our Secure Boot implementation will put the IC in a secure state, accepting only signed SPL firmware.

SPL then boots the trusted execution environment—OP-TEE—where we run an 'early' trusted application, ``fiovb`` (Foundries.io™ Verified Boot).
This trusted application provides secure access to the Replay Protected Memory Block (RPMB) partition in eMMC.
This is used to store keys, firmware, and rollback information.

OP-TEE also prepares the next stage bootloader—U-Boot—and generates an overlay DTS for the Linux® kernel consumption.
U-Boot implements the ``fiovb`` command to validate the trusted application functionality.

U-Boot then jumps to the kernel entry point.

A system which boots without TF-A would look as follows:

   .. figure:: /_static/imx-secure-boot.png
      :align: center
      :width: 6in

Systems using TF-A (ie, i.MX 8M*) are slightly different.
The following diagrams describes the secure boot sequence with a succinct description of the Yocto Project meta-layer's configuration for i.MX 8MM based platforms with TF-A:

   .. figure:: /_static/imx8-secure-boot.png
      :align: left
      :width: 8in

The communication path to gain access from userland to RPMB via the pseudo trusted application (PTA) follows the OP-TEE standard convention for PTAs (as the image below describes).
Userland uses ``libteec`` to issue an ioctl call to the Linux TEE driver, which in turn transitions the processor to its secure state and calls the application entrypoint.

With this in mind, ``fiovb`` is implemented as a secured user application instead of a PTA.

   .. figure:: /_static/optee-pta-access.png
      :align: center
      :width: 6in


HABv4 Architecture Overview
---------------------------

HABv4 authentication is based on public key cryptography using the RSA algorithm, in which image data is signed offline using a series of private keys.
The resulting signed image data is then verified on the i.MX processor using the corresponding public keys.

This key structure is known as a PKI tree; super root keys, or SRK, are components of the PKI tree: HAB relies on a table of the public SRKs to be hashed and placed in fuses on the target.
The i.MX Code Signing Tool (CST) is used to generate the HABv4 signatures for images using the PKI tree data and SRK table.

On the target, HAB evaluates the SRK table included in the signature by hashing it and comparing the result to the SRK fuse values: if the SRK verification is successful, this establishes the root of trust, and the remainder of the signature can be processed to authenticate the image.

How to Secure the Platform
--------------------------

.. note::
	 This page illustrates how the HABv4 Secure Boot process works.
	 It provides background information for our :ref:`ref-secure-machines` implementation for better understanding.

	 We recommend fusing and closing a board following our :ref:`ref-secure-machines` guide.
	 In the guide, some steps described here are omitted, and handled in our code for simpler and safer operations.

The first step is to generate the PKI tree, and commit the fuse table to the hardware.

 .. warning::
    Once the fuses have been programmed they can not be modified.

Please refer to the NXP® `Secure Boot Using HABv4 Guide`_ for a detailed description on how to generate the PKI tree.

For development purposes, we keep i.MX HABv4 sample keys and certificates at `lmp-tools/security/imx_hab4`_.
The fuse table can be inspected by executing the ``print_fuses`` script in that same directory.
The output should be::

	0xEA2F0B50
	0x871167F7
	0xF5CECF5D
	0x364727C3
	0x8DD52832
	0xF158F65F
	0xA71BBE78
	0xA3AD024A

The Security Reference Manual for your specific SoC will indicate which fuses need to be programmed with the SRK fuse information.

i.MX 8MM Fusing
^^^^^^^^^^^^^^^

.. warning::
	 The values shown in this section are just examples of our standard LmP HABv4 keys and are not meant for production.
	 Fuses cannot be changed after the first write.

On the i.MX 8MM the A-core fuses are stored in fuse banks 6-7, words 0 to 3::

        => fuse prog -y 6 0 0xEA2F0B50
        => fuse prog -y 6 1 0x871167F7
        => fuse prog -y 6 2 0xF5CECF5D
        => fuse prog -y 6 3 0x364727C3
        => fuse prog -y 7 0 0x8DD52832
        => fuse prog -y 7 1 0xF158F65F
        => fuse prog -y 7 2 0xA71BBE78
        => fuse prog -y 7 3 0xA3AD024A

Alternatively, you can use the kernel to program the A-core fuses via SDP by using NXP's Universal Update Utility.
This is shown in the following script::

        uuu_version 1.2.39

        SDP: boot -f imx-boot-mfgtool.signed

        SDPU: delay 1000
        SDPV: write -f u-boot-mfgtool.itb
        SDPV: jump

        FB: ucmd fuse prog -y 6 0 0xEA2F0B50
        FB: ucmd fuse prog -y 6 1 0x871167F7
        FB: ucmd fuse prog -y 6 2 0xF5CECF5D
        FB: ucmd fuse prog -y 6 3 0x364727C3
        FB: ucmd fuse prog -y 7 0 0x8DD52832
        FB: ucmd fuse prog -y 7 1 0xF158F65F
        FB: ucmd fuse prog -y 7 2 0xA71BBE78
        FB: ucmd fuse prog -y 7 3 0xA3AD024A

        FB: acmd reset

        FB: DONE


Upon reboot, if ``CONFIG_IMX_HAB`` is enabled in U-Boot, HABv4 will raise events indicating that an **unsigned SPL image** has been executed. 
Host events can be inspected by running U-Boot's ``hab_status`` command.

.. important::
   
	 Once the security fuses have been programmed, modify all your UUU scripts to use only **signed SPL** images.
	 Some of those scripts might depend on the occurrence of HABv4 events.
	 This is already covered in our :ref:`ref-secure-machines` implementations.

To secure the platform, there is an extra fuse that needs to be programmed.
We will only take this step once we are sure that we can successfully sign and boot a signed SPL image with a matching set of keys (containing the same public key hashes as those stored in the SRK fuses).

How to Sign an SPL Image
------------------------

.. note::
   
	 We provide a ``readme.md`` file with straight forward instructions on signing the SPL and mfgtool/SDP SPL for each board in our :ref:`ref-secure-machines` implementations.
	 This is part of the ``mfgtool-files`` artifact for the secure machines.

To build a signed image, you need to create a Command Sequence File (CSF) describing all the commands that the ROM will execute during Secure Boot.
These commands instruct HABv4 on which memory areas to authenticate, which keys to install and use, what data to write to a register, and so on.
In addition, the necessary certificates and signatures involved in the verification of the image are attached to the CSF generated binary output.

We keep a template at ``lmp-tools/security/imx_hab4/u-boot-spl-sign.csf-template``.

This template is used by ``lmp-tools/security/imx_hab4/sign-file.sh`` script which dynamically generates the authenticate data command "blocks" line(s) based on your binary.  The command "blocks" line contains three values:

* The first value is the address on the target where HAB expects the signed image data to begin.
* The second value is the offset into the file where CST will begin signing.
* The third value is length in bytes of the data to sign starting from the offset.


It is also required that the IVT and DCD regions are signed. HAB will verify the DCD and IVT fall in an authenticated region: The CSF will not successfully authenticate unless all commands are successful and all required regions are signed.

In the case of the SPL, you must enable **CONFIG_IMX_HAB** to include the IVT and DCD information.

The ``lmp-tools/security/imx_hab4/sign-file.sh`` script executes NXP's Code Signing Tool after preparing the CSF information based on the template::

	$ cd security/imx_hab4/
	$ ./sign-file.sh --cst ./cst --spl SPL

	SETTINGS FOR  : ./sign-file.sh
	--------------:
	CST BINARY    : ./cst
	CSF TEMPLATE  : u-boot-spl-sign.csf-template
	BINARY FILE   : SPL
	KEYS DIRECTORY: .
	FIX-SDP-DCD   : no

	FOUND HAB Blocks 0x2f010400 0x00000000 0x00018c00
	CSF Processed successfully and signed data available in SPL_csf.bin
	$ ls SPL.signed
	SPL.signed

All intermediate files generated during the signing process are removed by the script.

Booting this signed SPL image and inspecting the HAB status should give no HAB events therefore indicating that the image was correctly signed::

	=> hab_status
	Secure boot disabled
	HAB Configuration: 0xf0, HAB State: 0x66
	No HAB Events Found!

.. warning::
   The next fuse instruction will close the board for unsigned images: make sure you can rebuild the signed images before programming that fuse.


Now we can close the device — From here on only signed images can be booted on the platform.

	=> fuse prog 29 6 0x80000000

For i.MX 8MM you have to fuse bit25 of word 3 from bank 1 (SEC_CONFIG[1] in the documentation)::

        => fuse prog 1 3 0x2000000


Rebooting the board and checking the HAB status should give::

	=> hab_status
	Secure boot enabled
	HAB Configuration: 0xcc, HAB State: 0x99
	No HAB Events Found!

.. warning::
   A production device should also "lock" the SRK values to prevent bricking a closed device.  Refer to the Security Reference Manual for the location and values of these fuses.


How to Sign an SPL Image for SDP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Once the device has been closed, only signed images will be able to run on the processor: this means that injections via UUU/SDP will stop working unless the SPL it uses is properly signed.

1. On i.MX 6UL/6ULL families, the SDP imposes the following restrictions:

* SDP requires that the CSF is modified to include a check for the DCD table
* SDP requires that the DCD address of the image is cleared from the header

To comply with these requirements we need to sign the image adding the ``--fix-sdp-dcd`` parameter::

	$ cd security/imx_hab4/
	$ ./sign-file.sh --cst ./cst --spl SPL --fix-sdp-dcd

	SETTINGS FOR  : ./sign-file.sh
	--------------:
	CST BINARY    : ./cst
	CSF TEMPLATE  : u-boot-spl-sign.csf-template
	BINARY FILE   : SPL
	KEYS DIRECTORY: .
	FIX-SDP-DCD   : yes

	4+0 records in
	4+0 records out
	4 bytes copied, 8.3445e-05 s, 47.9 kB/s
	4+0 records in
	4+0 records out
	4 bytes copied, 6.6832e-05 s, 59.9 kB/s
	FOUND DCD Blocks 0x2f010000 0x0000002c 0x00000258
	FOUND HAB Blocks 0x2f010400 0x00000000 0x00021c00
	CSF Processed successfully and signed data available in SPL_csf.bin
	$ ls SPL.signed
	SPL.signed

2. On i.MX 8M and i.MX 6 families, using the ``--fix-sdp-dcd`` parameter is not required.


.. note::
   Which SoCs fall in which category can be identified by inspecting the `Universal Update Utility`_  g_RomInfo.
	 If the option ``ROM_INFO_HID_SKIP_DCD`` is configured, then the DCD does **not** need to be fixed for that SoC.


Booting Signed Images With the `Universal Update Utility`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
   These steps are covered in our mfgtool implementation of :ref:`ref-secure-machines`.

1. For i.MX 6UL/6ULL, we need to let SDP know the DCD location, as well as inform it that the DCD has been cleared.
A typical UUU boot script would be (replace ``@@MACHINE@@`` with your machine configuration name):

.. code-block:: console
   :emphasize-lines: 3

   uuu_version 1.0.1

   SDP: boot -f SPL.signed-@@MACHINE@@ -dcdaddr 0x2f010000 -cleardcd

   SDPU: delay 1000
   SDPU: write -f u-boot-@@MACHINE@@.itb

2) On i.MX 8M and i.MX 6 families — those where SDP does not impose DCD restrictions — the UUU boot script will look like:

.. code-block:: console

   uuu_version 1.0.1

   SDP: boot -f SPL.signed-@@MACHINE@@

   SDPU: delay 1000
   SDPU: write -f u-boot-@@MACHINE@@.itb

In both cases, if the device has been closed and is only accepting signed images, **it is recommended that UUU be started before powering the board, and before connecting it to the host PC, so that UUU polls for the connection and responds to it as soon as possible**.
To that effect we need to make sure of UUU's polling period flag::

	$ uuu -pp 1 file.uuu

.. note::

	 The flags `-dcdaddr`_, `-cleardcd`_, and `-pp`_ are required for SDP on older SoCs.
	 These have  been contributed to the Universal Update Utility by Foundries.io.
	 Make sure your UUU version is up-to-date with these changes.

Booting a Closed System With a CAAM Device
------------------------------------------

If you are running with a *Cryptographic Acceleration and Assurance Module* device, notice that in the closed configuration—and for devices with HAB 4.4.0 (or lower)—the HAB code locks the job ring and DECO master ID registers.

If the user-specific application requires any changes in the CAAM MID registers, it is necessary to add the “Unlock CAAM MID” command into the CSF file.
Not doing so, since the CAAM will not have been configured for the proper MIDs, leaves some of the CAAM registers not accessible for writing.
Thus, any attempt to write to them will cause system **core fails**.

.. note::
	 The current NXP BSP implementation expects the CAAM registers to be unlocked when configuring the CAAM to operate in the non-secure TrustZone world.
	 This applies when OP-TEE is enabled on the i.MX 6 processor.

Our ``u-boot-spl-sign.csf-template`` takes care of supporting CAAM on closed platforms by adding the following section::

	[Authenticate CSF]

	[Unlock]
	Engine = CAAM
	Features = MID, RNG

.. seealso::
   * :ref:`ref-boot-software-updates-imx`

.. _Secure Boot Using HABv4 Guide:
   https://www.nxp.com/webapp/Download?colCode=AN4581&location=null

.. _Universal Update Utility:
   https://github.com/nxp-imx/mfgtools

.. _-dcdaddr:
   https://github.com/nxp-imx/mfgtools/commit/003b6cb7a98ba36d78d591b5c1ef8e42423f1b90
.. _-cleardcd:
   https://github.com/nxp-imx/mfgtools/commit/a3e9f5b84d28666d53f565abecf59996b7810aca

.. _-pp:
   https://github.com/nxp-imx/mfgtools/commit/5a790eae0a0f424e145171681e1a3a4f3fa47904

.. _lmp-tools/security/imx_hab4:
   https://github.com/foundriesio/lmp-tools/tree/master/security/imx_hab4
