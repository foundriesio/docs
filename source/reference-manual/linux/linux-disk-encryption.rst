.. _howto-linux-disk-encryption:

Disk Encryption Support
=======================

To enhance the security of system deployments before manufacturing
provisions the Targets, LmP takes the approach detailed here.

During the image creation process in CI, LmP uses LUKS to construct a
symmetrically encrypted root file-system. The master key used for
data encryption is locked/unlocked via a passphrase.

Upon the initial boot, during initramfs, the passphrase used for
accessing the master key is discarded and replaced by a cryptographic
key. Since this key is used to protect the master key, it is known as
the Key Encryption Key (KEK).

LmP uses LUKS which uses Systemd to register the new KEK. The KEK is an
RSA 2048 asymmetric key, with the key pair being generated via either a
TPM 2.0 or a PKCS#11 security token. This also ensures the secure
storage of the key information.

By enrolling the KEK this way, the system gains the capability of
unlocking the volume seamlessly, without requiring any user involvement.

Once the KEK has been enrolled, LmP marks the rootfs volume for disk
`re-encryption`_, mounts it and allows the system to continue with the
boot sequence. This is know in LUKS terminology as ``online
re-encryption``.

As part of the regular boot procedure, a systemd service will initiate
the data re-encryption process in the background; this process is
non-blocking and allows the rest of the system to continue initializing.

Upon completion of the re-encryption, the service also creates and
stores a backup of the LUKS2 header. This backup image is stored in the
primary partition and serves as a safeguard, enabling the booting of
systems in cases where their disk headers may have been damaged.

.. note::

  If the system is restarted before the non-blocking re-encryption
  service has finished, the subsequent boot will be **blocked in
  initramfs** until the root file system has been fully encrypted.


Prerequisites
-------------

To ensure that the disk encryption and decryption processes can be
carried out without human intervention, LmP mandates the presence of
either PKCS#11 or TPM 2.0 controlled devices on the target hardware.

Devices controlled via PKCS#11 or TPM 2.0 interfaces can therefore be
utilized to securely store and provide the Key Encryption Key (KEK).

Storing the KEK is achieved through the use of LUKS2 tokens, making use
of either the **systemd-pkcs11** or **systemd-tpm2** plugins (refer to
`systemd-cryptenroll`_ for additional details).


.. figure:: /_static/systemd-luks.png
    :width: 300
    :align: center

    systemd-cryptenroll


In ARM System on Chips (SoCs), a common PKCS#11 scenario is to execute
OP-TEE within the TrustZone. In this setup, OP-TEE should be configured
to use the eMMC Replay Protected Memory Block (RPMB) for secure storage
with tamper-resistant properties.

In TPM 2.0 devices and as a security enhancement, we require that UEFI
boots with secure boot be enabled. This is because the KEK is linked to
the Platform Configuration Register 7 (PCR 7), which monitors the
**secure boot state of the machine**.

We demonstrate both of these scenarios using QEMU in the sections below.


Enabling Support for Disk Encryption
------------------------------------

The following options require customizations for disk encryption support:

For adding the required ``initramfs-module-cryptfs`` module to the initramfs
(based on what gets provided by ``MACHINE_FEATURES``, like ``tpm2`` or ``optee``):

.. code-block:: none

  DISTRO_FEATURES:append = " luks"

For splitting the ``/boot`` content from the ostree deployment in a separated
partition (where kernel/initramfs gets stored, unencrypted). This option is
enabled by default on systems booting with UEFI support.

.. code-block:: none

  OSTREE_SPLIT_BOOT = "1"

For supporting copying content from ``/usr/lib/ostree-boot`` (used for
boot firmware updates) into ``/boot`` as part of the ostree deployment step (OTA).
This is required for supporting boot firmware updates on devices with encrypted
root file systems.

.. code-block:: none

  OSTREE_DEPLOY_USR_OSTREE_BOOT = "1"

For supporting ``/boot`` in a separated partition at the final image the selected
``WKS_FILE`` needs to support split boot. UEFI based devices already have such
setup by default, but on most ARM/ARM64 devices a custom WKS might be
required. As an example, iMX8-based devices should use
``sdimage-imx8-spl-split-boot-sota.wks.in`` instead of the default
``sdimage-imx8-spl-sota.wks.ini`` file:

.. code-block:: none

  WKS_FILE:sota:mx8mm-nxp-bsp = "sdimage-imx8-spl-split-boot-sota.wks.in"

