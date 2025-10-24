.. _ref-linux-kernel:

Linux Kernel
============

A common and unified Linux® Kernel source tree is provided and used by the Linux microPlatform (LmP).
The latest continuous release is available on the `Foundries.io™ GitHub <https://github.com/foundriesio/linux>`_.

The kernel recipe can be found within the :ref:`meta-lmp layer <ref-linux-layers-meta-lmp>`, under ``meta-lmp-base/recipes-kernel/linux``.

.. _ref-linux-fragments:

LmP Kernel Configuration Fragments
----------------------------------

Together with the unified Linux Kernel tree, the LmP provides an additional repository for :term:`kernel configuration fragments <Fragments>`.
The latest continuous release of the kernel configuration fragments is available at `lmp-kernel-cache <https://github.com/foundriesio/lmp-kernel-cache>`_.

You can find the list of supported :term:`BSP` definitions and the configuration fragments used under ``lmp-kernel-cache/bsp``.

The fragments repository works similarly to the upstream ``yocto-kernel-cache`` repository.
As such, the same development workflow and documentation applies.
See the `Yocto Project Linux Kernel Development Manual`_ on how to work with the kernel metadata and configuration fragments.

.. _Yocto Project Linux Kernel Development Manual: https://docs.yoctoproject.org/4.0.6/kernel-dev/advanced.html

LmP With Real-Time Linux Kernel
--------------------------------

The recipe that can be used for real-time Linux is:

* ``meta-lmp/meta-lmp-base/recipes-kernel/linux/linux-lmp-rt_git.bb``

This is based on the ``linux-lmp`` recipe, extended to include the ``PREEMPT_RT`` patch-set (updated along with stable kernel updates).

The instructions to change the default Linux kernel to real-time are described in the following section.
After making the changes, build the LmP image as usual.

Building LmP with linux-lmp-rt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In ``meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc``,
set ``PREFERRED_PROVIDER_virtual/kernel`` to ``linux-lmp-rt`` :

.. code-block:: console

    $ cat meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc
    PREFERRED_PROVIDER_virtual/kernel:intel-corei7-64 = "linux-lmp-rt"

LmP With Linux Upstream
------------------------

The recipe ``meta-lmp/meta-lmp-base/recipes-kernel/linux/linux-lmp-dev.bb`` can be used to build the LmP with the upstream kernel tree instead of the LmP unified tree.
``linux-lmp-dev`` also uses the LmP Kernel Configuration Fragments repository for a compatible configuration.

Building LmP With linux-lmp-dev
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In ``meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc``,
set ``PREFERRED_PROVIDER_virtual/kernel`` to ``linux-lmp-dev`` :

.. code-block:: console

    $ cat meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc
    PREFERRED_PROVIDER_virtual/kernel = "linux-lmp-dev"

Now build any of the supported LmP images.

Specifying Linux Git Tree, Branch, and Commit Revision
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following can be also set in ``meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc``,
in order to build ``linux-lmp-dev`` using a specific Linux tree, branch, or commit revision::

    KERNEL_REPO = "git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git" # Kernel git repository
    KERNEL_BRANCH = "master" # Git kernel branch (default: master)
    KERNEL_COMMIT = "94710cac0e" # Kernel commit revision (default: HEAD)
    KERNEL_META_REPO = "git://github.com/foundriesio/lmp-kernel-cache.git" # Kernel configuration fragments repository
    KERNEL_META_BRANCH = "master" # Git kernel meta branch (default: master)
    KERNEL_META_COMMIT = "1c67180cfe" # Kernel meta commit revision (default: HEAD)
    LINUX_VERSION = "4.19-rc" # Linux kernel base version (base package version)
