# Linux Kernel

A common and unified Linux Kernel source tree is provided and used by
the Linux microPlatform. The latest continuous release is available at
[github.com/foundriesio/linux](https://github.com/foundriesio/linux).

The Linux Kernel recipe can be found in the `Meta-LMP layer
<ref-linux-layers-meta-lmp>`, under the
`meta-lmp-base/recipes-kernel/linux` directory.

## Linux microPlatform Kernel Configuration Fragments

Together with the unified Linux Kernel tree, the Linux microPlatform
also provides an additional repository for the kernel configuration
fragments. The latest continuous release for the kernel configuration
fragments is available at
[github.com/foundriesio/lmp-kernel-cache](https://github.com/foundriesio/lmp-kernel-cache).

You can find the list of supported BSP definitions and configuration
fragments used under the `lmp-kernel-cache/bsp` directory.

The fragments repository works similarly to the upstream
`yocto-kernel-cache` repository, so the same development workflow and
documentation applies. See the [Yocto Project Linux Kernel Development
Manual](https://www.yoctoproject.org/docs/2.5/kernel-dev/kernel-dev.html#kernel-dev-advanced)
for more information on how to work and manage the kernel metadata and
configuration fragments.

## Linux microPlatform with Real-Time Linux Kernel

The recipe
`meta-lmp/meta-lmp-base/recipes-kernel/linux/linux-lmp-rt_git.bb` can be
used for real-time linux, which is based on the `linux-lmp` recipe, but
extended to include the PREEMPT\_RT patch-set (updated along with stable
kernel updates).

At this moment only the `intel-corei7-64` machine configuration is
supported.

### Building Linux microPlatform with linux-lmp-rt

Set the `PREFERRED_PROVIDER_virtual/kernel` to `linux-lmp-rt` in
`meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc`:

    $ cat meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc
    PREFERRED_PROVIDER_virtual/kernel_intel-corei7-64 = "linux-lmp-rt"

Now just build the Linux microPlatform image as usual.

## Linux microPlatform with Linux upstream

The recipe
`meta-lmp/meta-lmp-base/recipes-kernel/linux/linux-lmp-dev.bb` can be
used to build the Linux microPlatform with the upstream kernel tree
instead of the LmP unified tree. `linux-lmp-dev` also uses the Linux
microPlatform Kernel Configuration Fragments repository for a compatible
configuration.

### Building Linux microPlatform with linux-lmp-dev

Set the `PREFERRED_PROVIDER_virtual/kernel` to `linux-lmp-dev` in
`meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc`:

    $ cat meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc
    PREFERRED_PROVIDER_virtual/kernel = "linux-lmp-dev"

Now just build any of the supported Linux microPlatform images.

### Specifying Linux git tree, branch and commit revision

The following variables can be also set in
`meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc`
in order to build `linux-lmp-dev` using a specific linux tree, branch or
commit revision:

    KERNEL_REPO = "git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git" # Kernel git repository
    KERNEL_BRANCH = "master" # Git kernel branch (default: master)
    KERNEL_COMMIT = "94710cac0e" # Kernel commit revision (default: HEAD)
    KERNEL_META_REPO = "git://github.com/foundriesio/lmp-kernel-cache.git" # Kernel configuration fragments repository
    KERNEL_META_BRANCH = "master" # Git kernel meta branch (default: master)
    KERNEL_META_COMMIT = "1c67180cfe" # Kernel meta commit revision (default: HEAD)
    LINUX_VERSION = "4.19-rc" # Linux kernel base version (base package version)
