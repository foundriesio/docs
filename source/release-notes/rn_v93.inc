LmP V93 Release Notes
=====================

.. note::
    You can view the full `v93 changelog`_ for greater detail.

Attention Points for Migration
------------------------------

Things to be aware of when :ref:`updating LmP <ref-linux-update>` from the v92 release:

 * Base OE/Yocto version in v93 is still kirkstone (4.0.16)
 * TI BSP updated to the 09.02.00.001 release, without major changes
 * Rust had a major update, from 1.68.2 to the 1.74.1 release
 * Container stack updated based on the revisions used by Docker v25.0.2
 * Skopeo and nerdctl were removed, in favor of composectl (for managing compose apps)
 * TI AM62XX-EVM updated to use the internal eMMC as the default storage device

Please also check the respective vendor BSP release notes for more information.

Known Issues
------------

None.

New Features
------------

 * Composectl is now used for managing compose apps (replacing skopeo, which was removed)

Aktualizr-Lite Updates
----------------------

 * Move to usage of the new `composectl` utility.
 * Added offline update support to the public API.
 * Support of the hybrid/mixing offline and online update.
 * Added the CLI API - wrapper over the public API to streamline a custom CLI SOTA client.
 * Minor fixes and improvements in the offline update implementation and the calculation of the application update size.

General Updates
---------------

 * LMP release based on the OE/Yocto 4.0.16 Kirkstone release
 * Bitbake updated to the 2.0.16 release
 * ContainerD updated to the 1.7.13 release
 * Docker-CE updated to the 25.0.2 release
 * Runc updated to the 1.1.12 release
 * Linux-lmp updated to the v6.1.75 stable release
 * Linux-lmp-rt updated to the v6.1.75-rt23 stable release
 * Linux-lmp-ti-staging updated to the cicd.kirkstone.202401090400 tag
 * Go updated to the 1.20.14 stable release
 * Rust updated to the 1.74.1 stable release
 * OpenSSL updated to the 3.0.13 stable release
 * Linux-firmware updated to the 20231030 snapshot
 * TI BSP updated to the 09.02.00.001 release
 * Intel BSP updated to align with ESE tag release-146_adl_s-mr7

.. _v93 changelog:
   https://foundries.io/products/releases/93/
