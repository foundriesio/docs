# LmP v97 Release Notes

**Quick Links:**
- [v97 Test Results](97/testresults_v97.md)
- [changelog_v97.md](v97/changelog_v97.md)

**Table of Contents**
- [LmP v97 Release Notes](#lmp-v97-release-notes)
  - [Important Migration Notes](#important-migration-notes)
  - [Foundries Updated Platform Components](#foundries-updated-platform-components)
    - [Aktualizr-Lite Updates](#aktualizr-lite-updates)
    - [Composectl Updates](#composectl-updates)
    - [fio-diag Updates](#fio-diag-updates)
    - [fioconfig Updates](#fioconfig-updates)
  - [Yocto Project Versions - Scarthgap 5.0.17](#yocto-project-versions---scarthgap-5017)
    - [Yocto ProjectSecurity Updates](#yocto-projectsecurity-updates)
  - [Deprecations](#deprecations)
  - [Plans for the Future](#plans-for-the-future)
  - [Known Issues](#known-issues)

## Important Migration Notes

_No migration notes for this release._

## Foundries Updated Platform Components

This release includes updates to the following Foundries-developed components:

| Component                    | Version                                    | Recipe Link                                                                                                                                                                                                                  |
|------------------------------|--------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| aktualizr-lite               | `v97`                                      | [aktualizr\_%.bbappend](https://github.com/foundriesio/meta-lmp/blob/d95a52269d8109de07bb1957c47dedcb45888f94/meta-lmp-base/recipes-sota/aktualizr/aktualizr_%.bbappend)                                                     |
| composectl                   | `lmp-97`                                   | [composectl\_git.bb](https://github.com/foundriesio/meta-lmp/blob/d95a52269d8109de07bb1957c47dedcb45888f94/meta-lmp-base/recipes-containers/composeapp/composectl_git.bb)                                                    |
| fio-diag                     | `1.2`                                      | [fio-diag\_1.2.bb](https://github.com/foundriesio/meta-lmp/blob/d95a52269d8109de07bb1957c47dedcb45888f94/meta-lmp-base/recipes-support/fio-diag/fio-diag_1.2.bb)                                                             |
| fioconfig                    | `638424812372cc60fea7f548712bfb92ed0275e2` | [fioconfig\_git.bb](https://github.com/foundriesio/meta-lmp/blob/d95a52269d8109de07bb1957c47dedcb45888f94/meta-lmp-base/recipes-support/fioconfig/fioconfig_git.bb)                                                          |
| lmp-device-register          | `2557b25bedd47315dec47a01f09d27b979e84569` | [lmp-device-register\_git.bb](https://github.com/foundriesio/meta-lmp/blob/d95a52269d8109de07bb1957c47dedcb45888f94/meta-lmp-base/recipes-sota/lmp-device-register/lmp-device-register_git.bb)                               |
| optee-fiovb                  | `d65977034839e01fc69c9577071059b84ea08f1d` | [optee-fiovb\_git.bb](https://github.com/foundriesio/meta-lmp/blob/d95a52269d8109de07bb1957c47dedcb45888f94/meta-lmp-base/recipes-security/optee/optee-fiovb_git.bb)                                                         |

### Aktualizr-Lite Updates

[View full changelog on GitHub](https://github.com/foundriesio/aktualizr-lite/releases/tag/v97.0.0)

**New Features:**
- **Proxy Support:** Adds configurable proxy support for fetching applications, enabling satellite use-case deployments
- **TUF Meta Update Events:** Emits a TUF meta update event when an error occurs or the target list is updated

**Improvements:**
- **Reduced Dependencies:** Removes dependency on the `timeout` binary
- **Better Error Reporting:** Prints more details when `composectl` commands fail

### Composectl Updates

[View full changelog on GitHub](https://github.com/foundriesio/composeapp/releases/tag/v96.1.0)

**New Features and Improvements:**
- **Proxy Support:** Adds proxy support via a configurable function in the application configuration
- **DockerHub Compatibility:** Improves compatibility with DockerHub images and compose apps
- **Force Update Completion:** Adds an option to force update completion
- **URI Support:** Extends `run` and `rm` commands to accept URIs
- **Debian Package:** Generates a Debian package as part of the release process

**Bug Fixes:**
- **Image Loading:** Fixes loading of identical images referenced multiple times with different paths
- **Cleanup Behavior:** Prunes only dangling images by default after uninstall or update completion
- **Suppress Non-Error Messages:** Fixes suppression of non-error messages when loading compose projects
- **Proxy Handling:** Improves proxy handling throughout the application
- **Image Deduplication:** Eliminates duplicate images during processing

 ### fio-diag Updates

- **Storage Usage:** Reports disk usage via `df -h`
- **SOTA conf.d Dump:** Reports contents of `/etc/sota/conf.d`
- **Speed Test:** More reliable speed test using `curl` with fallback to `wget`

### fioconfig Updates

**New Features:**
- **Improved Logging:** CLI and daemon logging now adapts appropriately for the given environment, with migration from log to slog
- **Public API:** Exposes a public API for using this tool inside other applications like fioup
- **Optional PKCS11 Support:** PKCS11 support is now optionally compiled
- **Run-and-Report Testing:** Adds support for run-and-report functionality with remote actions base
- **Enhanced Transport APIs:** Transport and config logic moved into public modules for improved usability
- **Remote Actions:** Initializes remote actions configuration with support for on-change handlers and fio-diag.sh execution
- **Service Management:** Improved systemd service handling with checks for enabled status before restarting

**Improvements:**
- **Extensible Initialization:** Refactored init functions to support better extensibility
- **Deployment Control:** Prevents aklite restart when not enabled

## Yocto Project Versions - Scarthgap 5.0.17

This release is based on OpenEmbedded/Yocto Project 5.0.17 (**Scarthgap**) and includes the following updated components:

| Package        | Version | Layer               | Recipe Link                                                                                                                                                                                              |
|----------------|---------|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| bitbake        | 2.8.1   | bitbake             | [\_\_init\_\_.py](https://github.com/lmp-mirrors/bitbake/blob/d3b4c352dd33fca90cd31649eda054b884478739/lib/bb/__init__.py)                                                                               |
| docker         | 25.0.3  | meta-virtualization | [docker-moby\_git.bb](https://github.com/lmp-mirrors/meta-virtualization/blob/d75faad37ae3cbbfe31dffaa6432553fc5450838/recipes-containers/docker/docker-moby_git.bb)                                     |
| go             | 1.22.12 | openembedded-core   | [go\_1.22.12.bb](https://github.com/lmp-mirrors/openembedded-core/blob/52380df998b3a8fe6a091f8547434a3231320a8e/meta/recipes-devtools/go/go_1.22.12.bb)                                                  |
| networkmanager | 1.46.0  | meta-openembedded   | [networkmanager\_1.46.0.bb](https://github.com/lmp-mirrors/meta-openembedded/blob/5124ac4a658899158f4a7a2ddf1d2ca931ec7d0e/meta-networking/recipes-connectivity/networkmanager/networkmanager_1.46.0.bb) |
| openssl        | 3.2.6   | openembedded-core   | [openssl\_3.2.6.bb](https://github.com/lmp-mirrors/openembedded-core/blob/52380df998b3a8fe6a091f8547434a3231320a8e/meta/recipes-connectivity/openssl/openssl_3.2.6.bb)                                   |
| ostree         | 2024.5  | meta-openembedded   | [ostree\_2024.5.bb](https://github.com/lmp-mirrors/meta-openembedded/blob/5124ac4a658899158f4a7a2ddf1d2ca931ec7d0e/meta-oe/recipes-support/ostree/ostree_2024.5.bb)                                      |
| rust           | 1.75.0  | openembedded-core   | [rust\_1.75.0.bb](https://github.com/lmp-mirrors/openembedded-core/blob/52380df998b3a8fe6a091f8547434a3231320a8e/meta/recipes-devtools/rust/rust_1.75.0.bb)                                              |
| systemd        | 255.21  | openembedded-core   | [systemd\_255.21.bb](https://github.com/lmp-mirrors/openembedded-core/blob/52380df998b3a8fe6a091f8547434a3231320a8e/meta/recipes-core/systemd/systemd_255.21.bb)                                         |

### Yocto ProjectSecurity Updates

For detailed CVE fixes included in this release, refer to the Yocto Project release notes:
- [Yocto Project 5.0.17](https://docs.yoctoproject.org/next/migration-guides/release-notes-5.0.17.html)
- [Yocto Project 5.0.16](https://docs.yoctoproject.org/next/migration-guides/release-notes-5.0.16.html)
- [Yocto Project 5.0.15](https://docs.yoctoproject.org/next/migration-guides/release-notes-5.0.15.html)
- [Yocto Project 5.0.14](https://docs.yoctoproject.org/next/migration-guides/release-notes-5.0.14.html)

## Deprecations

_No deprecations in this release._

## Plans for the Future

_To be announced in future releases._

## Known Issues

> **Note:** This section will be updated with any issues discovered during
> post-release testing and field deployment.
