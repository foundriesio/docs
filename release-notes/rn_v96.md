# LmP v96 Release Notes

**Quick Links:**
- [v96 Test Results](placeholder)

**Table of Contents**
- [LmP v96 Release Notes](#lmp-v96-release-notes)
  - [Important Migration Notes](#important-migration-notes)
  - [Updates](#updates)
    - [Platform Components](#platform-components)
    - [Aktualizr-Lite Updates](#aktualizr-lite-updates)
    - [Composectl Updates](#composectl-updates)
    - [Deprecations](#deprecations)
  - [Plans for the Future](#plans-for-the-future)
  - [Known Issues](#known-issues)

## Important Migration Notes

**Action Required for NXP Users:**

* NXP BSP support has been relocated from `meta-lmp` to the [`meta-partner`](https://github.com/foundriesio/meta-partner/) layer. The instructions for the migration can be found in the `meta-partner` README.

## Updates

### Platform Components

**Yocto Project - Scarthgap 5.0.13**

This release is based on OpenEmbedded/Yocto Project 5.0.13 (Scarthgap) and includes the following updated components:

| Component | Version |
|-----------|---------|
| BitBake | 2.8.1 |
| Go Runtime | 1.22.12-r0 |
| Rust | 1.75.0 |
| OpenSSL | 3.2.6-r0 |
| Linux Firmware | 20240909 |
| docker-cli-config | 0.1-r0 |
| docker-credential-helper-fio | 0.1-r0 |
| ostree-recovery-initramfs | 0.0.1-r0 |
| resize-helper | 0.1-r0 |
| ostree | 2024.5-r0 |
| NetworkManager | 1.46.0-r0 |
| systemd | 1:255.21-r0 |
| docker-moby | 25.0.3+gitf417435e5f6216828dec57958c490c4f8bae4f980+f417435e5f_67e0588f1d-r0 |

**Foundries Updated Platform Components:**
| Component | Version | Release |
|-----------|---------|-------|
| fioconfig | 62170c1344a7d3651c85354988677b77053d8ea1 | [link](https://github.com/foundriesio/fioconfig/commit/62170c1344a7d3651c85354988677b77053d8ea1) |
| fio-docker-fsck | c939707c8f424cfd02c8d3c42605ffdb3439d653 | [link](https://github.com/foundriesio/fio-docker-fsck/commit/c939707c8f424cfd02c8d3c42605ffdb3439d653) |
| lmp-device-register | 2557b25bedd47315dec47a01f09d27b979e84569 | [link](https://github.com/foundriesio/lmp-device-register/commit/2557b25bedd47315dec47a01f09d27b979e84569) |
| aktualizr-lite | 1.0+git0+067a72f2c3-7 | [link](https://github.com/foundriesio/aktualizr-lite/releases/tag/v96.0.0) |
| composectl | dc7fdc20251a73ad0ab9a6ffc91470d7286cfaea | [link](https://github.com/foundriesio/composeapp/releases/tag/v96.0.0) |

**Security Updates:**

For detailed CVE fixes included in this release, refer to the Yocto Project release notes:
- [Yocto Project 5.0.12](https://docs.yoctoproject.org/next/migration-guides/release-notes-5.0.12.html)
- [Yocto Project 5.0.13](https://docs.yoctoproject.org/next/migration-guides/release-notes-5.0.13.html)

### Aktualizr-Lite Updates

[View full changelog on GitHub](https://github.com/foundriesio/aktualizr-lite/releases/tag/v96.0.0)

**Key Improvements:**
- **Enhanced Visibility:** Uses composectl v96.0.0, which displays download progress and speed for each application blob
- **API & CLI Extensions:** Includes minor enhancements to the API and command-line interface, along with various bug fixes
- **Boost Compatibility:** Ensures compatibility with Boost version 1.88.0 and above

### Composectl Updates

[View full changelog on GitHub](https://github.com/foundriesio/composeapp/releases/tag/v96.0.0)

**Enhanced Download Management:**
- **Improved Visibility:**
  - Displays status of partially downloaded blobs in `check` and `pull` command outputs
  - Shows real-time download progress for each blob, including both average and current download speeds
- **Network Reliability:**
  - Adds configurable timeouts for registry communication to prevent stuck downloads:
    - Connection timeout: 2 minutes
    - Read timeout: 15 minutes
- **Performance Optimization:** Skips stopping apps that are not installed, reducing unnecessary overhead

### Deprecations

**Layer Reorganization:**
- **NXP BSP Support:** Relocated from `meta-lmp` to the [`meta-partner`](https://github.com/foundriesio/meta-partner/) layer
  - Affects all NXP-based hardware platforms

## Plans for the Future

_To be announced in future releases._

## Known Issues

> **Note:** This section will be updated with any issues discovered during post-release testing and field deployment.
