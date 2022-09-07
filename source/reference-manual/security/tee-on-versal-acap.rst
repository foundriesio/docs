.. highlight:: sh

.. _ref-tee-on-versal-acap:


OP-TEE on the Versal Adaptive Compute Acceleration Platform
===========================================================

A Trusted Execution Environment (TEE) is the security architecture cornerstone for the ARM® platforms that we support at Foundries.io; this is the reason why as part of the partnership agreements between Foundries.io and AMD/Xilinx, we brought `OP-TEE support`_ to the Versal™  Adaptive Compute Acceleration Platform (ACAP) platform.

Among the many features included (TRNG, eFUSE access, GPIO controls, secure storage, etc), Versal ACAP users are able to use hardware supported cryptographic operations from the ARM Trusted Zone.

.. _overview :

Overview
********

The OP-TEE support for the `Versal ACAP`_ delegates most of its functionality to the `PLM firmware`_ executing in the MicroBlaze™ processor.
In the case of cryptographic operations, ciphers, and keys not supported by the hardware will be routed to the `Libtomcrypt`_ software based implementation.

The services offered by PLM firmware are decided at build time: it is therefore important that the PLM firmware build configuration enables the services that OP-TEE will require.

As an example, if OP-TEE is configured to generate a hardware unique key, it will need access to the PLM Physical Unclonable Function and NVM services.

.. note::
   Communication between OP-TEE and the PLM uses the IPI mailbox controller being the IPI used selectable via ``CFG_VERSAL_MBOX_IPI_ID``.

As described in freely available documentation for the Versal ACAP `boot-flow`_, the BootROM handles loading the PLM, while the PLM will handle loading the rest of the images including OP-TEE.

A reference BIF file supporting an OP-TEE instance capable of loading the FPGA pdi can be seen below. In this example OP-TEE should be configured with ``CFG_DT=y`` and ``CFG_DT_ADDR=0x00001000``.
If enabled the platform expects the FPGA bitstream at 0x40000000; the location is configurable using ``CFG_VERSAL_FPGA_DDR_ADDR``.

.. code-block:: none

	ROM_image:
	{
		image {
                      { type=bootimage, file=vpl_gen_fixed.pdi }
	              { type=bootloader, file=plm.elf }
	              { core=psm, file=psmfw.elf }
	        }
	        image {
	              id = 0x1c000000, name=apu_subsystem
	              { type=raw, load=0x00001000, file=versal-vck190-revA-x-ebm-01-revA.dtb }
	              { type=raw, load=0x40000000, file=fpga.pdi }
	              { core=a72-0, exception_level=el-3, trustzone, file=bl31.elf }
 	              { core=a72-0, exception_level=el-2, file=u-boot.elf }
	              { core=a72-0, exception_level=el-1, trustzone, load=0x60000000, startup=0x60000000, file=tee-raw.bin }
	         }
         }


To build the boot-able image AMD/Xilinx uses the `bootgen tool`_; this tool aggregates all the different images in a single binary.

The available configuration options depend on the architecture.

In the case of Versal ACAP using the previously mentioned BIF file, the BOOT.BIN generation would be as follows:

.. code-block:: none

        $ bootgen -arch versal -image file.bif -o BOOT.BIN


Cryptographic driver
********************

The Versal ACAP cryptography driver rests on the PLM's `xilsecure`_ service.
It provides hardware assisted support for:

    1. SHA3-384
    2. RSA 2048, 4096
    3. ECC sign/verify
    4. AES-GCM

Other drivers
*************

The ``Versal ACAP eFUSE`` driver uses the PLM `xilnvm`_ service.
Access to certain eFuses require specific PLM configuration flags not selectable at run-time.

.. note::
   It is therefore left down to the user to make sure that the PLM has been configured as expected.

The ``Versal ACAP PUF`` driver uses the PLM `xilpuf`_ service.

At the time of this writing, the platform support includes three native drivers:

    1. ``Mailbox driver``
    2. ``TRNG driver``
    3. ``GPIO driver``


Hardware Unique Key
*******************

The calculation of the Hardware Unique Key - used to derive the RPMB secret - is similar to the Zynqmp platform: a digest is generated from the DNA eFUSE identifier and then GCM-AES encrypted.
The symmetric key for the AES-GCM encryption engine can however be selected at build time using the configuration option ``CFG_VERSAL_HUK_KEY``.

Contrary to what happens in the Zynqmp platform, the PUF KEK is available also on non-secured boards (i.e: boards not booting signed images).

This means that the driver has no mechanism for restricting the generation of the HUK to using data based on information ``only available`` to secured systems.

.. note::
   The security of the platform will depend on the process used to generate and lock the keys.

Effectively Working with the boot firmware
******************************************

