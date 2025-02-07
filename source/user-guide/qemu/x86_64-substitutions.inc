.. |ARCH| replace:: x86_64
.. |MACHINE| replace:: intel-corei7-64
.. |FIRMWARE_BLOB| replace:: ovmf.secboot.qcow2
.. |QEMU_GUI_FLAGS_LINUX| replace::

     -vga virtio -display gtk,gl=on
.. |QEMU_GUI_FLAGS_MAC| replace::

     -display cocoa -device virtio-gpu-pci
.. |ARTIFACT_COMMANDS| replace::

     # Download and extract the Factory image
     fioctl targets artifacts <target_number> |MACHINE|/lmp-factory-image-|MACHINE|.rootfs.wic.gz | gunzip > lmp-factory-image-|MACHINE|.wic
     # Download OVMF UEFI Firmware
     fioctl targets artifacts <target_number> |MACHINE|/|FIRMWARE_BLOB| > |FIRMWARE_BLOB|
     # If resizing disk image, download the wic.qcow2 file. This is different than the ovmf.secboot.qcow2!
     fioctl targets artifacts <target_number> |MACHINE|/other/lmp-factory-image-|MACHINE|.wic.qcow2 > |MACHINE|\_device1.qcow2

.. |QEMU_COW| replace::

     qemu-system-x86_64 -m 1024 -cpu kvm64 -enable-kvm -serial mon:stdio -serial null \\
     -drive file=|MACHINE|\_device1.qcow2,format=qcow2,if=none,id=hd \\
     -device virtio-scsi-pci,id=scsi -device scsi-hd,drive=hd -device virtio-rng-pci \\
     -drive if=pflash,format=qcow2,file=ovmf.secboot.qcow2 \\
     -net user,hostfwd=tcp::22223-:22 -net nic -nographic
