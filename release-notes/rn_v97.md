# LmP v97 Release Notes

**Quick Links:**
- [v97 Test Results](placeholder)

**Table of Contents**
- [LmP v97 Release Notes](#lmp-v97-release-notes)
  - [Important Migration Notes](#important-migration-notes)
  - [Updates](#updates)
    - [Platform Components](#platform-components)
    - [Aktualizr-Lite Updates](#aktualizr-lite-updates)
    - [Composectl Updates](#composectl-updates)
    - [fioconfig Updates](#fioconfig-updates)
    - [Deprecations](#deprecations)
  - [Plans for the Future](#plans-for-the-future)
  - [Known Issues](#known-issues)

## Important Migration Notes

_No migration notes for this release._

## Updates

### Platform Components

**Yocto Project - Scarthgap 5.0.15**

This release is based on OpenEmbedded/Yocto Project 5.0.15 (Scarthgap) and includes the following updated components:

| Component | Version |
|-----------|---------|
| BitBake | 2.8.1 | <!-- TODO: confirm BitBake version for v97 -->
| Go Runtime | 1.22.12-r0 |
| Rust | 1.75.0 |
| OpenSSL | 3.2.6-r0 |
| Linux Firmware | 20240909 |
| docker-cli-config | 0.1-r0 |
| docker-credential-helper-fio | 0.1-r0 |
| ostree-recovery-initramfs | 0.0.1-r0 |
| resize-helper | 0.1-r0 |
| ostree | 2024.5-r0 |
| NetworkManager | 1.46.6-r0 |
| systemd | 1:255.21-r0 |
| docker-moby | 25.0.3+gitf417435e5f6216828dec57958c490c4f8bae4f980+f417435e5f_67e0588f1d-r0 |

**Foundries Updated Platform Components:**
| Component | Version | Release |
|-----------|---------|-------|
| fioconfig | `87efd8b30ea163b2bc97d9ed43c3a666f29864f8` | [link](https://github.com/foundriesio/fioconfig/commit/87efd8b30ea163b2bc97d9ed43c3a666f29864f8) |
| fio-docker-fsck | `c939707c8f424cfd02c8d3c42605ffdb3439d653` | [link](https://github.com/foundriesio/fio-docker-fsck/commit/c939707c8f424cfd02c8d3c42605ffdb3439d653) |
| lmp-device-register | `2557b25bedd47315dec47a01f09d27b979e84569` | [link](https://github.com/foundriesio/lmp-device-register/commit/2557b25bedd47315dec47a01f09d27b979e84569) |
| aktualizr-lite | `2362e88f8b105b32cf871505082bdf3ed242009c` | [link](https://github.com/foundriesio/aktualizr-lite/releases/tag/v97.0.0) |
| composectl | `cc9ef57a9986f768aa659e53142860d9b3818cdc` | [link](https://github.com/foundriesio/composeapp/releases/tag/v96.1.0) |

**Security Updates:**

For detailed CVE fixes included in this release, refer to the Yocto Project release notes:
- [Yocto Project 5.0.14](https://docs.yoctoproject.org/next/migration-guides/release-notes-5.0.14.html)
- [Yocto Project 5.0.15](https://docs.yoctoproject.org/next/migration-guides/release-notes-5.0.15.html)

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


### Deprecations

_No deprecations in this release._

## Plans for the Future

_To be announced in future releases._

## Known Issues

> **Note:** This section will be updated with any issues discovered during post-release testing and field deployment.