.. note::

  Besides a custom ``WKS_FILE`` for split boot support, make sure to also update
  the target fstab to automatically mount ``/boot`` (from the first partition)
  at the root file system ``/boot`` folder.
  This is not required with UEFI-based systems as systemd is capable of
  automatically identifying and mounting the ESP partition during boot.

Testing TPM 2.0 Support With Qemu (x86) and swtpm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to test the disk encryption support with TPM 2.0 with Qemu and
`swtpm`_.

Make sure LUKS support is enabled for your x86 target:

.. code-block:: console

  $ cat meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc
  DISTRO_FEATURES:append:intel-corei7-64 = " luks"

Then make sure to enroll the :ref:`UEFI Secure Boot Certificates <ref-secure-boot-uefi>`
to enable secure boot support. This is required as the LUKS2 TPM 2.0 token
leverages **PCR 7**, which tracks the secure boot state.

Now install ``swtpm`` in the host machine (if not already installed), and start the ``swtpm``
daemon, which will be later consumed by Qemu and act as the hardware TPM.

.. code-block:: console

   $ mkdir -p /tmp/mytpm
   $ while true; do swtpm socket --tpmstate dir=/tmp/mytpm --ctrl type=unixio,path=/tmp/mytpm/swtpm-sock --tpm2; done;

Run Qemu with the required extra TPM 2.0 related commands:

.. code-block:: console

  $ qemu-system-x86_64 -device virtio-net-pci,netdev=net0,mac=52:54:00:12:35:02 \
      -netdev user,id=net0,hostfwd=tcp::2222-:22 \
      -object rng-random,filename=/dev/urandom,id=rng0 -device virtio-rng-pci,rng=rng0 \
      -drive if=none,id=hd,file=lmp-factory-image-intel-corei7-64.wic,format=raw \
      -device virtio-scsi-pci,id=scsi -device scsi-hd,drive=hd \
      -drive if=pflash,format=qcow2,file=ovmf.secboot.qcow2 -no-reboot \
      -nographic -m 1024 -serial mon:stdio -serial null -cpu host -enable-kvm \
      -chardev socket,id=chrtpm,path=/tmp/mytpm/swtpm-sock \
      -tpmdev emulator,id=tpm0,chardev=chrtpm -device tpm-tis,tpmdev=tpm0

Now during boot you should see the following during the first boot:

.. code-block:: none

  ...
  Starting version 250.5+
  /dev/sda2 not yet encrypted, encrypting with LUKS2
  [    0.699667] e2fsck: otaroot: clean, 15983/934032 files, 447887/933901 blocks
  resize2fs 1.46.5 (30-Dec-2021)
  Resizing the filesystem on /dev/sda2 to 925709 (4k) blocks.
  The filesystem on /dev/sda2 is now 925709 (4k) blocks long.
  Key slot 0 created.
  Finished, time 00:15.011, 3632 MiB written, speed 240.9 MiB/s
  Command successful.
  Enrolling LUKS2 keyslot based on tpm2 token
  New TPM2 token enrolled as key slot 1.
  Wiped slot 0.
  [   44.126792] e2fsck: otaroot: clean, 15983/934032 files, 447887/925709 blocks
  ...

Verify that LUKS2 is using the TPM 2.0 based systemd token for encryption:

