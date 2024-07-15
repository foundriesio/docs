# LmP V92 Release Notes

> [!NOTE]
> You can view the full [v92 changelog](https://foundries.io/products/releases/92/) for greater detail.

* [v92 Test Results](https://qa-reports.foundries.io/lmp/lmp-ci-testing/build/51952d1d66536c4432bd3a27f8acbea7bc664f46/)

## Attention Points for Migration

Things to be aware of when [updating LmP](https://docs.foundries.io/92/reference-manual/linux/linux-update.html) from the v91 release:

> -   Base OE/Yocto version in v92 is still kirkstone (4.0.15)
> -   NXP BSP updated to the lf-6.1.36-2.1.0 release:
>     -   U-boot had a major update from 2022.04 to 2023.04, porting
>         work and configuration changes might be required
>     -   OP-TEE updated from 3.20 to 3.21, requiring ELE firmware
>         updates on both i.MX93 and i.MX8ULP targets
>     -   Base BSP kernel updated from 6.1 to 6.1.36, with additional
>         fixes and improved hardware support
>     -   `imx8mp-lpddr4-evk` MFGTool now uses standard imx-boot,
>         u-boot.itb is not required for flashing anymore
> -   TI BSP updated to the 09.00.00.009 release, but without major
>     changes when comparing with 09.00.00.005
> -   NVIDIA Tegra BSP updated to the L4T R35.4.1 release, still based
>     on JetPack 5
> -   STM32MP15 flashlayout definition is now generated dynamically,
>     which might require changes depending on the level of
>     customization

Please also check the respective vendor BSP release notes for more
information.

## Known Issues

There is now a known issue with regards to `fioconfig` and the handler
it executes whenever the config is changed. The handler in question
`aktualizr-toml-update` currently expects a default location for the
`sota.toml` file. However if the directory that contains the `sota.toml`
is changed due to configuration, this may result in an error thrown by
the handler stating it cannot find `sota.toml`, whenever running a
`fioconfig` change. This has been patched in the following
[commit](https://github.com/foundriesio/meta-lmp/commit/294c684386b7e463b21dcfa56c62d10224b9dfff).
That patch will ensure the handler from then on uses whichever directory
has been configured to hold the `sota.toml` file.

## New Features

> -   [Support for encrypted rootfs images with on-line re-encryption using TPM 2.0 or PKCS#11](https://docs.foundries.io/92/reference-manual/linux/linux-disk-encryption.html#howto-linux-disk-encryption)
> -   Common configuration fragment for u-boot now available as part of
>     meta-lmp-base
> -   Manufacturing tool support for TI [AM62XX](https://docs.foundries.io/92/reference-manual/boards/am62xx-sk.html)/[AM64XX](https://docs.foundries.io/92/reference-manual/boards/am64xx-sk.html) devices is now available
> -   Boot firmware version can now be exposed in both U-Boot proper and
>     SPL
> -   Support for nvidia-container-runtime on Tegra devices
> -   Support for dynamic generation of flashlayout files on STM32MP15
>     based devices

## Aktualizr-Lite Updates

> -   Update size check before pulling update for both apps and ostree
> -   API: Add delayed App installation mode
> -   Several bug fixes for both online and offline updates

## Hardware Support

> -   i.MX 93: following the NXP BSP lf-6.1.36-2.1.0 release, only A1
>     silicon based EVKs are supported

## General Updates

> -   LmP release based on the OE/Yocto 4.0.15 Kirkstone release
> -   Bitbake updated to the 2.0.15 release
> -   ContainerD updated to the 1.7.3 release
> -   Docker-CE updated to the 24.0.6 release
> -   Docker-Compose updated to the v2.21.0 release
> -   Clang updated to the 14.0.6 stable release
> -   GCC updated to the v11.4 stable release
> -   Go updated to the 1.20.12 stable release
> -   OpenSSL updated to the 3.0.12 stable release
> -   Runc updated to the 1.1.8 release
> -   Linux-firmware updated to the 20230804 snapshot
> -   NXP BSP updated to the lf-6.1.36-2.1.0 release
> -   NVIDIA Tegra BSP updated to the L4T R35.4.1 release
> -   TI BSP updated to the 09.00.00.009 release
> -   OP-TEE updated to the 3.21.0+fio release
> -   U-boot-fio rebased on top of the upstream 2023.04 release
> -   Linux-lmp updated to the v6.1.59 stable release
> -   Linux-lmp-rt updated to the v6.1.59-rt16 stable release
> -   Linux-lmp-fslc-imx updated to the 6.1.36-2.1.0 BSP release
> -   Linux-lmp-fslc-imx-rt updated to the v6.1.38 stable release
> -   Linux-lmp-ti-staging updated to the v6.1.33 stable release
