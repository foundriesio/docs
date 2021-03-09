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
