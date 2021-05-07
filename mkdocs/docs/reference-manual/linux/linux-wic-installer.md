# WIC Image Installer

> Note
>
> Only EFI compatible systems are currently supported by the image
> installer (e.g. intel-corei7-64, n1sdp).

To generate a WIC based image installer, switch the default
`WKS_FILE_sota` definition for your target machine to
`image-efi-installer.wks`:

    $ cat meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc
    # WIC-based installer for the intel-corei7-64 target
    WKS_FILE_intel-corei7-64_sota = "image-efi-installer.wks.in"

    # WIC-based installer for the n1sdp target
    WKS_FILE_n1sdp_sota = "image-efi-installer.wks.in"

As WIC is only capable of consuming one single WKS file (even if
multiple are defined via WKS\_FILES), this will force the build system
to only generate installer images by default.

Remove the custom `WKS_FILE_sota` override to restore back to the
default behavior and generate normal bootable WIC images.

## Testing WIC Image Installer with Qemu (x86)

It is possible to test the WIC image installer with Qemu, all that is
required is an additional block device with enough disk space for the
LmP rootfs image.

If running Qemu without graphics support, make sure that the default
console is set to `ttyS0,115200`, which can be done manually in grub (by
editing the boot arguments before booting the `install` target) or by
removing `console=tty0` from the image installer by changing
`lmp-factory-custom.inc`:

    $ cat meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc
    APPEND_remove_intel-corei7-64 = "console=tty0"

Create the virtual disk device that will be used as target with
`qemu-img`:

    $ qemu-img create -f raw disk.img 4G

Download `lmp-factory-image-intel-corei7-64.wic` and `ovmf.qcow2` from
your own Factory CI run, then run Qemu with the following arguments:

    $ qemu-system-x86_64 -device virtio-net-pci,netdev=net0,mac=52:54:00:12:35:02 \
        -netdev user,id=net0,hostfwd=tcp::2222-:22 \
        -object rng-random,filename=/dev/urandom,id=rng0 -device virtio-rng-pci,rng=rng0 \
        -drive if=none,id=hd,file=lmp-factory-image-intel-corei7-64.wic,format=raw \
        -device virtio-scsi-pci,id=scsi -device scsi-hd,drive=hd \
        -drive if=none,id=hd2,file=disk.img,format=raw -device scsi-hd,drive=hd2 \
        -drive if=pflash,format=qcow2,file=ovmf.qcow2 -no-reboot \
        -nographic -cpu kvm64 -enable-kvm -m 1024 -serial mon:stdio -serial null

Now just follow the instructions provided by the installer in order to
install the actual LmP image into `disk.img`.

After completed, hit enter to stop the current Qemu execution and start
it up again, but using `disk.img` as the primary block device:

    $ qemu-system-x86_64 -device virtio-net-pci,netdev=net0,mac=52:54:00:12:35:02 \
        -netdev user,id=net0,hostfwd=tcp::2222-:22 \
        -object rng-random,filename=/dev/urandom,id=rng0 -device virtio-rng-pci,rng=rng0 \
        -drive if=none,id=hd,file=disk.img,format=raw \
        -device virtio-scsi-pci,id=scsi -device scsi-hd,drive=hd \
        -drive if=pflash,format=qcow2,file=ovmf.qcow2 \
        -nographic -cpu kvm64 -enable-kvm -m 1024 -serial mon:stdio -serial null