One of the features that make the `Versal AI Core Series VCK190 Evaluation Kit`_ a friendly platform to develop on is its integrated JTAG support: a single USB cable provides the different consoles as well as the JTAG port

At Foundries.io and via the FoundriesFactory CI, we build and deliver a WIC image that allows Versal ACAP platforms to boot securely.
This way an average user could just flash the WIC image on a uSD card, plug it in the corresponding slot and boot to a secured functional system.

But we also deliver all the individual components that form the different binaries as well as the pointers to the corresponding git trees and versions.

Now lets imagine that Xilinx/AMD releases a new version of the PLM firmware; this firmware controls the actual cryptographic operations requested by OP-TEE.

Without having to rebuild the complete WIC image, the developer could just update and rebuild OP-TEE and PLM and include these new binaries in the BOOT.BIN image using the BIF file previously mentioned; then it would use the Xilinx Software Command Line Tool (xsct) to boot it.

.. code-block:: none

        $ xsct load_boot_bin.tcl


Te xsct script would look like follows:

.. code-block:: none

        $ cat load_boot_bin.tcl

	connect
	after 1000
	target 1
	rst
	targets -set -nocase -filter {name =~ "*Versal*"}
	device program "/path/to/BOOT.BIN"


Execution of that command would boot to the U-boot shell.
The beauty of it is that we didnt need to modify U-boot. And so, if the uSD card was plugged with a FoundriesFactory LmP image, the Linux kernel would continue booting to the final shell from which the developer could validate the new PLM/OP-TEE features.

