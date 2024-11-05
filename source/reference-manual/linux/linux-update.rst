.. _ref-linux-update:

Updating the Linux microPlatform Core
=====================================

The FoundriesFactory™ Platform manifest is tailored to make consuming core platform updates easily.
At Foundries.io™, we often `release`_ Linux® microPlatform (LmP) updates as an effort to get the latest features and security fixes out to users.

.. _release:
   https://github.com/foundriesio/lmp-manifest/releases

.. note::
   You can subscribe to `Factory Notifications <https://app.foundries.io/settings/notifications>`_ to be informed of new LmP releases.

This page covers the steps for updating LmP to the latest release version.
It also shows common update problems and how to solve them.

.. note::
    The examples show a LmP update from v88 to v91 for an i.MX 8MMini based machine using the ``imx8mm-lpddr4-evk`` reference machine.
    Similar steps are taken for different reference hardware and LmP versions.

.. important:: 
    See :ref:`release notes <changelog>` for things to be aware of when updating to a given release.

.. tip::
    When facing issues to reproduce these steps, do not hesitate to contact `Foundries.io support <https://support.foundries.io/>`_.

Updating Your Factory
~~~~~~~~~~~~~~~~~~~~~

.. tip::
    We suggest that you perform the release migration on a new branch, forked off your stable development, so as to avoid impacting your current devices.
    After testing, the changes can be merged back to development.

    See :ref:`ref-new-branch`.

``lmp-manifest``
^^^^^^^^^^^^^^^^

We provide the helper script ``update-factory-manifest`` to update your Factory to a new LmP release.
This script tries to update your manifest to the latest LmP version available:

.. code-block::

    $ git clone https://source.foundries.io/factories/<myfactory>/lmp-manifest.git
    $ git clone https://github.com/foundriesio/lmp-tools
    $ cd lmp-manifest/
    $ git checkout <branch to update>
    $ ../lmp-tools/scripts/update-factory-manifest
    New upstream release(s) have been found.
    Merging local code with upstream release: 91
    Proceed ? (y/n): y

If no merge conflicts are found, it merges your changes and pushes the updated manifest to your Factory, triggering a new platform build.

.. warning::
    Once published, the update is deployed to devices following this tag.
    For this reason, doing the migration on a separate branch is recommended.

