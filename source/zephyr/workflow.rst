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
  Zephyr microPlatform tree, targeting the default board (96b_nitrogen)::

      ./zmp build some-application

  This generates artifacts under ``outdir`` like so::

      outdir
      └── some-application
          └── 96b_nitrogen
              ├── app
              └── mcuboot

  The application build for ``96b_nitrogen`` is in
  ``outdir/some-application/96b_nitrogen/app``. The mcuboot build is
  in ``mcuboot``, next to ``app``.

- To build the same application for another board,
  e.g. ``96b_carbon``, use the ``-b`` option::

      ./zmp build -b 96b_carbon some-application

  The ``-b`` option can be used in any ``zmp build`` command to
  target other boards.

  Running this after building for 96Boards Nitrogen as in the above
  example results in a parallel set of build artifacts, like so::

      outdir
      └── some-application
          ├── 96b_carbon
          │   ├── app
          │   └── mcuboot
          └── 96b_nitrogen
              ├── app
              └── mcuboot

- It's fine to build application sources in a subdirectory. For
  example, running::

    ./zmp build some-nested/application-name

  will generate::

    outdir
    └── some-nested
        └── application-name
            └── 96b_nitrogen
                ├── app
                └── mcuboot

  Note that the signed image in ``96b_nitrogen/app`` is named
  ``application-name-96b_nitrogen-signed.bin``; i.e., just the base
  name of the application directory is used.

- To build or incrementally compile the application image only, not
  updating the mcuboot image, use ``-o``::

      ./zmp build -o app some-application

- Similarly, to build or incrementally compile mcuboot only::

      ./zmp build -o mcuboot some-application

.. _zephyr-configure:

Configure an Application: ``zmp configure``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
<https://www.zephyrproject.org/doc/reference/kconfig/index.html>`_.

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
<https://www.zephyrproject.org/doc/boards/boards.html>`_\
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
~~~~~~~~~~~~~~~~~~~~~

.. todo::

   Provide a primer; upstream Zephyr has enough DT machinery to make
   this possible now.

Debug a Running Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: improve this once 'make debug' is re-worked upstream

Attach a debugger in the host environment to the device, and provide
the ELF binaries from the build tree to it for symbol tables.

Integrate an External Dependency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: user-friendly instructions, post-CMake transition.

.. _Application Development Primer:
   https://www.zephyrproject.org/doc/application/application.html

Integrating external dependencies with Zephyr is currently not
straightforward. One approach is to copy them into your application
repository, either directly or as submodules.

Additional information is available in the Zephyr `Application
Development Primer`_.

.. _zephyr-repo:

Use Repo to Manage Git Repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   After first installing the Zephyr microPlatform, use of Repo is optional.
   Since Repo is essentially a wrapper around Git, it's possible to use
   ``git`` commands directly in individual repositories as well.

The Zephyr microPlatform uses the Repo tool to manage its Git repositories. In
:ref:`zephyr-install`, you used this tool to clone these Git
repositories into an Zephyr microPlatform installation directory on a
developmentcomputer.

After the installation, you can continue to use Repo to manage local
branches and fetch upstream changes.  Importantly, you can use:

- ``repo start`` to create local Git branches in multiple repositories.
- ``repo status`` to get status output about each Zephyr microPlatform
  repository (this is similar to ``git status``, but operates on all
  repositories).
- ``repo diff`` to get a diff of unstaged changes in each Git repository
  (this is similar to ``git diff``, but operates on all repositories).
- ``repo sync`` to fetch remote changes from all Zephyr microPlatform
  repositories, and rebase local Git branches on top of them (alternatively,
  use ``repo sync -n`` to fetch changes only, without rebasing).

See the `Repo command reference
<https://source.android.com/source/using-repo>`_ for more details.
However, note that because the **Zephyr microPlatform does not use Gerrit** as
a Git repository server, repo commands which expect a Gerrit server are not
applicable to an Zephyr microPlatform installation. For example, instead of
using ``repo upload``, use ``git push``.

You can also run ``repo help <command>`` to get usage for each repo
command; for example, use ``repo help sync`` to get help on ``repo
sync``.

.. rubric:: Footnotes

.. _Makefile.export:
   https://www.zephyrproject.org/doc/application/application.html#support-for-building-third-party-library-code

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
