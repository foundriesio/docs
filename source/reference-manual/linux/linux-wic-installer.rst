.. highlight:: sh

.. _ref-linux-wic-installer:

WIC Image Installer
===================

.. note::

  Only EFI compatible systems are currently supported by the image installer (e.g. ``intel-corei7-64``, ``generic-arm64``).

To generate a WIC based image installer, switch the default ``WKS_FILE:sota`` definition for your target machine to ``image-efi-installer.wks``:

.. code-block:: console

  $ cat meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc
  # WIC-based installer for the intel-corei7-64 target
  WKS_FILE:intel-corei7-64:sota = "image-efi-installer.wks.in"

  # WIC-based installer for the generic-arm64 target
  WKS_FILE:generic-arm64:sota = "image-efi-installer.wks.in"

WIC is only capable of consuming a single :term:`WKS` file (even if multiple are defined via ``WKS_FILES``).
Doing this forces the build system to only generate installer images.

Remove the custom ``WKS_FILE:sota`` override to restore the default behavior and generate normal bootable WIC images.

Testing WIC Image Installer With QEMU (x86)
-------------------------------------------

It is possible to test the WIC image installer with QEMU.
All that is required is an additional block device with enough disk space for the LmP rootfs image.

If running QEMU without graphics support, make sure that the default console is set to ``ttyS0,115200``.
This can be done manually in GRUB by editing the boot arguments before booting the ``install`` target.
It can also be done by removing ``console=tty0`` from the image installer by appending ``lmp-factory-custom.inc`` with::

    APPEND:remove:intel-corei7-64 = "console=tty0"

Create the virtual disk device that will be used as the target with ``qemu-img``:

.. code-block:: console

  $ qemu-img create -f raw disk.img 4G

Download ``lmp-factory-image-intel-corei7-64.wic`` and ``ovmf.secboot.qcow2`` from your Factory CI run.
Run QEMU with the following arguments:

.. code-block:: console

  $ qemu-system-x86_64 -device virtio-net-pci,netdev=net0,mac=52:54:00:12:35:02 \
      -netdev user,id=net0,hostfwd=tcp::2222-:22 \
      -object rng-random,filename=/dev/urandom,id=rng0 -device virtio-rng-pci,rng=rng0 \
      -drive if=none,id=hd,file=lmp-factory-image-intel-corei7-64.wic,format=raw \
      -device virtio-scsi-pci,id=scsi -device scsi-hd,drive=hd \
      -drive if=none,id=hd2,file=disk.img,format=raw -device scsi-hd,drive=hd2 \
      -drive if=pflash,format=qcow2,file=ovmf.secboot.qcow2 -no-reboot \
      -nographic -m 1024 -serial mon:stdio -serial null -cpu host -enable-kvm

Follow the instructions provided by the installer to install the LmP image into ``disk.img``.
After completed, hit enter to stop QEMU. 
Restart using ``disk.img`` as the primary block device:

.. code-block:: console

  $ qemu-system-x86_64 -device virtio-net-pci,netdev=net0,mac=52:54:00:12:35:02 \
      -netdev user,id=net0,hostfwd=tcp::2222-:22 \
      -object rng-random,filename=/dev/urandom,id=rng0 -device virtio-rng-pci,rng=rng0 \
      -drive if=none,id=hd,file=disk.img,format=raw \
      -device virtio-scsi-pci,id=scsi -device scsi-hd,drive=hd \
      -drive if=pflash,format=qcow2,file=ovmf.secboot.qcow2 \
      -nographic -m 1024 -serial mon:stdio -serial null -cpu host -enable-kvm

.. note::
   If running QEMU on a macOS (x86) host, replace ``-enable-kvm`` with ``-M accel=hvf``.