.. code-block:: none

  root@intel-corei7-64-unknown:~# cryptsetup luksDump /dev/sda2
  LUKS header information
  Version:        2
  Epoch:          463
  Metadata area:  16384 [bytes]
  Keyslots area:  16744448 [bytes]
  UUID:           af0d8a12-5c60-48d1-9f03-a6165906df30
  Label:          otaroot
  Subsystem:      (no subsystem)
  Flags:          (no flags)

  Data segments:
    0: crypt
          offset: 16777216 [bytes]
          length: (whole device)
          cipher: aes-xts-plain64
          sector: 512 [bytes]

  Keyslots:
    1: luks2
          Key:        512 bits
          Priority:   normal
          Cipher:     aes-xts-plain64
          Cipher key: 512 bits
          PBKDF:      pbkdf2
          Hash:       sha512
          Iterations: 1000
          Salt:       d1 2f 37 48 98 37 32 5a f8 3a 45 29 dd 04 03 43
                      89 d2 ae ed 8e d9 56 2f c1 d0 60 31 12 8e 1d 46
          AF stripes: 4000
          AF hash:    sha512
          Area offset:290816 [bytes]
          Area length:258048 [bytes]
          Digest ID:  0
  Tokens:
    0: systemd-tpm2
          tpm2-pcrs:  7
          tpm2-bank:  sha256
          tpm2-primary-alg:  ecc
          tpm2-blob:  00 9e 00 20 7f 2c f2 d0 ec 9b 17 a3 7e 48 90 bf
                      74 1f 43 92 2e d3 45 6d b4 1d 06 6a b8 4c 65 3f
                      54 64 b6 75 00 10 09 ee 39 3c ce 2a 6f cc b1 1e
                      f9 e7 50 e2 1b ce 6c 6d 26 1e 2a 39 24 01 e8 39
                      7b 44 90 62 a2 b9 6b 81 7a 43 9e 76 93 0c 39 d6
                      76 47 85 67 d8 bc 07 4c 68 b1 43 b8 25 58 ed 97
                      c7 0f 00 a7 33 43 2d b2 8b e1 94 da ac 80 19 03
                      1e 06 be 03 7a d5 28 a6 26 cf b5 db f9 63 ee 2a
                      bb 40 9f b0 b6 08 64 6b 3a 5f b1 31 c0 e9 62 12
                      17 fc e8 b6 48 94 d0 80 9e f1 5f d3 9a 85 14 0f
                      00 4e 00 08 00 0b 00 00 00 12 00 20 86 0e d1 f6
                      e3 49 84 56 16 f1 4e cb cd 56 76 b6 97 0e d2 48
                      4b 96 c9 af ee 27 a4 f2 de ce 48 84 00 10 00 20
                      34 85 f5 a4 b1 a4 ca 83 c7 ff ab aa 55 46 a7 4d
                      89 8b 55 4a 82 36 4a 1d 77 36 3e b7 50 8c 81 4f
          tpm2-policy-hash:
                      86 0e d1 f6 e3 49 84 56 16 f1 4e cb cd 56 76 b6
                      97 0e d2 48 4b 96 c9 af ee 27 a4 f2 de ce 48 84
          Keyslot:    1
  Digests:
    0: pbkdf2
          Hash:       sha256
          Iterations: 312076
          Salt:       6c 91 b1 65 23 2f 70 0d 36 ba 42 cc 3e 97 33 e1
                      73 48 b4 84 d7 32 7d 1b 81 a5 ed fd 7c 5e 06 4c
          Digest:     5c 30 5b f3 59 db fe 6a 71 c4 9a a0 2d 22 cf 6b
                      18 e7 cc 8d 6a 44 c9 67 97 f8 34 80 96 69 53 7b

.. note::

   As long as the TPM 2.0 emulation storage is not deleted, you will be
   able to reboot your QEMU image since the key will persist.


Implementation Details for OP-TEE PKCS#11 Support
-------------------------------------------------

To prevent conflicts with the PKCS#11 token slot utilized by
``aktualizr-lite``, a dedicated slot is necessary.

LmP will set this dedicated slot as **slot 1** with the label ``lmp``.

Before initiating the re-encryption process, the slot is initialized,
and a new **RSA 2048** key is generated. This key never leaves the
PKCS#11 domain.

It is important to emphasize that only the **encrypted master key** is
stored in the LUKS JSON token header area.

Please ensure that you **DO NOT** erase the PKCS#11 token slot or its key
throughout the lifespan of your product. Failure to follow this
precaution will result in the system's inability to boot.

In the event of such a scenario, a recovery key can be created and
provided manually, but it won't support an unattended boot process.


Testing PKCS#11 Support With Qemu (arm64)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure LUKS support is enabled for your ``qemuarm64-secureboot`` target:

.. code-block:: console

  $ cat meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc
  DISTRO_FEATURES:append:qemuarm64-secureboot = " luks"


When running QEMU, please be cautious not to exceed 2GB of memory usage,
as attempting to use more than 2GB of memory may prevent the OP-TEE
emulation from successfully booting. So, it's advisable to stay within
this memory limit.

.. code-block:: console

  $ qemu-system-aarch64 -m 2048 -cpu cortex-a57 -no-acpi -bios flash.bin \
      -device virtio-net-device,netdev=net0,mac=52:54:00:12:35:02 -device virtio-serial-device \
      -drive id=disk0,file=lmp-console-image-qemuarm64-secureboot.wic,if=none,format=raw \
      -device virtio-blk-device,drive=disk0 -netdev user,id=net0,hostfwd=tcp::2222-:22 \
      -object rng-random,filename=/dev/urandom,id=rng0 -device virtio-rng-pci,rng=rng0 \
      -chardev null,id=virtcon -machine virt,secure=on -nographic


During the boot sequence, you will observe the following:

