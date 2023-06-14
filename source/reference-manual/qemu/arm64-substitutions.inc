.. |ARCH| replace:: arm64
.. |MACHINE| replace:: qemuarm64-secureboot
.. |FIRMWARE_BLOB| replace:: flash.bin
.. |QEMU_GUI_FLAGS| replace::

     -display gtk,gl=on -device virtio-gpu-pci

.. |ARTIFACT_COMMANDS| replace::

     # Download and extract the Factory image
     fioctl targets artifacts <target_number> |MACHINE|/lmp-factory-image-|MACHINE|.wic.gz | gunzip > lmp-factory-image-|MACHINE|.wic
     # Download ATF + OP-TEE + U-Boot binary
     fioctl targets artifacts <target_number> |MACHINE|/|FIRMWARE_BLOB| > |FIRMWARE_BLOB|
     # If resizing disk image, download the qcow2 file
     fioctl targets artifacts <target_number> |MACHINE|/other/lmp-factory-image-|MACHINE|.wic.qcow2 > lmp-factory-image-|MACHINE|.wic.qcow2

.. |QEMU_COW| replace::

     qemu-system-aarch64 -m 1024 -cpu cortex-a57 -no-acpi -bios flash.bin \\
     -device virtio-net-device,netdev=net0,mac=52:54:00:12:35:02 -device virtio-serial-device \\
     -drive id=disk0,file=lmp-factory-image-qemuarm64-secureboot.wic.qcow2,if=none,format=qcow2 \\
     -device virtio-blk-device,drive=disk0 -netdev user,id=net0,hostfwd=tcp::2222-:22 \\
     -object rng-random,filename=/dev/urandom,id=rng0 -device virtio-rng-pci,rng=rng0 \\
     -chardev null,id=virtcon -machine virt,secure=on -nographic
