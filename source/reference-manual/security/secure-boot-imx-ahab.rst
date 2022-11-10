.. highlight:: sh

.. _ref-secure-boot-imx-ahab:

Secure Boot on i.MX 8/8X Families using AHAB including 8QM
==========================================================

The i.MX8 and i.MX8x family of applications processors introduce a secure boot concept  which differs
from HABv4.  Due to the multi-core architecture the Security Controller (SECO) and System Control Unit (SCU)
are heavily involved in the secure boot process, comparing to HABv4, where BootROM (running on A-core) is fully
responsible for that.

AHAB Architecture Overview
--------------------------

The Advanced High Assurance Boot (AHAB) feature as well as HABv4 relies on digital signatures to prevent
unauthorized software execution during the device boot sequence.

In i.MX8 and i.MX8x families the System Control Unit (SCU) is responsible to interface with the boot media, managing
the process of loading the firmware and software images in different partitions of the SoC. The Security Controller (SECO)
is responsible to authenticate the images and authorize the execution of them.

How to Secure the Platform
--------------------------

The first step is to generate the PKI tree and commit the fuse table to the hardware.

 .. warning::

   Once the fuses have been programmed they can't be modified.

Please refer to NXP's `AN12312 Secure Boot on i.MX 8 and i.MX 8X Families using AHAB – Application Note`_ for a detailed
description on how to generate the PKI tree.

For development purposes, we keep i.MX AHAB sample keys and certificates at ``lmp-tools/security/imx_ahab``. The fuse table
can be inspected by executing the ``print_fuses`` script in that same directory. The output should be::

	0x7E90F8D6
	0xE1020512
	0x4FF77EB2
	0x1D964702
	0x5ED61C06
	0x14139AB9
	0x0A57872C
	0xF367F432
	0xE8153815
	0xA804967A
	0xDC14638B
	0xB3A914F7
	0x211FD529
	0x8273EBD2
	0x6E0B791C
	0x6A558134

The Security Reference Manual for your specific SoC indicates which fuses need to be programed with the SRK fuse information.

i.MX8QM fusing
--------------------------

On the i.MX8QM SoC fuses are stored in fuse bank 0, words 722 to 737::

        => fuse prog -y 0 722 0x7E90F8D6
        => fuse prog -y 0 723 0xE1020512
        => fuse prog -y 0 724 0x4FF77EB2
        => fuse prog -y 0 725 0x1D964702
        => fuse prog -y 0 726 0x5ED61C06
        => fuse prog -y 0 727 0x14139AB9
        => fuse prog -y 0 728 0x0A57872C
        => fuse prog -y 0 729 0xF367F432
        => fuse prog -y 0 730 0xE8153815
        => fuse prog -y 0 731 0xA804967A
        => fuse prog -y 0 732 0xDC14638B
        => fuse prog -y 0 733 0xB3A914F7
        => fuse prog -y 0 734 0x211FD529
        => fuse prog -y 0 735 0x8273EBD2
        => fuse prog -y 0 736 0x6E0B791C
        => fuse prog -y 0 737 0x6A558134

Alternatively, use the kernel to program SoC fuses using SDP via NXP's Universal Update Utility with a script as follows::

        uuu_version 1.3.102

        SDPS: boot -f imx-boot-mfgtool.signed
        CFG: FB: -vid 0x0525 -pid 0x4000
        CFG: FB: -vid 0x0525 -pid 0x4025
        CFG: FB: -vid 0x0525 -pid 0x402F
        CFG: FB: -vid 0x0525 -pid 0x4030
        CFG: FB: -vid 0x0525 -pid 0x4031

        SDPU: delay 1000
        SDPU: write -f u-boot-mfgtool.itb
        SDPU: jump

        # These commands will be run when use SPL and will be skipped if no spl
        # if (SPL support SDPV)
        # {
        SDPV: delay 1000
        SDPV: write -f u-boot-mfgtool.itb
        SDPV: jump
        # }

        FB: ucmd fuse prog -y 0 722 0x7E90F8D6
        FB: ucmd fuse prog -y 0 723 0xE1020512
        FB: ucmd fuse prog -y 0 724 0x4FF77EB2
        FB: ucmd fuse prog -y 0 725 0x1D964702
        FB: ucmd fuse prog -y 0 726 0x5ED61C06
        FB: ucmd fuse prog -y 0 727 0x14139AB9
        FB: ucmd fuse prog -y 0 728 0x0A57872C
        FB: ucmd fuse prog -y 0 729 0xF367F432
        FB: ucmd fuse prog -y 0 730 0xE8153815
        FB: ucmd fuse prog -y 0 731 0xA804967A
        FB: ucmd fuse prog -y 0 732 0xDC14638B
        FB: ucmd fuse prog -y 0 733 0xB3A914F7
        FB: ucmd fuse prog -y 0 734 0x211FD529
        FB: ucmd fuse prog -y 0 735 0x8273EBD2
        FB: ucmd fuse prog -y 0 736 0x6E0B791C
        FB: ucmd fuse prog -y 0 737 0x6A558134

        FB: acmd reset
        FB: done

Upon reboot, if **CONFIG_AHAB_BOOT** is set AHAB will raise events to indicate that an **unsigned imx-boot image** has been executed. Those events can be inspected by running U-Boot's command ``ahab_status`` for i.MX8/i.MX8x::

    => ahab_status
    Lifecycle: 0x0020, NXP closed

    SECO Event[0] = 0x0087EE00
            CMD = AHAB_AUTH_CONTAINER_REQ (0x87)
            IND = AHAB_NO_AUTHENTICATION_IND (0xEE)

