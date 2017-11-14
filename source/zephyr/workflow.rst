.. _zephyr-workflows:

Development Workflows
=====================

This page describes the workflows for developing and deploying
embedded applications with the Zephyr microPlatform. It assumes that the
Zephyr microPlatform has successfully been installed as described in
:ref:`zephyr-getting-started`.

.. _zephyr-development-workflow:

Helper Script
-------------

After installing the Zephyr microPlatform repositories and build environment,
the Zephyr and mcuboot build systems and other tools can be used
directly. However, these interfaces can be hard to use when first developing
applications. For this reason, the Zephyr microPlatform provides a helper
script, named ``zmp``, which provides a higher-level interface.

The ``zmp`` utility is installed into the root of the Zephyr microPlatform
tree by ``repo sync``. It accepts multiple commands useful during
development; they are documented below. Run ``./zmp -h`` from the
Zephyr microPlatform installation directory for additional information.

.. _zephyr-build:

Build an Application: ``zmp build``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

   By default, mcuboot binaries and Zephyr microPlatform applications are built
   and signed with development keys which are not secret. While this makes
   development and testing more convenient, it is not suitable for
   production.

   It's not currently possible to generate mcuboot images that trust
   non-dev keys without editing the mcuboot source code.

   As such, the ``--signing-key`` and ``--signing-key-type`` arguments
   to ``zmp build`` are misleading, as the mcuboot image won't trust
   the key used to sign the application. Don't use these for now.

.. todo::

   Re-work after mcuboot can consume a key at build time.

The top-level command is ``zmp build``. By default, it takes a
path to an application inside the Zephyr microPlatform installation directory,
and builds a signed application image, as well as an mcuboot binary
capable of loading that application image. (The default behavior can
be changed through various options.)

To get help, run this from the Zephyr microPlatform root directory::

    ./zmp build -h

The ``zmp build`` command always builds out of tree; that is,
build artifacts are never generated in the source code directories. By
default, they are stored under ``outdir`` in the Zephyr microPlatform top-level
directory.

Examples:

- To build an application ``some-application`` available in the
  Zephyr microPlatform tree, targeting the BLE Nano 2::

      ./zmp build -b nrf52_blenano2 some-application

  This generates artifacts under ``outdir`` like so::

      outdir
      └── some-application
          └── nrf52_blenano2
              ├── app
              └── mcuboot

  The application build for ``nrf52_blenano2`` is in
  ``outdir/some-application/nrf52_blenano2/app``. The mcuboot build is
  in ``mcuboot``, next to ``app``.

- To build the same application for another board,
  e.g. ``96b_carbon``, use the ``-b`` option::

      ./zmp build -b 96b_carbon some-application

  The ``-b`` option can be used in any ``zmp build`` command to
  target other boards.

  Running this after building for BLE Nano 2 as in the above
  example results in a parallel set of build artifacts, like so::

      outdir
      └── some-application
          ├── 96b_carbon
          │   ├── app
          │   └── mcuboot
          └── nrf52_blenano2
              ├── app
              └── mcuboot

- It's fine to build application sources in a subdirectory. For
  example, running::

    ./zmp build some-nested/application-name

  will generate::

    outdir
    └── some-nested
        └── application-name
            └── nrf52_blenano2
                ├── app
                └── mcuboot

  Note that the signed image in ``nrf52_blenano2/app`` is named
  ``application-name-nrf52_blenano2-signed.bin``; i.e., just the base
  name of the application directory is used.

- To build or incrementally compile the application image only, not
  updating the mcuboot image, use ``-o``::

      ./zmp build -b nrf52_blenano2 -o app some-application

- Similarly, to build or incrementally compile mcuboot only::

      ./zmp build -b nrf52_blenano2 -o mcuboot some-application

.. _zephyr-configure:

Configure an Application: ``zmp configure``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Zephyr RTOS uses a configuration system called Kconfig, which is
borrowed from the Linux kernel. The ``zmp configure`` command lets
you change the configuration database for an application build, using
any of the Kconfig front-ends supported on your platform.

The top-level command is ``zmp configure``.

**This command can only be run after using** ``zmp build`` **to
create the build directory, which contains the configuration
database.**

To get help, run this from the Zephyr microPlatform root directory::

    ./zmp configure -h

Example uses:

