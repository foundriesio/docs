.. _ref-rm_qemu_arm:

arm
===

.. include:: arm-substitutions.inc
.. include:: qemu-instructions.template

QEMU CLI
^^^^^^^^

.. code-block:: 

   qemu-system-arm -machine virt,highmem=off -cpu cortex-a7 -m 1024M \
       -bios u-boot-qemuarm.bin \
       -serial mon:vc -serial null \
       -drive id=disk0,file=lmp-factory-image-qemuarm.wic,if=none,format=raw -device virtio-blk-device,drive=disk0 \
       -object rng-random,filename=/dev/urandom,id=rng0 -device virtio-rng-pci,rng=rng0 \
       -device virtio-net-device,netdev=usernet \
       -netdev user,id=usernet,hostfwd=tcp::22222-:22 \
       -no-acpi -d unimp -nographic

Demo
^^^^

.. asciinema:: ./demo/arm.cast
