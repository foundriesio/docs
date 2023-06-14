.. |ARCH| replace:: arm
.. |MACHINE| replace:: qemuarm
.. |FIRMWARE_BLOB| replace:: u-boot-qemuarm.bin
.. |QEMU_GUI_FLAGS| replace::

     -display gtk,gl=on -device virtio-gpu-pci

.. |ARTIFACT_COMMANDS| replace::

     # Download and extract the Factory image
     fioctl targets artifacts <target_number> |MACHINE|/lmp-factory-image-|MACHINE|.wic.gz | gunzip > lmp-factory-image-|MACHINE|.wic
     # Download ATF + OP-TEE + U-Boot binary
     fioctl targets artifacts <target_number> |MACHINE|/other/|FIRMWARE_BLOB| > |FIRMWARE_BLOB|
     # If resizing disk image, download the qcow2 file
     fioctl targets artifacts <target_number> |MACHINE|/other/lmp-factory-image-|MACHINE|.wic.qcow2 > lmp-factory-image-|MACHINE|.wic.qcow2

.. |QEMU_COW| replace::
   
     qemu-system-arm -machine virt,highmem=off -cpu cortex-a7 -m 1024M \\
     -bios u-boot-qemuarm.bin \\
     -serial mon:vc -serial null \\
     -drive id=disk0,file=mp-factory-image-qemuarm.wic.qcow2,if=none,format=qcow2 -device virtio-blk-device,drive=disk0 \\
     -object rng-random,filename=/dev/urandom,id=rng0 -device virtio-rng-pci,rng=rng0 \\
     -device virtio-net-device,netdev=usernet \\
     -netdev user,id=usernet,hostfwd=tcp::22222-:22 \\
     -no-acpi -d unimp -nographic
