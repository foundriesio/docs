# LmP V95 Release Notes

[v95 Test Results](https://)

**Table of Contents**
- [LmP V95 Release Notes](#lmp-v95-release-notes)
  - [Attention Points for Migration](#attention-points-for-migration)
  - [Aktualizr-Lite Updates](#aktualizr-lite-updates)
    - [New Features](#new-features)
    - [Improvements](#improvements)
    - [Bug Fixes](#bug-fixes)
    - [Testing](#testing)
  - [Composectl Updates](#composectl-updates)
    - [New Features](#new-features-1)
    - [Bug Fixes](#bug-fixes-1)
    - [Testing](#testing-1)
  - [General Updates](#general-updates)
    - [Deprecation list](#deprecation-list)
  - [Plans for the Future](#plans-for-the-future)
  - [Known Issues](#known-issues)

## Attention Points for Migration
Things to be aware of when [updating LmP](https://docs.foundries.io/95/reference-manual/linux/linux-update.html)from the v94.y release:

1. **Scarthgap**: **v95** is the first LmP release based on Yocto Project Scarthgap (5.0.9).
   So, when updating a FoundriesFactory from previous LmP versions the line
   `LAYERSERIES_COMPAT_meta-subscriber-overrides = "scarthgap"`
    on `meta-subscriber-overrides/conf/layer.conf` will be required.
2. **Merge conflict**: When using the `lmp-tools/scripts/update-factory-manifest`
   script to update a previously created FoundriesFactory to **v95**,
   a merge conflict is expected -
   [FAQ](https://docs.foundries.io/latest/user-guide/troubleshooting/troubleshooting.html#update-foundriesfactory-fanifest-merge-conflict)
3. **Linux Kernel 6.6**: The default directory expected for the DTB files for
   Linux Kernel 6.6 has changed.
   Remove the `dir` from `KERNEL_DEVICETREE` items `<dir>/<dtb-name>`
4. **`aktualizr-lite`**: Change in downgrade behavior, now downgrades are not allowed
   by default for the daemon
5. **BSP** Updates
   1. **TI** BSP updated to the 11.00.01 release, without major changes
   2. **NVIDIA** Tegra BSP updated to the L4T R35.6.0 release,
      without major changes
   3. **NXP** BSP updated to the lf-6.6.52-2.2.0 release, including updates to
      U-Boot and Kernel, which could cause patch conflicts
   4. **u-boot-scr**: vendor prefix was removed from kernel-lmp-fitimage,
      so make sure to align the boot scripts to also remove the vendor prefix
      in the `fdtfile` variable.
   5. **Jailhouse** support in LmP is removed. An error might occur during the migration -
      [FAQ](https://docs.foundries.io/latest/user-guide/troubleshooting/troubleshooting.html#jailhousesupportin-lmp-is-removed)
   6. **am64xx-evm**: when updating from **v94** serial has to be added in the
      local boot entry conf -
      [How to](https://docs.foundries.io/latest/user-guide/lmp-customization/lmp-customization.html#kernel-command-line-arguments)
   7. **imx8mn-ddr4-evk-sec**: WiFi is not working


Please check the respective vendor BSP release notes for more
information.

## Aktualizr-Lite Updates

### New Features
> - Added support for EFI boot firmware updates, including functionality to
>   get/set bootloader control environment variables using the
>   `fioefi_setenv` and `fioefi_printenv` utilities.
> - Added new CLI client commands: check, pull, install, and run.
>   These individual commands allow users to pull, install,
>   and apply updates from different contexts.
> - Introduced the `--src-dir` parameter for the `aktualizr-lite` CLI client,
>   enabling offline updates.
> - Automatic downgrade prevention.
> - Added experimental support for user-initiated rollbacks.

### Improvements

> - Integrated `composectl` for all operations involving Compose Apps,
>   such as pruning, checking if running, etc.
> - Optimized app management to minimize the number of actions performed on
>   Compose Apps during the update cycle.
> - Made app stopping before an update configurable.
> - Introduced several changes to the API.
> - Moved the custom SOTA client example from the `aktualizr-lite` repository to
>    a dedicated repository: https://github.com/foundriesio/sotactl.
> - Transitioned the aklite daemon to API-based usage.
> - Allow re-pulling of ostree commits marked as partial.

### Bug Fixes

> - Fix rollback Target selection on applications only update when using CLI
>   delay-app-install install mode.


### Testing
> - Added a
>   [Compose-based environment for developing and testing](https://github.com/foundriesio/aktualizr-lite/tree/v95?tab=readme-ov-file#development-and-testing-in-containerized-environment)
>   `aktualizr-lite` end-to-end in a containerized setup against a real Factory.

## Composectl Updates

### New Features

> - Added the publish command to package a Compose App as a container image and
>   upload it to a container registry.
> - Added the show command to print app manifest and Compose project details.
> - Introduced App bundle indexing, which includes hash generation for
>   each item in the bundle. The hashes are verified during app OTA updates,
>   installation, and starting. Additionally, the maximum app bundle size is
>   now limited to 1GB.

### Bug Fixes

> - Resolved minor issues, mainly related to app blob pruning and checking
>   whether an app is installed and running.

### Testing

> - Added a Compose-based environment for development and end-to-end testing of
>  `composectl` in a containerized setup.
> - Implemented a series of end-to-end tests, including tests for edge cases.

## General Updates

> - Yocto Project
>   - LMP release based on the OE/Yocto 5.0.8 **Scarthgap** release
>   - **BitBake** updated to the 2.8.8 release
>   - **Go** updated to the 1.22.12 stable release
>   - **Rust** updated to the 1.75 stable release
>   - **OpenSSL** updated to the 3.2.4 stable release
>   - **Linux-firmware** updated to the 20240909 snapshot
>   - The license for package `gmp` prefers **GPLv2-or-later** instead of dual license
> - BSP Updates
>   - `Linux-lmp` updated to the v6.6.74 stable release
>   - `Linux-lmp-rt` updated to the v6.6.65-rt47 stable release
>   - `Linux-lmp-ti-staging`: updated to the 10.01.10 tag
>   - **TI** BSP updated to the 11.00.01 release
>   - **NVIDIA** Tegra BSP updated to the L4T R35.6.0 release
>   - **NXP** BSP updated to the lf-6.6.52-2.2.0 release
>   - `u-boot-fio_imx`: imx8mn and imx8mp now require CONFIG_SPL_MXC_OCOTP=y

### Deprecation list

> - BSP
>   - Xilinx BSP: Support was moved from `meta-lmp` to `meta-partner`
>   - STM32 BSP: Support was moved from `meta-lmp` to `meta-partner`
>   - iMX 8ULP: Support for this SoC was removed from LmP
>   - iMX 7D/ULP: Support for this SoC was removed from LmP
> - General
>   - Jailhouse: Support for this package was removed from LmP
>     (check the respective vendor BSP support)
>   - Xenomai4: Support for this kernel feature was removed from LmP
>     (check the respective vendor BSP support)
>   - FIT_NODE_SEPARATOR: This variable is no longer used by LmP

## Plans for the Future

>   - TI BSP: Support will be moved from `meta-lmp` to `meta-partner` in **v96**
>   - NVidia BSP: Support will be moved from `meta-lmp` to `meta-partner` in **v96**

## Known Issues

TODO: Update with post-release findings