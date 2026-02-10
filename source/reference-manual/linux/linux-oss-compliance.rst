OSS Compliance With FoundriesFactory
====================================

The Yocto Project provides a set of tools to help with Open Source Software (OSS) compliance and
the FoundriesFactory™ Platform can be configured to use these tools to meet the requirements of various OSS licenses.

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

Where:

* ``<factory>`` is the FoundriesFactory name
* ``<version>`` is the target version (and can be found in the first column of :guilabel:`Targets`).
* ``<machine>`` is the machine name as in the ``factory-config.yml``.
* ``<image>`` is the image name as in the ``factory-config.yml``.
 
.. _ref-remove-gplv3:

How to Avoid Using Packages Depending on the License
----------------------------------------------------

FoundriesFactory uses the default Yocto Project configuration, controlled by the variable ``DISABLE_GPLV3``.
When set to ``"1"``, it prevents the use of packages under GPL-3.0, LGPL-3.0, or AGPL-3.0 licenses in the final image.

Change the file ``ci-scripts/factory-config.yml`` to include the variable ``DISABLE_GPLV3: "1"`` in the desired branches,
with the goal of disabling the GPLv3 packages.

.. code-block:: yaml

  lmp:
    ref_options:
      refs/heads/main:
        params:
          DISABLE_GPLV3: "1"
      refs/heads/devel:
        params:
          DISABLE_GPLV3: "1"

This is the only change needed, the meta-layers are handled in respect to the ``DISABLE_GPLV3`` variable.

For more details on license compliance tooling and configuration, see:

* `Maintaining Open Source License Compliance <https://docs.yoctoproject.org/singleindex.html#maintaining-open-source-license-compliance-during-your-product-s-lifecycle>`_
* `INCOMPATIBLE_LICENSE variable <https://docs.yoctoproject.org/ref-manual/variables.html#term-INCOMPATIBLE_LICENSE>`_

.. seealso::

   :ref:`sbom`
