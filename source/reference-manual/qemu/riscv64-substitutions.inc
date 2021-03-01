.. |ARCH| replace:: riscv64
.. |MACHINE| replace:: qemuriscv64
.. |FIRMWARE_BLOB| replace:: fw_payload.elf
.. |ARTIFACT_COMMANDS| replace::

     # Download and extract the Factory image
     fioctl targets artifacts <target_number> |MACHINE|/lmp-factory-image-|MACHINE|.wic.gz | gunzip > lmp-factory-image-|MACHINE|.wic
     # Download OpenSBI Firmware
     fioctl targets artifacts <target_number> |MACHINE|/|FIRMWARE_BLOB| > |FIRMWARE_BLOB|
