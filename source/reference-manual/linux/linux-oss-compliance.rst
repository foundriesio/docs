OSS Compliance With FoundriesFactory
====================================

The Yocto Project provides a set of tools to help with Open Source Software (OSS) compliance.
FoundriesFactory® is configured to use some of them by default.
These provide a good starting point when working with license requirements.

There are several OSS licenses.
This document details technical aspects of handling the GPLv2 and GPLv3 license family.
However, the content here can be extended to other licenses.

.. warning:: This document focuses on some technical aspects and must not be considered legal advice.
   Always consult a lawyer.

Providing Source Code and License Manifest
------------------------------------------

Common requirements for many OSS licenses, such as GPLv2 and others, are to provide:

* A **license manifest**: all the projects used and their license
* The **source code**: all source code, including scripts and any changes, to be made available (accessible) to the user
* The **license text** and **copyright information**: a copy of the license for each project and the copyright information for attribution.

FoundriesFactory configures the LmP to provide a license manifest and source code tarball by default.

The license manifest for a given Target can be found at:

``https://app.foundries.io/factories/<factory>/targets/<version>/artifacts/<machine>/other/<image>-<machine>.license.manifest``

All the image's packages source code under the GPLv2 or GPLv3 license family can be found at:

``https://app.foundries.io/factories/<factory>/targets/<version>/artifacts/<machine>/other/<machine>-source-release.tar``

.. todo: * How to get the license text files

Where:

* ``<factory>`` is the FoundriesFactory name
* ``<version>`` is the target version (and can be found in the first column of :guilabel:`Targets`).
* ``<machine>`` is the machine name as in the ``factory-config.yml``.
* ``<image>`` is the image name as in the ``factory-config.yml``.

How to Avoid Using Packages Depending on the License
----------------------------------------------------

When using FoundriesFactory with hardware configured with secure boot, it may be necessary to avoid installing packages under certain licenses.

For example, GPLv3 requires that hardware restrictions *not limit or disallow variations of the software from being executed on the hardware*.
When using secure boot, the hardware is configured only to execute a complete boot and run unmodified software signed with a private key.

.. warning:: There are other examples of why a license should be avoided or chosen. Advice from a lawyer is recommended.

.. note:: Another option to meet the GPLv3 requirement when using hardware configured with secure boot,
   is providing either a way of disabling secure boot or the keys when requested.

When using LmP there are two variables that can be used for blocking licenses, ``INCOMPATIBLE_LICENSE`` and ``IMAGE_LICENSE_CHECKER_ROOTFS_DENYLIST`` [1]_.
Both of these variables list the licenses by SPDX identifier.

INCOMPATIBLE_LICENSE
""""""""""""""""""""

Add to the ``build/conf/local.conf`` or to the distro the following line [2]_:

.. prompt:: text

   INCOMPATIBLE_LICENSE = "GPL-3.0* LGPL-3.0* AGPL-3.0*"

Using this configuration to build ``lmp-factory-image`` results in the following error:

.. prompt:: text

   ERROR: lmp-factory-image-1.0-r0 do_rootfs: Package bash cannot be installed into the image because it has incompatible license(s): GPL-3.0+

In this example, the package `bash` cannot be installed because it is licensed under GPLv3.
This is the default approach from the Yocto Project.
An error is raised when a package under one of the listed licenses is used during build time.
This is true even if the package is not to be installed in the final image.

If a package is released under multi-license, this error is raised if any of the incompatible licenses are included.
This strategy can be used when there is a need to verify build time dependencies between packages.

IMAGE_LICENSE_CHECKER_ROOTFS_DENYLIST
"""""""""""""""""""""""""""""""""""""

This variable is introduced by the ``image-license-checker`` class.
In the same way as with ``INCOMPATIBLE_LICENSE``, it lists the licenses to be avoided, by SPDX identifier.

With this class, the package under the avoided license is built—when brought as a dependency.
When creating the rootfs, the licenses are checked, and if a package is under multi-license, an error is raised if any of the incompatible licenses are included.

Another important difference is that this class prevents the installation of the avoided license package, even for multi-licensed packages.

This class can be reviewed at `image-license-checker`_.

Add to the LmP Factory customization file ``meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc`` the lines from `ci-scripts` [3]_.

Using this configuration to build ``lmp-factory-image`` results in the following error:

::

  ERROR: lmp-factory-image-1.0-r0 do_rootfs: Packages have denylisted licenses:
  libunistring (LGPLv3+ | GPLv2), bash (GPLv3+), time (GPLv3), mc (GPLv3),
  mc-helpers (GPLv3), grep (GPLv3), dosfstools (GPLv3), coreutils (GPLv3+),
  mc-fish (GPLv3), libelf (GPLv2 | LGPLv3+), tar (GPLv3), less (GPLv3+ |
  BSD-2-Clause), sed (GPLv3+), gmp (GPLv2+ | LGPLv3+), libidn2 ((GPLv2+ |
  LGPLv3)), parted (GPLv3+), readline (GPLv3+), gawk (GPLv3), coreutils-stdbuf
  (GPLv3+), findutils (GPLv3+), bc (GPLv3+), cpio (GPLv3), gzip (GPLv3+), ed
  (GPLv3+), mc-helpers-perl (GPLv3)

This error means, for image ``lmp-factory-image``, a long list of packages under GPLv3 are being installed, such as ``bash``.
The goal here to clear the image from those dependencies.

.. _ref-remove-gplv3:

How to Remove Packages Under GPLv3 Family License
-------------------------------------------------

FoundriesFactory uses the `image-license-checker`_ approach.
Only a single change is needed to avoid using packages under GPL-3.0, LGPL-3.0 or AGPL-3.0 license in final image.

Change the file ``ci-scripts/factory-config.yml`` to include the variable ``DISABLE_GPLV3: "1"`` in the desired branches,
with the goal of disabling the GPLv3 packages.

.. prompt:: text

  lmp:
    ref_options:
      refs/heads/main:
        params:
          DISABLE_GPLV3: "1"
      refs/heads/devel:
        params:
          DISABLE_GPLV3: "1"

  mfg_tools:
    - machine: <machine>
      params:
        DISTRO: lmp-mfgtool
        EXTRA_ARTIFACTS: mfgtool-files.tar.gz
        IMAGE: mfgtool-files
        DISABLE_GPLV3: "0"

.. tip:: it is possible to enable or disable `DISABLE_GPLV3` on `mfgtool` targets, as shown above.

This is the only change needed, the meta-layers are handled in respect to the ``DISABLE_GPLV3`` variable.

It is important to note that when using an image different than ``lmp-factory-image``, other packages might be used.
In this case, the error message guides on which package to target.

.. seealso::

   :ref:`sbom`


.. _image-license-checker: https://github.com/foundriesio/meta-lmp/blob/main/meta-lmp-base/classes/image-license-checker.bbclass


.. rubric:: Footnotes

.. [1] Since **v87**,
       the variable ``IMAGE_LICENSE_CHECKER_ROOTFS_DENYLIST``
       replaces
       ``IMAGE_LICENSE_CHECKER_ROOTFS_BLACKLIST``.
.. [2] Since **v87**,
     the contents of ``INCOMPATIBLE_LICENSE`` has changed,
     as a consequence of the Kirkstone SPDX tags change.
.. [3] The list of license strings follows the SPDX standard and may vary.
       Consult the up-to-date code https://github.com/foundriesio/ci-scripts/blob/master/lmp/bb-config.sh#L189-L192.
