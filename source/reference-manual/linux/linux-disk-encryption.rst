.. _howto-linux-disk-encryption:

Disk Encryption Support
=======================

LmP supports encrypting the disk used by the root file system on first boot. 
This is to guarantee a unique LUKS2 master key per device.

The effort for creating an encrypted root file system via CI (and required logic for online re-encryption during first boot) is part of ``meta-lmp`` `pull request 868 <https://github.com/foundriesio/meta-lmp/pull/868>`.

Prerequisites
-------------

As the process for decrypting the disk needs to be unattended, LmP requires either PKCS#11 (e.g. OP-TEE with RPMB as secure storage) or TPM 2.0 to be available by the target hardware.
These are leveraged for securely storing the Key Encryption Key (KEK) used for decrypting the disk during the boot process. 
This is done via LUKS2 tokens, leveraging systemd-pkcs11 or systemd-tpm2, see `systemd-cryptenroll`_ for more information.

For enhanced security, TPM 2.0 support also requires UEFI secure boot to be enabled.
This is because the key is bound to the Platform Configuration Register (PCR) 7, which tracks the secure boot state of the machine.

Enabling Support for Disk Encryption
------------------------------------

The following options require customizations for disk encryption support:

For adding the required ``initramfs-module-cryptfs`` module to the initramfs (based on what gets provided by ``MACHINE_FEATURES``, like ``tpm2`` or ``optee``):

.. code-block:: none

  DISTRO_FEATURES:append = " luks"

For splitting the ``/boot`` content from the ostree deployment in a separated partition (where kernel/initramfs gets stored, unencrypted).
This option is enabled by default on systems booting with UEFI support:

.. code-block:: none

  OSTREE_SPLIT_BOOT = "1"

For supporting the copying of content from ``/usr/lib/ostree-boot`` (used for boot firmware updates) to ``/boot``, as part of the ostree deployment step (OTA).
This is required for supporting boot firmware updates on devices with encrypted root file systems:

.. code-block:: none

  OSTREE_DEPLOY_USR_OSTREE_BOOT = "1"

For supporting ``/boot`` being in a separated partition at the final image the selected ``WKS_FILE`` needs to support split boot.
UEFI based devices already have such setup by default, but on most ARM/ARM64 devices a custom WKS might be required.
As an example, iMX8-based devices should use ``sdimage-imx8-spl-split-boot-sota.wks.in`` instead of the default ``sdimage-imx8-spl-sota.wks.ini`` file:

.. code-block:: none

  WKS_FILE:sota:mx8mm-nxp-bsp = "sdimage-imx8-spl-split-boot-sota.wks.in"

.. note::

  Along with a custom ``WKS_FILE`` for split boot support, also update the target fstab to automatically mount ``/boot`` (from the first partition).
  This is not required with UEFI-based systems, as systemd is capable of automatically identifying and mounting the ESP partition during boot.

Implementation Details for OP-TEE PKCS#11 Support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A dedicated slot is required to avoid conflicts with the PKCS#11 token slot normally used by ``aktualizr-lite``.
This dedicated slot is currently hardcoded to slot 1, with the label ``lmp``.

During the encryption process the token slot is initialized and a RSA 2048 key is generated, which is later used by `systemd-cryptenroll`_.

Make sure to **not** erase the token slot or the key during the lifetime of the image.
Doing so would cause the system to fail at boot.
A recovery key can be created and provided manually if required, but it will not be an unattended boot.

Testing TPM 2.0 Support With Qemu (x86) and swtpm
-------------------------------------------------

It is possible to test the disk encryption support with TPM 2.0 with QEMU and `swtpm`_.

Make sure LUKS support is enabled for your x86 target:

.. code-block:: console

  $ cat meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc
  DISTRO_FEATURES:append:intel-corei7-64 = " luks"

Then enroll the :ref:`UEFI Secure Boot Certificates <ref-secure-boot-uefi>` to enable secure boot support.
This is required as the LUKS2 TPM 2.0 token leverages PCR 7, which tracks the secure boot state.

Now install ``swtpm`` on the host machine, and start the ``swtpm`` daemon.
This will be consumed by QEMU and act as the hardware TPM.

.. code-block:: console

   $ mkdir -p /tmp/mytpm
   $ while true; do swtpm socket --tpmstate dir=/tmp/mytpm --ctrl type=unixio,path=/tmp/mytpm/swtpm-sock --tpm2; done;

Run QEMU with the required extra TPM 2.0 related commands:

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

You should see the following during the first boot:

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

.. _systemd-cryptenroll:
   https://www.freedesktop.org/software/systemd/man/systemd-cryptenroll.html

.. _swtpm:
   https://github.com/stefanberger/swtpm/wiki