To secure the platform, there is an extra step that needs to be done: we will only take that step once we are sure that we can successfully sign and boot a signed boot image with a matching set of keys (containing the same public key hashes as those stored in the SRK fuses).

How to sign an i.MX boot image
------------------------------

To build a signed image, you need to create a Command Sequence File - CSF - describing the commands that the CSU executes during secure boot. These commands instruct AHAB on which memory areas of the image to authenticate, which keys to install and use, what data to write to a register and so on. In addition, the necessary certificates and signatures involved in the verification of the image are attached to the CSF generated binary output.

We keep a template at ``lmp-tools/security/imx_ahab/u-boot-spl-sign.csf-template``.

This template is used by the ``lmp-tools/security/imx_ahab/sign-file.sh`` script which dynamically generates the authenticate data command "Offsets" line based on imx-boot image.  The command "Offset" line contains two values:

* Container header - offset to header of container, which contains set of binary images that should be signed
* Signature block - offset to the signature block header

.. note::
    Once the security fuses have been programmed, we recommend that all your UUU scripts are modified to use only **signed imx-boot** images since some of those scripts might depend on the occurrence - or not - of AHAB events.

The ``lmp-tools/security/imx_ahab/sign-file.sh`` script executes NXP's Code Signing Tool after preparing the CSF information based on the template::

    $ cd security/imx_ahab/
    $ ./sign-file.sh --cst ./cst --spl imx-boot-apalis-imx8
    SETTINGS FOR  : ./sign-file.sh
    --------------:
    CST BINARY    : cst
    CSF TEMPLATE  : u-boot-spl-sign.csf-template
    BINARY FILE   : imx-boot-apalis-imx8
    KEYS DIRECTORY: .
    KEYS INDEX    : 1

    Invoking CST to sign the binary
    Process completed successfully and signed file is .imx-boot-apalis-imx8.signed


Booting this signed imx-boot image and inspecting the HAB status should give no HAB events therefore indicating that the image was correctly signed::

    => ahab_status
    Lifecycle: 0x0020, NXP closed

    sc_seco_get_event: idx: 0, res:3
    No SECO Events Found!


.. warning::
    The next fuse instruction will close the board for unsigned images: make sure you can rebuild the signed images before running this command.

How to close board
------------------

.. warning::
    This section describes the manual process of closing a board. It's preferable to use UUU script from the next section, as it's considered to be less error-prone as it contains implicit checks for SRK values.

Now we can close the device meaning that from thereon only signed images can be booted on this platform. For that we should run ``ahab_close``::

	=> ahab_close

Rebooting the board and checking the AHAB status should give lifecycle value ``0x80 OEM closed``.

.. warning::
    A production device should also "lock" the SRK values to prevent bricking a closed device.  Refer to the Security Reference Manual for the location and values of these fuses.

How to close board using UUU script
-----------------------------------

To avoid any mistakes board securing procedure can be automated program using SDP via NXP's Universal Update Utility with a script as follows::

        uuu_version 1.3.102

        SDPS: boot -f imx-boot-mfgtool.signed
        CFG: FB: -vid 0x0525 -pid 0x4000
        CFG: FB: -vid 0x0525 -pid 0x4025
        CFG: FB: -vid 0x0525 -pid 0x402F
        CFG: FB: -vid 0x0525 -pid 0x4030
        CFG: FB: -vid 0x0525 -pid 0x4031

        SDPU: delay 1000
        SDPU: write -f u-boot-mfgtool.itb
        SDPU: jump

        # These commands will be run when use SPL and will be skipped if no spl
        # if (SPL support SDPV)
        # {
        SDPV: delay 1000
        SDPV: write -f u-boot-mfgtool.itb
        SDPV: jump
        # }

        FB: ucmd if mmc dev 0; then setenv fiohab_dev 0; else setenv fiohab_dev 1; fi;

        FB: ucmd setenv srk_0 0x7E90F8D6
        FB: ucmd setenv srk_1 0xE1020512
        FB: ucmd setenv srk_2 0x4FF77EB2
        FB: ucmd setenv srk_3 0x1D964702
        FB: ucmd setenv srk_4 0x5ED61C06
        FB: ucmd setenv srk_5 0x14139AB9
        FB: ucmd setenv srk_6 0x0A57872C
        FB: ucmd setenv srk_7 0xF367F432
        FB: ucmd setenv srk_8 0xE8153815
        FB: ucmd setenv srk_9 0xA804967A
        FB: ucmd setenv srk_10 0xDC14638B
        FB: ucmd setenv srk_11 0xB3A914F7
        FB: ucmd setenv srk_12 0x211FD529
        FB: ucmd setenv srk_13 0x8273EBD2
        FB: ucmd setenv srk_14 0x6E0B791C
        FB: ucmd setenv srk_15 0x6A558134

        FB[-t 1000]: ucmd if fiohab_close; then echo Platform Secured; else echo Error, Can Not Secure the Platform; sleep 2; fi
        FB: acmd reset

        FB: done

U-Boot cmd ``fiohab_close`` will automatically validate that all SRK fuses have correct values and after then will close
the board, otherwise it will print error message.

.. _AN12312 Secure Boot on i.MX 8 and i.MX 8X Families using AHAB – Application Note:
   https://www.nxp.com/docs/en/application-note/AN12312.pdf
