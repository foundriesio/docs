# riscv64

Warning

qemu-system-riscv64 does not currently support this functionality.

<https://patchwork.kernel.org/project/qemu-devel/cover/cover.1538683492.git.alistair.francis@wdc.com/>

## QEMU CLI

    qemu-system-riscv64 -machine virt -m 1024 \
        -device virtio-serial-device -chardev null,id=virtcon -device virtconsole,chardev=virtcon \
        -device virtio-net-device,netdev=usernet \
        -netdev user,id=usernet,hostfwd=tcp::22222-:22 \
        -object rng-random,filename=/dev/urandom,id=rng0 -device virtio-rng-device,rng=rng0 \
        -bios fw_payload.elf \
        -monitor null \
        -drive file=lmp-factory-image-qemuriscv64.wic,format=raw,id=hd0 -device virtio-blk-device,drive=hd0 \
        -nographic

## Demo

./demo/x86\_64.cast

Tip

You can register your device following the steps from `gs-register`.
