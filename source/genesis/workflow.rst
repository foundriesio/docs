.. _genesis-workflows:

Genesis Workflows
=================

This page describes the workflows for developing and deploying
embedded applications with Genesis. It assumes that Genesis has
successfully been installed as described in
:ref:`genesis-getting-started`.

.. _genesis-development-workflow:

Development Workflow
--------------------

The development workflow describes how to use Genesis to create,
develop, and maintain embedded applications.

The ``genesis`` utility, which is installed into the root of the
Genesis tree, is an important entry point. It accepts multiple
commands useful during development; key commands are described
below. Run ``./genesis -h`` from the Genesis installation directory
for additional information.

.. _genesis-build:

Building Applications: ``genesis build``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

   By default, mcuboot binaries and Genesis applications are built and
   signed with development keys which are not secret. While this makes
   development and testing more convenient, it is not suitable for
   production. See :ref:`genesis-production-workflow` for more
   information.

.. todo::

   It's not currently possible to generate mcuboot images that trust
   non-dev keys (https://trello.com/c/mSZPuXxG,
   https://projects.linaro.org/browse/LITE-147).

   As such, the ``--signing-key`` and ``--signing-key-type`` arguments
   to ``genesis build`` are misleading, as the mcuboot image won't
   trust the key used to sign the application. Don't use these for
   now.

The top-level command is ``genesis build``. To get help, run this from
the Genesis root directory::

    ./genesis build -h

Builds are always out of tree; that is, build artifacts are never
generated in the source code directories. By default, they are stored
under ``outdir`` in the Genesis top-level directory.

Examples:

- To build an application ``some-application`` (for example,
  ``zephyr-fota-hawkbit``) available in the Genesis tree, targeting
  the default board (96b_nitrogen)::

      ./genesis build some-application

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

      ./genesis build -b 96b_carbon some-application

  The ``-b`` option can be used in any ``genesis build`` command to
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

- To build or incrementally compile the application image only, not
  updating the mcuboot image, use ``-o``::

      ./genesis build -o app some-application

- Similarly, to build or incrementally compile mcuboot only::

      ./genesis build -o mcuboot some-application

- Other applications can be built the same way::

      ./genesis build some-other-application

.. _genesis-configure:

Configure an Application: ``genesis configure``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Zephyr RTOS uses a configuration system called Kconfig, which is
borrowed from the Linux kernel. The ``genesis configure`` command lets
you change the configuration database for an application build, using
any of the Kconfig front-ends supported on your platform.

The top-level command is ``genesis configure``.

To get help, run this from the Genesis root directory::

    ./genesis configure -h

Example uses:

- To configure the ``zephyr-fota-hawkbit`` application (not mcuboot)
  build for the default board, ``96b_nitrogen``::

      ./genesis configure -o app zephyr-fota-hawkbit

- To configure the mcuboot (not application) build for another board,
  ``96b_carbon``::

      ./genesis configure -o mcuboot -b 96b_nitrogen zephyr-fota-hawkbit

Note that ``genesis configure`` accepts many of the same options as
:ref:`genesis build <genesis-build>`. You can mix application
configuration and build using these commands in any order you want.

For more information on Kconfig in Zephyr, see `Configuration Options
Reference Guide
<https://www.zephyrproject.org/doc/reference/kconfig/index.html>`_.

Flash an Application to a Device
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: Replace with ``genesis flash`` once implemented:
          https://trello.com/c/SXgRHneO

Please refer to the :ref:`demonstration system <iot-devices>`
documentation.

Create an Application
~~~~~~~~~~~~~~~~~~~~~

.. todo:: fill this in when it's possible.

   https://trello.com/c/Yj5vW4zf
   https://projects.linaro.org/browse/LITE-91
   https://projects.linaro.org/browse/LITE-125

Debug a Running Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: improve this.

Attach a debugger in the host environment to the device, and provide
the ELF binaries to it for symbol tables. On boards which support
CMSIS-DAP, `pyOCD <https://github.com/mbedmicro/pyOCD>`_ is the
recommended solution.

Integrate an External Dependency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: user-friendly instructions, post-CMake transition.

Integrating external dependencies with Zephyr is currently not
straightforward. One approach is to copy them into your application
repository, either directly or as submodules.

.. _genesis-repo:

Use Repo to Manage Git Repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   After first installing Genesis, use of Repo is optional.  Since
   Repo is essentially a wrapper around Git, it's possible to use
   ``git`` commands directly in individual repositories as well.

Genesis uses the Repo tool to manage its Git repositories. In
:ref:`install-genesis`, you used this tool to clone these Git
repositories into a Genesis installation directory on a development
computer.

After the installation, you can continue to use Repo to manage local
branches and fetch upstream changes.  Importantly, you can use:

- ``repo start`` to create local Git branches in multiple repositories.
- ``repo status`` to get status output about each Genesis repository
  (this is similar to ``git status``, but operates on all repositories).
- ``repo diff`` to get a diff of unstaged changes in each Git repository
  (this is similar to ``git diff``, but operates on all repositories).
- ``repo sync`` to fetch remote changes from all Genesis repositories,
  and rebase local Git branches on top of them (alternatively, use
  ``repo sync -n`` to fetch changes only, without rebasing).

See the `Repo command reference
<https://source.android.com/source/using-repo>`_ for more details.
However, note that because **Genesis does not use Gerrit** as a Git
repository server, repo commands which expect a Gerrit server are not
applicable to a Genesis installation. For example, instead of using
``repo upload``, use ``git push``.

You can also run ``repo help <command>`` to get usage for each repo
command; for example, use ``repo help sync`` to get help on ``repo
sync``.

.. _genesis-production-workflow:

Production Workflow
-------------------

.. todo:: Write this section.

   - Minimum sane key management policies
   - Building production-ready mcuboot and application images
     (blocker: https://trello.com/c/mSZPuXxG)
   - Disabling JTAG/SWD or making physical access harder and other
     issues discussed in the threat model.
