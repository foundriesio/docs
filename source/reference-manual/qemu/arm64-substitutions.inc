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