.. code-block:: none

      [0.015]****************************************
      [0.072]Xilinx Versal Platform Loader and Manager
      [0.131]Release 2022.1   Apr 11 2022  -  09:29:50
      [0.190]Platform Version: v2.0 PMC: v2.0, PS: v2.0
      [0.256]BOOTMODE: 0x0, MULTIBOOT: 0x0
      [0.310]****************************************
      [0.541]Non Secure Boot
      [3.487]PLM Initialization Time
      [3.537]***********Boot PDI Load: Started***********
      [3.600]Loading PDI from SBI
      [3.649]Monolithic/Master Device
      [4.153]0.527 ms: PDI initialization time
      [4.211]+++Loading Image#: 0x1, Name: lpd, Id: 0x04210002
      [4.280]---Loading Partition#: 0x1, Id: 0xC
      [55.514] 51.147 ms for Partition#: 0x1, Size: 2880 Bytes
      [60.374]---Loading Partition#: 0x2, Id: 0x0
      [64.757] 0.516 ms for Partition#: 0x2, Size: 48 Bytes
      [68.908]---Loading Partition#: 0x3, Id: 0x0
      [107.863] 35.087 ms for Partition#: 0x3, Size: 58912 Bytes
      [110.190]---Loading Partition#: 0x4, Id: 0x0
      [115.764] 1.620 ms for Partition#: 0x4, Size: 5888 Bytes
      PSM Firmware version: 2022.1 [Build: Apr 11 2022 09:29:50 ]
      [124.377]+++Loading Image#: 0x2, Name: pl_cfi, Id: 0x18700000
      [129.731]---Loading Partition#: 0x5, Id: 0x3
      [955.552] 821.867 ms for Partition#: 0x5, Size: 1258736 Bytes
      [958.137]---Loading Partition#: 0x6, Id: 0x5
      [1847.061] 884.970 ms for Partition#: 0x6, Size: 1335632 Bytes
      [1849.762]+++Loading Image#: 0x3, Name: aie_subsys, Id: 0x0421C005
      [1855.536]---Loading Partition#: 0x7, Id: 0x7
      [1862.473] 2.897 ms for Partition#: 0x7, Size: 864 Bytes
      [1864.660]+++Loading Image#: 0x4, Name: fpd, Id: 0x0420C003
      [1869.838]---Loading Partition#: 0x8, Id: 0x8
      [1874.286] 0.410 ms for Partition#: 0x8, Size: 1552 Bytes
      [1879.189]+++Loading Image#: 0x5, Name: apu_subsystem, Id: 0x1C000000
      [1884.947]---Loading Partition#: 0x9, Id: 0x0
      [1900.269] 11.283 ms for Partition#: 0x9, Size: 23296 Bytes
      [1902.684]---Loading Partition#: 0xA, Id: 0x0
      [2358.623] 451.899 ms for Partition#: 0xA, Size: 707616 Bytes
      [2361.208]---Loading Partition#: 0xB, Id: 0x0
      [2405.954] 40.707 ms for Partition#: 0xB, Size: 67536 Bytes
      [2408.370]---Loading Partition#: 0xC, Id: 0x0
      [3482.773] 1070.362 ms for Partition#: 0xC, Size: 1647504 Bytes
      [3485.532]---Loading Partition#: 0xD, Id: 0x0
      [3778.339] 288.766 ms for Partition#: 0xD, Size: 452640 Bytes

      NOTICE:  BL31: v2.4(debug):xlnx_rebase_v2.4_2021.1_update1-24-g7174d24f7-dirty
      NOTICE:  BL31: Built : 11:17:24, Aug 31 2022
      INFO:    GICv3 with legacy support detected.
      INFO:    ARM GICv3 driver initialized in EL3
      INFO:    BL31: Initializing runtime services
      INFO:    setting up optee service..
      WARNING: BL31: cortex_a72: CPU workaround for 859971 was missing!
      WARNING: BL31: cortex_a72: CPU workaround for 1319367 was missing!
      INFO:    BL31: cortex_a72: CPU workaround for cve_2017_5715 was applied
      INFO:    BL31: cortex_a72: CPU workaround for cve_2018_3639 was applied
      INFO:    BL31: Initializing BL32
      INFO:    executing opteed_init I/TC:

      I/TC: Non-secure external DT found
      I/TC: pl011: device parameters ignored (115200)
      I/TC: Switching console to device: /axi/serial@ff000000
      I/TC: OP-TEE version: 3.18.0-93-gf893d5703-dev (gcc version 7.3.1 20180425 [linaro-7.3-2018.05 revision d29120a424ecfbc167ef90065c0eeb7f91977701] (Linaro GCC 7.3-2018.05)) #1 Fri Sep  2 13:59:25 UTC 2022 aarch64
      I/TC: WARNING: This OP-TEE configuration might be insecure!
      I/TC: WARNING: Please check https://optee.readthedocs.io/en/latest/architecture/porting_guidelines.html
      I/TC: Primary CPU initializing
      I/TC: Platform Versal:  Silicon Revision v2
      I/TC: Hardware Root of Trust: Asymmetric NOT Enabled, Symmetric NOT Enabled
      I/TC: Using Development HUK
      I/TC: Primary CPU switching to normal world boot
      INFO:    BL31: Preparing for EL3 exit to normal world
      INFO:    Entry point address = 0x8000000
      INFO:    SPSR = 0x3c9

      U-Boot 2022.01-17188-g3334d79c23-dirty (Jul 21 2022 - 11:50:46 +0200)
      CPU:   Versal
      Silicon: v2
      Model: Xilinx Versal vck190 Eval board revA (QSPI)
      DRAM:  8 GiB
      EL Level:       EL2
      MMC:   mmc@f1050000: 0
      Loading Environment from nowhere... OK
      In:    serial@ff000000
      Out:   serial@ff000000
      Err:   serial@ff000000
      Bootmode: JTAG_MODE
      Net:

      [...]
      Hit any key to stop autoboot:  0

      2055 bytes read in 13 ms (154.3 KiB/s)
      ## Executing script at 20000000
      sha256+ 566 bytes read in 22 ms (24.4 KiB/s)
      14889652 bytes read in 1015 ms (14 MiB/s)
      ## Loading kernel from FIT Image at 10000000 ...
	  Using 'conf-system-top.dtb' configuration
	  Verifying Hash Integrity ... OK
	  Trying 'kernel-1' kernel subimage
	    Description:  Linux kernel
	    Type:         Kernel Image
	    Compression:  gzip compressed
	    Data Start:   0x10000110
	    Data Size:    9252712 Bytes = 8.8 MiB
	    Architecture: AArch64
	    OS:           Linux
	    Load Address: 0x18000000
	    Entry Point:  0x18000000
	    Hash algo:    sha256
	    Hash value:   a83cc2eacc021dc6f84c481f6ca8238ed755c702b20f5c3c3dd1e8a31b6cb2f0
	  Verifying Hash Integrity ... sha256+ OK
      ## Loading ramdisk from FIT Image at 10000000 ...
	  Using 'conf-system-top.dtb' configuration
	  Verifying Hash Integrity ... OK
	  Trying 'ramdisk-1' ramdisk subimage
	    Description:  initramfs-ostree-lmp-image-vck190-versal
	    Type:         RAMDisk Image
	    Compression:  uncompressed
	    Data Start:   0x108db168
	    Data Size:    5602258 Bytes = 5.3 MiB
	    Architecture: AArch64
	    OS:           Linux
	    Load Address: unavailable
	    Entry Point:  unavailable
	    Hash algo:    sha256
	    Hash value:   6d6f902bb14fc30faee41ab9dc8821a57e6ebfbccd8b0781d7d964bc0f7630a5
	  Verifying Hash Integrity ... sha256+ OK
      ## Loading fdt from FIT Image at 10000000 ...
	  Using 'conf-system-top.dtb' configuration
	  Verifying Hash Integrity ... OK
	  Trying 'fdt-system-top.dtb' fdt subimage
	    Description:  Flattened Device Tree blob
	    Type:         Flat Device Tree
	    Compression:  uncompressed
	    Data Start:   0x108d3188
	    Data Size:    32506 Bytes = 31.7 KiB
	    Architecture: AArch64
	    Hash algo:    sha256
	    Hash value:   3a2720ff2aa10e889ee2ff6a419fdf69c3b031e08135ad3800b7ddc6d9df445c
	  Verifying Hash Integrity ... sha256+ OK
	  Booting using the fdt blob at 0x108d3188
	  Uncompressing Kernel Image
	  Loading Ramdisk to 7d972000, end 7dec9bd2 ... OK
	  Loading Device Tree to 000000007d967000, end 000000007d971ef9 ... OK

      Starting kernel ...

      [    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd083]
      [    0.000000] Linux version 5.15.64-lmp-standard (oe-user@oe-host) (aarch64-lmp-linux-gcc (GCC) 11.3.0, GNU ld (GNU Binutils) 2.38.20220708) #1 SMP Thu Sep 1 02:40:19 UTC 2022
      [    0.000000] Machine model: Xilinx Versal vck190 Eval board revA (QSPI)
      [    0.000000] earlycon: pl11 at MMIO32 0x00000000ff000000 (options '115200n8')
      [    0.000000] printk: bootconsole [pl11] enabled
      [    0.000000] efi: UEFI not found.
      [    0.000000] Zone ranges:
      [    0.000000]   DMA32    [mem 0x0000000000000000-0x00000000ffffffff]
      [    0.000000]   Normal   [mem 0x0000000100000000-0x000000097fffffff]
      [    0.000000] Movable zone start for each node
      [    0.000000] Early memory node ranges
      [    0.000000]   node   0: [mem 0x0000000000000000-0x000000005fffffff]
      [    0.000000]   node   0: [mem 0x0000000060000000-0x000000006fffffff]
      [    0.000000]   node   0: [mem 0x0000000070000000-0x000000007fffffff]
      [    0.000000]   node   0: [mem 0x0000000800000000-0x000000097fffffff]
      [    0.000000] Initmem setup node 0 [mem 0x0000000000000000-0x000000097fffffff]
      [    0.000000] cma: Reserved 256 MiB at 0x0000000050000000
      [    0.000000] psci: probing for conduit method from DT.
      [    0.000000] psci: PSCIv1.1 detected in firmware.
      [    0.000000] psci: Using standard PSCI v0.2 function IDs

      [...]

      [   12.287689] macb ff0c0000.ethernet eth0: PHY [ff0c0000.ethernet-ffffffff:01] driver [TI DP83867] (irq=POLL)                                                                                                                                                                           
      [   12.297444] macb ff0c0000.ethernet eth0: configuring for phy/rgmii-id link mode
      [   12.313947] pps pps0: new PPS source ptp0
      [   12.318721] macb ff0c0000.ethernet: gem-ptp-timer ptp clock registered.
      [  OK  ] Started containerd container runtime.
      [   17.439954] macb ff0c0000.ethernet eth0: Link is Up - 1Gbps/Full - flow control tx
      [   17.454684] IPv6: ADDRCONF(NETDEV_CHANGE): eth0: link becomes ready

      Linux-microPlatform 4.0.3-1721-77-506-g22e6cd6 vck190-versal -
      vck190-versal login:


      
.. _boot-flow:
    https://docs.xilinx.com/r/en-US/ug1304-versal-acap-ssdg/Boot-Flow

.. _bootgen tool:
  https://github.com/Xilinx/bootgen

.. _Libtomcrypt:
   https://optee.readthedocs.io/en/latest/architecture/crypto.html?highlight=libtomcrypt#libtomcrypt

.. _OP-TEE support:
   https://github.com/OP-TEE/optee_os/pull/5426

.. _PLM firmware:
   https://github.com/Xilinx/embeddedsw

.. _Versal ACAP:
   https://www.xilinx.com/products/silicon-devices/acap/versal.html

.. _Versal AI Core Series VCK190 Evaluation Kit:
   https://www.xilinx.com/products/boards-and-kits/vck190.html

.. _xilnvm:
   https://github.com/Xilinx/embeddedsw/tree/master/lib/sw_services/xilnvm

.. _xilpuf:
   https://github.com/Xilinx/embeddedsw/tree/master/lib/sw_services/xilpuf

.. _xilsecure:
   https://github.com/Xilinx/embeddedsw/tree/master/lib/sw_services/xilsecure



