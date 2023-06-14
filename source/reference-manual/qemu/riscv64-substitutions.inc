.. |ARCH| replace:: riscv64
.. |MACHINE| replace:: qemuriscv64
.. |FIRMWARE_BLOB| replace:: fw_payload.elf
.. |QEMU_GUI_FLAGS| replace::

     -display gtk,gl=on -device virtio-gpu-pci

.. |ARTIFACT_COMMANDS| replace::

     # Download and extract the Factory image
     fioctl targets artifacts <target_number> |MACHINE|/lmp-factory-image-|MACHINE|.wic.gz | gunzip > lmp-factory-image-|MACHINE|.wic
     # Download OpenSBI Firmware
     fioctl targets artifacts <target_number> |MACHINE|/|FIRMWARE_BLOB| > |FIRMWARE_BLOB|
     # If resizing disk image, download the qcow2 file
     fioctl targets artifacts <target_number> |MACHINE|/other/lmp-factory-image-|MACHINE|.wic.qcow2 > lmp-factory-image-|MACHINE|.wic.qcow2

.. |QEMU_COW| replace::

     qemu-system-riscv64 -machine virt -m 1024 \\
     -device virtio-serial-device -chardev null,id=virtcon -device virtconsole,chardev=virtcon \\
     -device virtio-net-device,netdev=usernet \\
     -netdev user,id=usernet,hostfwd=tcp::22222-:22 \\
     -object rng-random,filename=/dev/urandom,id=rng0 -device virtio-rng-device,rng=rng0 \\
     -bios fw_payload.elf \\
     -monitor null \\
     -drive file=lmp-factory-image-qemuriscv64.wic.qcow2,format=qcow2,id=hd0 -device virtio-blk-device,dri  ve=hd0 \\
     -nographic