.. code-block:: none

  [    1.932467] Freeing unused kernel memory: 4736K
  [    1.933323] Run /init as init process
  Starting version 250.5+
  [   53.995060] e2fsck: otaroot: clean, 7841/136880 files, 79834/156064 blocks
  Enrolling LUKS2 keyslot based on pkcs11 token
  Token successfully initialized
  User PIN successfully initialized
  Key pair generated:
  Private Key Object; RSA
    label:      luks
    ID:         9d
    Usage:      decrypt, sign
    Access:     sensitive, always sensitive, never extractable, local
  Public Key Object; RSA 2048 bits
    label:      luks
    ID:         9d
    Usage:      encrypt, verify
    Access:     local
  Engine "pkcs11" set.
  Created certificate:
  7Certificate Object; type = X.509 cert
    label:      luks
    subject:    DN: CN=LmP
    ID:         9d
  Successfully logged into security token 'lmp' via protected authentication path.
  New PKCS#11 token enrolled as key slot 0.
  Wiped slot 31.
  Successfully logged into security token 'lmp' via protected authentication path.
  Successfully decrypted key with security token.
  [...]
  [  OK  ] Reached target Basic System.
	   Starting D-Bus System Message Bus...
	   Starting Check and fix an … store of the docker daemon...
	   Starting IPv6 Packet Filtering Framework...
	   Starting IPv4 Packet Filtering Framework...
	   Starting Online LUKS2 disk re-encryption...
	   Starting User Login Management...
  [  OK  ] Started TEE Supplicant.
  [  OK  ] Started Network Name Resolution.
  [  OK  ] Finished IPv6 Packet Filtering Framework.
  [  OK  ] Finished IPv4 Packet Filtering Framework.
  [  OK  ] Starting Network Manager Script Dispatcher Service...
  [  OK  ] Started Network Manager Script Dispatcher Service.

  Linux-microPlatform 4.0.11 qemuarm64-secureboot -

  qemuarm64-secureboot login: fio
  Password:

  fio@qemuarm64-secureboot:~$

  [  OK  ] Finished Online LUKS2 disk re-encryption.
	   Starting Resize root filesystem to fit available disk space...
  [  210.434491] EXT4-fs (dm-0): resizing filesystem from 156064 to 160161 blocks
  [  210.448134] EXT4-fs (dm-0): resized filesystem to 160161
  [  OK  ] Finished Resize root filesystem to fit available disk space.


After the service has finished, you can inspect the volume. First list
the block devices:

.. code-block:: none

  fio@qemuarm64-secureboot:~$ lsblk
  NAME           MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINTS
  zram0          251:0    0     0B  0 disk
  vda            253:0    0 925.6M  0 disk
  |-vda1         253:1    0    78M  0 part  /var/rootdirs/mnt/boot
  |-vda2         253:2    0   200M  0 part  /boot
  `-vda3         253:3    0 641.6M  0 part
    `-vda3_crypt 252:0    0 625.6M  0 crypt /var
					    /usr
					    /
					    /sysroot


Then inspect the encrypted one:

