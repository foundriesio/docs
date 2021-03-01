arm64
=====

.. include:: arm64-substitutions.inc
.. include:: qemu-instructions.template

QEMU CLI
^^^^^^^^

.. code-block:: 

     qemu-system-aarch64 -m 1024 -cpu cortex-a57 -no-acpi -bios -d unimp -semihosting-config enable,target=native \
       -device virtio-net-device,netdev=net0,mac=52:54:00:12:35:02 -device virtio-serial-device -device virtconsole,chardev=virtcon -device virtconsole,chardev=virtcon \
       -drive id=disk0,file=lmp-factory-image-qemuarm64.wic,if=none,format=raw \
       -netdev user,id=net0,hostfwd=tcp::2222-:22 \
       -chardev null,id=virtcon \
       -machine virt,secure=on -nographic

Demo
^^^^

.. asciinema:: ./demo/x86_64.cast