- To change the application configuration (not the mcuboot
  configuration) for ``some-application`` for the default board::

      ./zmp configure -o app some-application

- To change the mcuboot (not application) configuration for another
  board, ``96b_carbon``::

      ./zmp configure -o mcuboot -b 96b_carbon some-application

If you don't specify ``-o``, then ``zmp configure`` will sequentially
run the application and mcuboot configuration interfaces, in that
order.

Note that ``zmp configure`` accepts many of the same options as
:ref:`zmp build <zephyr-build>`.

For more information on Kconfig in Zephyr, see `Configuration Options
Reference Guide
<http://docs.zephyrproject.org/reference/kconfig/index.html>`_.

.. _zephyr-flash:

Flash an Application to a Device: ``zmp flash``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After building an application and mcuboot binary with :ref:`zmp
build <zephyr-build>`\ [#makefileexport]_, the ``zmp flash``
command can be used to flash it to a board, usually via USB.

The ``zmp flash`` command uses information about the board
obtained from Zephyr's build system to choose a flashing utility, and
run it with the correct arguments to flash mcuboot and the application
binary to an attached board. Before using this command, make sure you
can flash your board using the Zephyr ``make flash`` command as
described in its `Zephyr documentation
<http://docs.zephyrproject.org/boards/boards.html>`_\
[#zephyrflash]_.

To get help, run this from the Zephyr microPlatform root directory::

  ./zmp flash -h

Basic uses:

- To flash the artifacts for ``some-application`` to the default board::

    ./zmp flash some-application

- To flash to a different board, ``96b_carbon``::

    ./zmp flash -b 96b_carbon some-application

- To flash to a particular board, given the device ID supported by its
  underlying flashing utility::

    ./zmp flash -b SOME_BOARD -d SOME_BOARD_ID some-application

The command also accepts an ``-e`` argument, which can be used to pass
extra arguments to the flashing utility.

Create an Application
---------------------

This is a rough guide for experimental development using the Zephyr
microPlatform.

We currently recommend that you start your application work from one
of our :ref:`iotfoundry-top`.

#. Begin by selecting one of the systems, and reproducing the demo on
   your hardware.

#. Create a new directory in the Zephyr microPlatform installation
   directory for your application:

   .. code-block:: console

      $ mkdir your_app

   This won't be managed by the Repo tool used to fetch updates for
   the microPlatform itself, leaving it up to you to decide how to
   version it, etc.

#. Copy one of the existing application sources under
   ``zephyr-fota-samples`` to your application directory.

   For example, to copy the ``dm-lwm2m`` example:

   .. code-block:: console

      $ cp -r zephyr-fota-samples/dm-lwm2m/* your_app

#. Make sure you can build and flash it as normal:

   .. code-block:: console

      $ ./zmp build -b YOUR_BOARD your_app
      $ ./zmp flash -b YOUR_BOARD your_app

#. Initialize any version control you would like on the ``your_app``
   directory, and make adjustments to suit your purposes. You can use
   the existing board support as a starting example.

   Refer to the `Zephyr developer guides`_ and other documentation for
   generic information on Zephyr development.

.. _zephyr-repo:

Use Repo to Fetch Updates
-------------------------

The Zephyr microPlatform uses the Repo tool to manage its Git
repositories. In :ref:`zephyr-install`, you used this tool to clone
these Git repositories into a Zephyr microPlatform installation
directory on a development computer. See :ref:`repo-primer`
for more details on Repo.

After the installation, you'll continue to use Repo to fetch upstream
changes as follows.

#. Enter the ``.repo/manifests`` subdirectory of the Zephyr
   microPlatform (this is where the Repo manifest repository is
   installed on your system).

#. Use git to note the current Git commit SHA of the manifest
   repository. For example:

   .. code-block:: console

      git --no-pager log -n1 --pretty='%H'

   We'll call the current SHA ``STARTING_MANIFEST_SHA``.

#. Go back to the top level Zephyr microPlatform installation
   directory, and use Repo to sync updates:

   .. code-block:: console

      repo sync

   .. warning::

      If you make any changes to any repositories managed by Repo, this
      will attempt to rebase your local branches, which **can erase
      history and cause conflicts**.

      You can use ``repo sync -n`` to fetch changes only, without
      rebasing, and then use Git to inspect the differences between your
      local and the upstream branches, merge or rebase appropriately,
      etc.

      This is currently considered an advanced use case. If you are
      trying this during the beta period and you run into problems,
      please contact us.

#. After running ``repo sync``, you can use the ``zmp`` helper script
   documented above to re-build and re-test your application, and make
   adjustments.

   We recommend comparing your application with the updated version
   of the sample application you started from for relevant
   updates. This will let you adjust your application if needed to
   keep up with upstream.

If you run into problems, you can temporarily roll back to a previous
Zephyr microPlatform release as follows:

.. code-block:: console

   $ cd .repo/manifests
   $ git checkout STARTING_MANIFEST_SHA
   $ cd ../..
   $ repo sync

However, this defeats the purpose of receiving continuous updates from
Open Source Foundries.

Managing Out of Tree Patches
----------------------------

While an upstream first approach is recommended for development, situations
come up when out-of-tree patches are necessary for a microPlatform project
such as Zephyr. `Repo`_ has built-in tooling to handle this workflow. The
``repo start`` command informs Repo that development will take place in a
given branch name for a project. Once Repo is aware there are development
branches for a project, ``repo sync`` will take care of rebasing the patch(es).

.. code-block:: console

   # work starts at latest microPlatform release
   # A fix is required in Zephyr, the patch was submitted upstream, but is
   # is still awaiting review. In the meantime, a branch can be used with:
   $ repo start github-pr-XXX zephyr
   $ cd zephyr
   # apply the patch(es) to zephyr
   $ git commit -a -m "out-of-tree patch waiting for zephyr merge #12"
   ...
   # A new update comes in for the microPlatform
   $ repo sync
   ...
   # If no merge conflicts are detected, everything is done. Otherwise
   # you will have to drop into the zephyr directory and use Git to
   # resolve the merge conflict.


Port a Board
------------

.. warning::

   Porting a board necessarily means altering the Zephyr repository,
   which complicates the ``repo sync`` process used to receive
   updates.

   See the above section for more details.

Start with the `Zephyr porting guides`_, and the existing supported
boards. In addition to architecture and basic board support, you'll
need a flash driver and working networking for MCUBoot and FOTA
updates. Some useful starting points:

- ``include/flash.h`` and the ``drivers/flash`` directory in the
  Zephyr source tree for flash drivers.

- The `Zephyr networking documentation`_

Some particular areas to be aware of when porting Zephyr
microPlatform-based applications to a new board follow.

- `Device tree with flash partitions`_: your board will need a device
  tree defined, which includes flash partitions for MCUBoot itself
  (``boot_partition``), a partition your application runs in
  (``slot0_partition``), a partition to download firmware updates into
  (``slot1_partitition``; this must be the same size as
  ``slot0_partition``), and a scratch partition for MCUBoot to use
  when swapping images between slots 0 and 1 (``scratch_partition``;
  this can be as small as a single sector, but be aware of extra wear
  on your flash). Currently, ``slot0_partition``, ``slot1_partition``,
  and ``scratch_partition`` must be contiguous on flash. The
  ``boot_partition`` must be chosen so that the chip reset vector will
  be loaded from there.

  Each supported board has a device tree with a partition layout you
  can use while getting started.

- A device tree overlay file: your application needs a device tree
  ``.overlay`` file instructing the Zephyr build system to use the
  flash partitions defined in the device tree when linking.

  See the example overlay files in the ``boards`` subdirectory of each
  sample application, along with the build system files which use
  them, for reference.

  Selecting ``slot0_partition`` within your DTS overlay will ensure
  that your application is linked appropriately:

  .. code-block:: none

     / {
             chosen {
                     zephyr,code-partition = &slot0_partition;
             };
     };

  For additional information on this, see the documentation for
  `CONFIG_FLASH_LOAD_OFFSET`_ and `CONFIG_FLASH_LOAD_SIZE`_. Note that
  **these values are set automatically** by Zephyr's
  ``scripts/dts/extract_dts_includes.py`` script as a consequence of
  your DTS overlay file.

- `CONFIG_TEXT_SECTION_OFFSET`_: On ARM targets, this is the offset
  from ``CONFIG_FLASH_LOAD_OFFSET`` at which your application's vector
  table is stored. This is required so ``zmp build`` can place an
  MCUBoot header in the space between the flash load offset and the
  beginning of your image.

  If you're unsure, ``0x200`` is a generally safe default value.

  Lower values (such as 0x100) may be possible depending on your
  chip's vector table alignment requirements. Smaller values waste
  less flash space.

- To port MCUBoot to your board, you also need a Zephyr flash driver,
  ideally (though not necessarily) with `CONFIG_FLASH_PAGE_LAYOUT`_
  support.

  (MCUBoot's build system will automatically pick up the device tree
  partitions you define in Zephyr, and ``zmp`` will be automatically
  be able to build MCUBoot for your board once it's got Zephyr
  support.)

  For additional background information on porting MCUBoot to your
  board, see the `MCUBoot README-zephyr.rst`_ file.

.. _repo-primer:

Repo Primer
-----------

This section describes `Repo`_ and how the Zephyr microPlatform uses
it. If you're unfamiliar with Repo, it may make things clearer.

A Zephyr microPlatform installation contains multiple `Git`_
repositories, which are managed by a *manifest file* in a Repo
*manifest repository*.

The manifest repository's name is ``zmp-manifest``. It's a Git
repository, just like any of the source code repositories. When
:ref:`installing the Zephyr microPlatform <zephyr-install>`, `repo
init`_ is given the URL for the manifest repository (either a
subscriber or public version).

The manifest repository contains a manifest file, named
``default.xml``.  This file describes the other Git repositories in
the Zephyr microPlatform installation, and their metadata. During
installation, `repo sync`_ is run after ``repo init``. This clones the
other repositories according to the contents of the manifest.

Roughly speaking, the manifest file contains:

- *remotes*, which specify where Zephyr microPlatform repositories are
  hosted.
- *projects*, which specify the Git repositories that make up the
  microPlatform, along with the remotes to fetch them from, and Git
  branches to check out.

.. rubric:: Footnotes

.. _Makefile.export:
   http://docs.zephyrproject.org/application/application.html#support-for-building-third-party-library-code

.. [#makefileexport]

   It's possible to use ``zmp flash`` on directories not generated
   by ``zmp build``, but it assumes an output directory hierarchy
   matching what :ref:`zmp build <zephyr-build>` creates,
   including the presence of a `Makefile.export`_.

.. [#zephyrflash]

   If your board's Zephyr support does not include ``make flash``,
   ``zmp flash`` will not work either.

   ``zmp flash`` exists mainly because the Zephyr ``make flash`` target
   currently only allows flashing a single application binary to a
   board at a fixed address. This is not sufficient for the
   Zephyr microPlatform, which has a more complex flashing process due to the
   presence of a bootloader and an application, which must be flashed in
   different locations. This is being addressed in upstream Zephyr.

.. _Zephyr developer guides: http://docs.zephyrproject.org/application/index.html

.. _Zephyr porting guides: http://docs.zephyrproject.org/porting/porting.html

.. _Zephyr networking documentation: http://docs.zephyrproject.org/subsystems/networking/networking.html

.. _CONFIG_TEXT_SECTION_OFFSET: http://docs.zephyrproject.org/reference/kconfig/CONFIG_TEXT_SECTION_OFFSET.html#cmdoption-arg-config-text-section-offset

.. _Device tree with flash partitions: http://docs.zephyrproject.org/devices/dts/device_tree.html

.. _CONFIG_FLASH_LOAD_OFFSET: http://docs.zephyrproject.org/reference/kconfig/CONFIG_FLASH_LOAD_OFFSET.html#cmdoption-arg-config-flash-load-offset

.. _CONFIG_FLASH_LOAD_SIZE: http://docs.zephyrproject.org/reference/kconfig/CONFIG_FLASH_LOAD_SIZE.html#cmdoption-arg-config-flash-load-size

.. _CONFIG_FLASH_PAGE_LAYOUT: http://docs.zephyrproject.org/reference/kconfig/CONFIG_FLASH_PAGE_LAYOUT.html#cmdoption-arg-config-flash-page-layout

.. _MCUBoot README-zephyr.rst: https://github.com/runtimeco/mcuboot/blob/master/README-zephyr.rst

.. _Repo: https://gerrit.googlesource.com/git-repo/

.. _Git: https://git-scm.com/

.. _repo init:
   https://source.android.com/source/using-repo#init

.. _repo sync:
   https://source.android.com/source/using-repo#sync