Common Pitfalls
"""""""""""""""

Usually at this stage, the problems are related to changes to ``lmp-manifest``.
For example, if you have bumped only ``meta-lmp`` in order to bring in new changes, it causes a merge conflict:

.. code-block::

    $ ../lmp-tools/scripts/update-factory-manifest
    Auto-merging lmp-base.xml
    CONFLICT (content): Merge conflict in lmp-base.xml
    Automatic merge failed; fix conflicts and then commit the result.

    Unable to perform automatic update.  Restoring previous state.

    One of these last few commits is probably causing a conflict:
    f54f9f9939b6c1548f838e9bd85b98bb01a6a42f (HEAD -> next) lmp-base: bump meta-lmp

In this case, you need to identify the conflicting commit and revert this change before proceeding:

.. code-block::

    $ git revert f54f9f9939b6c1548f838e9bd85b98bb01a6a42f
    $ ../lmp-tools/scripts/update-factory-manifest
    Automatic update successful!

.. tip::
    If something goes wrong, do not fret! This is why we use version control!

    .. code-block::

        $ git revert HEAD


``meta-subscriber-overrides``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The previous step pushes the update to the FoundriesFactory, which triggers a new platform build for the latest LmP release.
It is expected that, during the migration, this initial build often fails as ``meta-subcriber-overrides`` may have changes that require adjustments to the new release.

.. tip::
    It is helpful to :ref:`sync the Factory sources locally <ref-linux-building-ref>` so you can easily navigate through the Factory code.
    Some of the suggestions here are based on this.
    Remember: ``bitbake -e`` is a powerful tool.

* **Layer compatibility**

Make sure ``meta-subscriber-overrides`` is compatible with the current OE release.

.. code-block::

    $ cat meta-lmp/meta-lmp-bsp/conf/layer.conf | grep COMPAT
    LAYERSERIES_COMPAT_meta-lmp-bsp = "kirkstone"
    $ cat meta-subscriber-overrides/conf/layer.conf | grep COMPAT
    LAYERSERIES_COMPAT_meta-subscriber-overrides = "kirkstone"

* **Revert unecessary backports**

In some cases, the Factory has backports applied to the old version.
It can be due to fixing critical bugs or bringing in a new feature.

These commits are tagged with ``[REVERTME-vXX]``, that indicates the first LmP version to integrate that change, which makes the backport unrequired.

.. note::
    For example, a backport bugfix commit for ``lmp-device-register`` can be found below:

    .. code-block::

        [REVERTME-v91] sota: device register: bump lmp-device-register

        Bump lmp-device-register to bring patch that makes writing of
        config files safer.

        diff --git a/recipes-sota/lmp-device-register/lmp-device-register_git.bbappend b/recipes-sota/lmp-device-register/lmp-device-register_git.bbappend
        new file mode 100644
        index 0000000..0bdbd23
        --- /dev/null
        +++ b/recipes-sota/lmp-device-register/lmp-device-register_git.bbappend
        @@ -0,0 +1 @@
        +SRCREV = "848bcbbba886320b13b11ac04826be0361288619"

During the migration, these commits need to be identified and reverted so they do not conflict with ``meta-lmp`` defaults.

.. code-block::

    $ git log --oneline | grep REVERT
    aaaaaaa [REVERTME-v91] sota: device register: bump lmp-device-register
    bbbbbbb [REVERTME-v91] sota: aktualizr: bump aktualizr
    $ git revert aaaaaaa
    $ git revert bbbbbbb

* **U-Boot**

To debug U-Boot issues, it is important to understand the U-Boot sources.
You can get the necessary information from the local build:

.. code-block::

    # Getting the U-Boot recipe name
    $ bitbake -e lmp-factory-image | grep PREFERRED_PROVIDER_virtual/bootloader
    PREFERRED_PROVIDER_virtual/bootloader="u-boot-fio"

    # Getting the U-Boot tree url based on previous output
    $ bitbake -e u-boot-fio | grep SRC_URI
    SRC_URI="git://github.com/foundriesio/u-boot.git;protocol=https;branch=2021.04+imx_5.10.35-2.0.0-fio file://fw_env.config file://lmp.cfg "

    # Getting U-Boot revision to sync sources
    $ bitbake -e u-boot-fio | grep SRCREV
    SRCREV="d5976b6253dcae875fb42fbef68e1d05e7de5141"

Now syncing U-Boot to the proper revision:

.. code-block::

    $ git clone git://github.com/foundriesio/u-boot.git # SRC_URI
    $ cd u-boot
    $ git checkout d5976b6253dcae875fb42fbef68e1d05e7de5141 # SRCREV

a. Patches

Factories sometimes carry U-Boot code that has been applied in LmP sources.
These patches do not apply cleanly to the sources and cause build errors (`do_patch` fails).

The user needs to review the patches in ``meta-subscriber-overrides/recipes-bsp/u-boot/u-boot-fio/<machine>/`` and drop those already applied in LmP.

Custom patches not applied in LmP, including hardware support, need to be rebased on top of the current U-Boot release.

.. tip::
    If you have multiple patches to be rebased, we suggest doing small sets at a time and testing the output before progressing, so you can spot any issues during the migration/rebase.
    Bringing several changes at once can cause problems and makes it hard to identify changes that break the U-Boot support.

b. Config

The best way to handle U-Boot config change is to compare the changes between the two LmP versions for the reference hardware.

For example, if migrating a custom i.MX 8MMini custom board (reference machine ``imx8mm-lpddr4-evk``) from LmP v88 to v91:

    * U-Boot configs for v88: https://github.com/foundriesio/meta-lmp/blob/mp-88/meta-lmp-bsp/recipes-bsp/u-boot/u-boot-fio/imx8mm-lpddr4-evk/lmp.cfg

    * U-Boot configs for v91: https://github.com/foundriesio/meta-lmp/blob/mp-91/meta-lmp-bsp/recipes-bsp/u-boot/u-boot-fio/imx8mm-lpddr4-evk/lmp.cfg

A ``diff`` between these two files brings which configs were dropped/added to the new release:

.. code-block::

    $ cd meta-lmp
    $ git diff <old-tag> <new-tag> <path-to-file>
    $ git diff mp-88 mp-91 meta-lmp-bsp/recipes-bsp/u-boot/u-boot-fio/imx8mm-lpddr4-evk/lmp.cfg

.. tip::
    Problems with the current configuration can cause U-Boot `do_configure` step to fail:

    .. code-block::

        Summary: 1 task failed:
          /build-lmp/conf/../../layers/meta-lmp/meta-lmp-base/recipes-bsp/u-boot/u-boot-fio_imx-2022.04.bb:do_configure

    This likely means a critical config is not defined.

* **boot.cmd**

Similar to U-Boot configs, `boot.cmd` changes can be easily spotted by comparing the two LmP versions:

    * `boot.cmd` for v88: https://github.com/foundriesio/meta-lmp/blob/mp-88/meta-lmp-bsp/recipes-bsp/u-boot/u-boot-ostree-scr-fit/imx8mm-lpddr4-evk/boot.cmd

    * `boot.cmd` for v91: https://github.com/foundriesio/meta-lmp/blob/mp-91/meta-lmp-bsp/recipes-bsp/u-boot/u-boot-ostree-scr-fit/imx8mm-lpddr4-evk/boot.cmd

.. code-block::

    $ cd meta-lmp
    $ git diff mp-88 mp-91 meta-lmp-bsp/recipes-bsp/u-boot/u-boot-ostree-scr-fit/imx8mm-lpddr4-evk/boot.cmd

.. _ref-kernel-update:

* **Kernel**

Like U-Boot, it is important to understand the kernel sources when bringing up a new kernel version.
You can get the necessary information from the local build:

.. code-block::

    # Getting the Kernel recipe name
    $ bitbake -e lmp-factory-image | grep PREFERRED_PROVIDER_virtual/kernel
    PREFERRED_PROVIDER_virtual/kernel="linux-lmp-fslc-imx"

    # Getting the kernel tree url based on previous output
    $ bitbake -e linux-lmp-fslc-imx | grep SRC_URI
    SRC_URI="git://github.com/Freescale/linux-fslc.git;protocol=https;branch=6.1-1.0.x-imx;name=machine;
    ...

    # Getting U-Boot revision to sync sources
    $ bitbake -e linux-lmp-fslc-imx | grep SRCREV
    SRCREV_machine="f28a9b90c506241e614212f2ce314d8f5460819d"

Now syncing Linux kernel to the proper revision:

.. code-block::

    $ git clone git://github.com/Freescale/linux-fslc.git # SRC_URI
    $ cd linux-fslc
    $ git checkout f28a9b90c506241e614212f2ce314d8f5460819d # SRCREV

a. Patches

Same as U-Boot patches, the user needs to review the patches in ``meta-subscriber-overrides/recipes-kernel/linux/linux-lmp-fslc-imx/<machine>/`` and drop those already applied in LmP.

Custom patches need to be rebased on top of the current kernel release.

Out of tree kernel drivers should be compatible with the current kernel version.
For that, check with the driver vendor for latest releases.

b. Config

LmP kernel uses config fragments as defined in `lmp-kernel-cache <https://github.com/foundriesio/lmp-kernel-cache/>`_.

The suggestion is to compare the changes between releases for the refence hardware and apply the diff to your machine configuration:

    * Config fragments for v88: https://github.com/foundriesio/lmp-kernel-cache/blob/mp-88-linux-v5.10.y/bsp/imx/imx8mmevk.cfg

    * Config fragments for v91: https://github.com/foundriesio/lmp-kernel-cache/blob/mp-91-linux-v6.1.y/bsp/imx/imx8mmevk.cfg

.. code-block::

    $ git diff mp-88-linux-v5.10.y mp-91-linux-v6.1.y bsp/imx/imx8mmevk.cfg

.. note::
    Note that this repository has multiple tags for each release depending on the kernel version the reference hardware runs:

    .. code-block::

        mp-88-linux-v4.19.y
        mp-88-linux-v5.10.y
        mp-88-linux-v5.14.y
        mp-88-linux-v5.15.y
        mp-88-linux-v5.4.y
        ...
        mp-91-linux-v5.15.y
        mp-91-linux-v6.1.y

    You can get this value as an output of the ``bitbake -e linux-lmp-fslc-imx | grep SRC_URI`` command shown :ref:`before <ref-kernel-update>`.

* **Device tree**

You can get the reference hardware device tree name by running in the local build:

.. code-block::

    $ MACHINE=<reference-machine> source setup-environment
    $ bitbake -e lmp-base-console-image | grep ^KERNEL_DEVICETREE

Use this information to find the proper ``.dts`` file in the kernel tree, for example:

.. code-block::

    KERNEL_DEVICETREE=" freescale/imx8mm-evk.dtb ...
    $ cd linux
    $ find -iname imx8mm-evk.dts
    ./arch/arm64/boot/dts/freescale/imx8mm-evk.dts

Compare the changes from this file between the two versions and apply them to your machine device tree.

.. tip::
    In some cases, changes in included ``.dtsi`` files cause build errors due to nodes that were moved or dropped, specially from the ``<soc>.dtsi`` file. Usually, the reference hardware device tree brings an updated fix for these issues. Please review these changes as needed.

* **OP-TEE**

OP-TEE config differences can be spotted by diffing the two releases:

    * OP-TEE configs in v88: https://github.com/foundriesio/meta-lmp/blob/mp-88/meta-lmp-bsp/recipes-security/optee/optee-os-fio-bsp.inc

    * OP-TEE configs in v91: https://github.com/foundriesio/meta-lmp/blob/mp-91/meta-lmp-bsp/recipes-security/optee/optee-os-fio-bsp.inc

.. code-block::

    $ cd meta-lmp
    $ git diff mp-88 mp-91 meta-lmp-bsp/recipes-security/optee/optee-os-fio-bsp.inc

Bring relevant changes from the reference machine to your machine code.

* **Mfgtool** (if applicable)

.. note::
    Not all machines require/support ``mfgtool`` build. Currently, i.MX and STM32MP are supported.

Check if the ``mfgtool-files`` from your reference machine have changed between the two releases. Mirror the changes to your machine.

For i.MX:

    * Mfgtool scripts in v88: https://github.com/foundriesio/meta-lmp/tree/mp-88/meta-lmp-bsp/recipes-support/mfgtool-files/mfgtool-files/imx8mm-lpddr4-evk

    * Mfgtool scripts in v91: https://github.com/foundriesio/meta-lmp/tree/mp-91/meta-lmp-bsp/recipes-support/mfgtool-files/mfgtool-files/imx8mm-lpddr4-evk

.. code-block::

    $ cd meta-lmp
    $ git diff mp-88 mp-91 meta-lmp-bsp/recipes-support/mfgtool-files/mfgtool-files/imx8mm-lpddr4-evk/

.. note::
    For STM32MP, the ``mfgtool`` scripts are located in https://github.com/foundriesio/meta-lmp/tree/mp-91/meta-lmp-bsp/dynamic-layers/stm-st-stm32mp/recipes-support/stm32-mfgtool-files/stm32-mfgtool-files.

For the i.MX SoCs, the update process of ``mfgtool`` hardware support recipes like ``u-boot-fio-mfgtool``, ``linux-lmp-dev-mfgtool`` and ``optee-os-fio-mfgtool`` is the same for each component as described in the previous sections.

.. tip::
    For Factory sources synced locally, the command line to set the build environment to enable ``bitbake -e`` commands for ``lmp-mfgtool`` is:

    .. code-block::

        MACHINE=<machine> DISTRO=lmp-mfgtool source setup-environment

Verifying Your Work
~~~~~~~~~~~~~~~~~~~

After you get a successful build, it is time to test the new artifacts.

If the LmP update brings a new U-Boot or Linux kernel version, the recommendation is to reflash a device from scratch and verify it is able to boot the new image.
Debug and fix eventual issues as you go.

After the device is able to boot to user space, validate other aspects that changed in this release, like out of tree kernel drivers and other customizations.
Basic LmP features, like OTA capabilites, are tested at every release for the reference hardwares.

Once you are happy with the software, you can then try an OTA from your latest release to this new Target.

.. important::
    Remember to trigger :ref:`ref-boot-software-updates` when necessary.

1. Take a bench device and flash it with the latest stable image of the **old** LmP version (e.g. v88).

2. Register it to the Factory to the tag which brings the new LmP version, for example ``next`` (e.g. v91):

    .. code-block::

        $ lmp-device-register -n test-lmp-update -t next

3. After the registration, the board updates from the **old** LmP version (v88) to the latest one available for the ``next`` tag (v91).

4. Fix eventual update issues until you get a successful iteration.

Merging Back to Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once your ``next`` branch is in a good state, you may wish to migrate your development branches to this new release.
Here, the development branch is called ``devel``.

1. Clone all 3 required repos:

    .. code-block::

        $ git clone https://github.com/foundriesio/lmp-tools
        $ git clone https://source.foundries.io/factories/<YOUR FACTORY>/lmp-manifest
        $ git clone https://source.foundries.io/factories/<YOUR FACTORY>/meta-subscriber-overrides

2. Update ``meta-subscriber-overrides``:

    .. code-block::

        $ cd meta-subscriber-overrides
        $ git checkout next
        $ git pull --rebase
        $ git checkout devel
        $ git pull --rebase
        $ git merge --ff-only next
        $ git commit --allow-empty -m "[skip ci] Update to LmP v91"
        $ git push

3. Update ``lmp-manifest``:

    .. code-block::

        $ cd lmp-manifest
        $ git checkout devel
        $ git pull --rebase
        $ ../lmp-tools/scripts/update-factory-manifest
        New upstream release(s) have been found.
        Merging local code with upstream release: 91
        Proceed ? (y/n):

4. Proceed by typing ``y``. This updates the ``lmp-manifest/devel`` branch and trigger a build for the new release.

5. Once it is built, a new Target for the latest LmP release becomes available for your development devices following ``devel``.

Common Errors and Tips
~~~~~~~~~~~~~~~~~~~~~~

* A good practice when debugging migration issues is to compare the reference machine changes from one LmP version to the other. Likely, the changes from the reference machine should be mirrored to your custom machine.

* Working on the LmP update in a separate branch is highly recommended so it does not block your development branches.

* For machines that support :ref:`lmp-mfgtool distro <ref-lmp-mfgtool>`, use that for a quick debug iteration: there is no need to flash the whole image to verify U-Boot, for example.

* Also for machines that support :ref:`lmp-mfgtool distro <ref-lmp-mfgtool>`, the suggestion is to keep a single source of patches for hardware support (for ``u-boot-fio``/``u-boot-fio-mfgtool`` and ``linux-lmp-fslc-imx``/``linux-lmp-dev-mfgtool``). This avoids duplicated code in the Factory.

For example:

.. code-block::

    $ tree recipes-bsp/u-boot
    ├── u-boot-fio
    │   └── <machine>
    │       ├── 0001-add-custom-hw-support.patch
    │       ├── 0002-add-custom-driver.patch
    │       └── 0003-enable-driver.patch
    │       └── lmp.cfg
    ├── u-boot-fio-<vendor>.inc
    ├── u-boot-fio_%.bbappend
    ├── u-boot-fio-mfgtool
    │   └── <machine>
    │       └── lmp.cfg
    └── u-boot-fio-mfgtool_%.bbappend

    $ cat recipes-bsp/u-boot/u-boot-fio-<vendor>.inc
    # common vendor u-boot-fio code
    SRC_URI:append:<machine> = " \
        file://0001-add-custom-hw-support.patch \
        file://0002-add-custom-driver.patch \
        file://0003-enable-driver.patch \
    "

    $ cat recipes-bsp/u-boot/u-boot-fio_%.bbappend
    FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

    require u-boot-fio-<vendor>.inc

    $ cat recipes-bsp/u-boot/u-boot-fio-mfgtool_%.bbappend
    FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:${THISDIR}/u-boot-fio:"

    require u-boot-fio-<vendor>.inc

* You can find the list of patches appended to the sources by grepping ``SRC_URI``, for example Linux kernel:

.. code-block::

    $ bitbake -e linux-lmp-fslc-imx | grep SRC_URI
    SRC_URI="git://github.com/Freescale/linux-fslc.git;protocol=https;branch=5.10-2.1.x-imx;name=machine; \
    git://github.com/foundriesio/lmp-kernel-cache.git;protocol=https;type=kmeta;name=meta;branch=linux-v5.10.y;destsuffix=kernel-meta \
    file://0004-FIO-toup-hwrng-optee-support-generic-crypto.patch \
    file://0001-FIO-extras-arm64-dts-imx8mm-evk-use-imx8mm-evkb-for-.patch \
    file://0001-FIO-tonxp-drm-bridge-it6161-add-missing-gpio-consume.patch \
    file://0001-arm64-dts-imx8mq-drop-cpu-idle-states.patch \
    file://0001-FIO-temphack-ARM-mach-imx-conditionally-disable-some.patch \
    file://0001-FIO-internal-arm64-dts-imx8mn-evk.dtsi-re-add-blueto.patch "

* Sometimes, a core recipe gets renamed between releases. In this case, old `.bbappends` may fail to override this recipe, for example:

.. code-block::

    ERROR: No recipes in default available for:
      /build-lmp/conf/../../layers/meta-subscriber-overrides/recipes-kernel/linux/linux-lmp-dev-mfgtool.bbappend

To fix this, go through the ``layers`` folder to understand the change to the core recipe, for example:

.. code-block::

    # v88
    $ find ../layers/ -iname linux-lmp-dev-mfgtool*
    ../layers/meta-lmp/meta-lmp-base/recipes-kernel/linux/linux-lmp-dev-mfgtool.bb
    ../layers/meta-lmp/meta-lmp-bsp/recipes-kernel/linux/linux-lmp-dev-mfgtool.bbappend
    ../layers/meta-lmp/meta-lmp-bsp/recipes-kernel/linux/linux-lmp-dev-mfgtool

    # v91
    $ find ../layers/ -iname linux-lmp-dev-mfgtool*
    ../layers/meta-lmp/meta-lmp-base/recipes-kernel/linux/linux-lmp-dev-mfgtool_git.bb

The previous recipe ``linux-lmp-dev-mfgtool.bb`` is now called ``linux-lmp-dev-mfgtool_git.bb``.
To avoid a build error, the ``meta-subscriber-overrides`` `.bbappend` should now be ``linux-lmp-dev-mfgtool_%.bbappend``.

* Getting through these steps is not an easy task! Do not hesitate to contact `Foundries.io support <https://support.foundries.io/>`_ during your LmP update cycle.

.. seealso::

    :ref:`ref-pg`
