SPL
===

In boards using SPL as the second stage bootloader,
like the supported i.MX targets, SPL is used to load and verify the integrity of the FIT image (i.e. ``u-boot.itb`` file).
The FIT image includes U-Boot proper, DTB, OP-TEE, and Arm Trusted Firmware (ARMv8), and possibly other firmware.
SPL verifies the signature of these sequentially loaded images, signed as part of FoundriesFactory CI.
It checks to make sure they were generated with the expected keys.

.. note::

  At this moment, Secure Boot is only supported on SPL-based targets, as LmP relies on a signed SPL as the root of trust.

U-Boot should support SPL, so ``meta-lmp`` handles the SPL and FIT image generation and signing of the FIT image components.
If SPL is not yet supported, you can enable it by following the
`U-Boot documentation and guidelines <https://github.com/ARM-software/u-boot/blob/master/doc/README.SPL>`_.
Append it to their U-Boot porting, or  `contact support <https://support.foundries.io>`_ for guidance.

Next, review the board-specific U-Boot patches and align them with the respective u-boot-fio version.
Commits can be applied with ``git rebase`` or ``git cherry-pick`` on top of the ``u-boot-fio`` branch.
The patches can be copied to the appropriate directory under ``meta-subscriber-overrides`` and included in a ``u-boot-fio`` .bbappend file.
`Devtool <https://docs.yoctoproject.org/ref-manual/devtool-reference.html>`_ can be used during the process.
As described in the Yocto Project documentation:

.. prompt:: bash host:~$

    devtool modify u-boot-fio
    devtool finish --force-patch-refresh u-boot-fio <layer_path>

The resultant source code from the merge of ``u-boot-fio`` and board-specific patches can now be compiled and tested on a target.
In some cases, the user may need to create additional patches in order to align their board support with the ``u-boot-fio`` tree.

For example:

.. prompt:: text

    recipes-bsp/u-boot/
    ├── u-boot-fio
    │ └── <board>
    │     ├── 0001-add-<board>-support.patch
    │     ├── 0002-add-feature.patch
    │     ├── 0003-fix-bug.patch
    │     └── 0004-align-with-u-boot-fio.patch
    └── u-boot-fio_%.bbappend

If applicable, you may need to do the same procedure for TF-A patches.
This would be the case for ARMv8 targets that have additional implementations by the vendor.
Some considerations on TF-A to comply with LmP can be found in :ref:`ref-sec-tfa-optee`.

.. note::

    If the target is based on imx8m*, you may also want to pay attention to the provided firmwares.
    This includes the likes of DDR and HDMI (when applicable), and the vendor ``imx-mkimage`` implementation.
    The vendor changes applied to ``u-boot-fio`` should match with the related projects (``imx-atf``, ``imx-mkimage``).
    Otherwise the ``u-boot-fio`` porting will not work.