.. code-block:: none

  fio@qemuarm64-secureboot:~$ sudo cryptsetup luksDump /dev/vda3
  Password:
  LUKS header information
  Version:        2
  Epoch:          99
  Metadata area:  16384 [bytes]
  Keyslots area:  16744448 [bytes]
  UUID:           06be9f40-ac4f-4301-ad33-e566def6023d
  Label:          otaroot
  Subsystem:      (no subsystem)
  Flags:          (no flags)

  Data segments:
    0: crypt
	  offset: 16777216 [bytes]
	  length: (whole device)
	  cipher: aes-xts-plain64
	  sector: 512 [bytes]

  Keyslots:
    1: luks2
	  Key:        512 bits
	  Priority:   normal
	  Cipher:     aes-xts-plain64
	  Cipher key: 512 bits
	  PBKDF:      pbkdf2
	  Hash:       sha512
	  Iterations: 1000
	  Salt:       a2 76 b4 61 3b c6 79 02 1a c1 23 89 02 ca 02 8f
		      f3 82 ec e6 c4 b0 6a c7 4a 4b 99 5e e6 92 c0 88
	  AF stripes: 4000
	  AF hash:    sha512
	  Area offset:32768 [bytes]
	  Area length:258048 [bytes]
	  Digest ID:  1
  Tokens:
    0: systemd-pkcs11
	  pkcs11-uri: pkcs11:token=lmp;object=luks
	  pkcs11-key: 38 49 ce f7 3e e9 dc fc 66 3d b8 13 90 ec ec 29
		      99 73 5d 47 6a cb d0 fc 6c ab 1c a7 26 a8 08 7e
		      46 b3 5d 15 f5 01 a9 e7 e6 d2 80 72 15 14 0d 0b
		      61 85 fe ee 1f f8 f0 04 26 c8 46 31 83 52 cc 37
		      44 d7 2a 83 7d 5a d9 44 a3 90 d0 f5 ff f2 9d e3
		      6f 09 4b 2c 79 5e df e3 b0 f7 df b4 b2 8c 0b 78
		      0a 4a 31 c1 d1 63 bb 54 a3 ca c9 a9 a3 88 bc ec
		      96 68 25 26 75 b3 44 3d 9b ee bc a4 73 a5 e2 b3
		      f2 5e a3 74 29 32 7a 46 b2 af 55 cf 48 3d b6 ea
		      4e d0 ca 0c da 06 f1 4e 33 23 73 be bb b0 c0 e1
		      ab bf 7a 2d f3 d7 7a be 5c 01 e5 d6 ab 43 33 91
		      48 e7 14 77 61 1c b9 c0 2c 6a 47 36 4c 1f a1 81
		      39 8c 5b 56 43 fa 86 33 7f 8d ec ee cf 74 1a 3a
		      43 69 6d bf 3b 70 70 ea 4b f7 02 a0 99 c0 55 02
		      49 16 14 00 45 da 78 da b9 5e 34 17 65 1b 3b c3
		      78 26 64 60 bf fe da 11 a0 3b 7a f9 0f 9e 93 8f
	  Keyslot:    1
  Digests:
    1: pbkdf2
	  Hash:       sha512
	  Iterations: 1000
	  Salt:       a6 10 c3 0d 89 22 c4 67 32 c1 c4 49 31 6f 05 10
		      4a f6 3d bd 7f 26 7a ba 9e 74 54 0b 5f da 54 34
	  Digest:     58 da 0f b2 ec d5 0d 5d 3d 99 15 85 85 ab e5 40
		      41 14 9c 57 6a 16 02 08 5d 8f 2a 18 ca 77 2d 7b
		      e1 be 92 d4 0a 49 f1 f1 77 48 c3 c1 27 35 57 ea
		      68 47 60 20 15 a1 a2 80 11 c5 dd 8e c7 93 c4 80


You can also examine the PKCS#11 slot created by OP-TEE to verify the
presence of the RSA-2048 key mentioned earlier:

.. code-block:: none

  root@qemuarm64-secureboot:/var/rootdirs/home/fio# pkcs11-tool --module /usr/lib/libckteec.so.0 --list-token-slots
  Available slots:
  Slot 0 (0x0): 94e9ab89-4c43-56ea-8b35-45dc07226830
    token state:   uninitialized
  Slot 1 (0x1): 94e9ab89-4c43-56ea-8b35-45dc07226830
    token label        : lmp
    token manufacturer : Linaro
    token model        : OP-TEE TA
    token flags        : login required, PIN pad present, rng, token initialized, PIN initialized
    hardware version   : 0.0
    firmware version   : 0.1
    serial num         : 0000000000000001
    pin min/max        : 4/128
  Slot 2 (0x2): 94e9ab89-4c43-56ea-8b35-45dc07226830
    token state:   uninitialized

.. note::

   The OP-TEE PKCS#11 secure storage emulation  will NOT survive across
   reboots. As a consequence of this, because the root file system
   was encrypted, the system will encounter a failure in mounting the
   root file system during the subsequent boot.


If you were to reboot the system under the described circumstances, you
should expect to encounter the following error:

.. code-block :: none

  [    1.776260] registered taskstats version 1
  [    1.776628] Loading compiled-in X.509 certificates
  [    1.879079] Loaded X.509 cert 'Default insecure key from Factory II: 1b2327c0b75d0bc1e4914c8195bbf053629b8abb'
  [    1.902679] uart-pl011 9000000.pl011: no DMA platform data
  [    1.937637] Freeing unused kernel memory: 4736K
  [    1.938472] Run /init as init process
  Starting version 250.5+
  No slot with token named "lmp" found
  PKCS11 certificate not found!


.. _re-encryption:
  https://man7.org/linux/man-pages/man8/cryptsetup-reencrypt.8.html

.. _systemd-cryptenroll:
   https://www.freedesktop.org/software/systemd/man/systemd-cryptenroll.html

.. _swtpm:
   https://github.com/stefanberger/swtpm/wiki
