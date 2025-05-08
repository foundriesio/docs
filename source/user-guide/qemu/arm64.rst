.. _ref-rm_qemu_arm64:

``arm64``
=========

.. include:: arm64-substitutions.inc

.. important::
     If using QEMU versions < 9.0, replace ``-machine acpi=off`` with ``-no-acpi``

.. include:: qemu-instructions.template

QEMU CLI
^^^^^^^^

.. code-block::

    qemu-system-aarch64 \
    -m 2048 \ 
    -cpu cortex-a57 \
    -smp 2 \
    -machine acpi=off \
    -bios flash.bin \
    -device virtio-net-device,netdev=net0,mac=52:54:00:12:35:02 \
    -device virtio-serial-device \
    -drive id=disk0,file=lmp-factory-image-qemuarm64-secureboot.wic,if=none,format=raw \
    -device virtio-blk-device,drive=disk0 -netdev user,id=net0,hostfwd=tcp::2222-:22 \
    -object rng-random,filename=/dev/urandom,id=rng0 \
    -device virtio-rng-pci,rng=rng0 \
    -chardev null,id=virtcon \
    -machine virt,secure=on 
    -nographic

.. note::
    A |FIRMWARE_BLOB| artifact is usually in the same location where you downloaded the ``.wic.gz`` image.
    If you are unable to locate |FIRMWARE_BLOB|, consider checking for other artifacts such as ``QEMU_EFI.fd`` and ``QEMU_VARS.fd``.
    Use these to boot the image with the ``-drive`` flag.
    Example:

    .. code-block::

        qemu-system-aarch64 \
        -drive file=lmp-factory-image-qemuarm64-secureboot.wic.qcow2,if=virtio,format=qcow2 \
        -device qemu-xhci \
        -device usb-tablet \
        -device usb-kbd \
        -net nic \
        -net user \
        -machine virt \
        -cpu host \
        -smp 4 \
        -m 2048 \
        -accel hvf \
        -no-reboot \
        -device virtio-gpu-pci \
        -display default,show-cursor=on \
        -drive file=QEMU_EFI.fd,format=raw,readonly=on,if=pflash \
        -serial mon:stdio -serial null

.. include:: qemu-ssh.template

.. tip::
    You can register your device by following the steps from :ref:`gs-register`.
