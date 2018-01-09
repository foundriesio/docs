.. _ref-zephyr-zmp:

Zephyr microPlatform zmp Tool
=============================

This page describes the ``zmp`` tool used for developing and flashing
embedded applications with the Zephyr microPlatform. It assumes that
the Zephyr microPlatform has successfully been installed using Repo as
described in :ref:`tutorial-zephyr`, but provides additional
information on using ``zmp`` with other boards and in additional
contexts.

After installing the Zephyr microPlatform repositories and build environment,
the Zephyr and mcuboot build systems and other tools can be used
directly. However, these interfaces can be hard to use when first developing
applications. For this reason, the Zephyr microPlatform provides a helper
script, named ``zmp``, which provides a higher-level interface.

The ``zmp`` utility is installed into the root of the Zephyr microPlatform
tree by ``repo sync``. It accepts multiple commands useful during
development; they are documented below. Run ``./zmp -h`` from the
Zephyr microPlatform installation directory for additional information.

.. _ref-zephyr-zmp-build:

Build an Application: ``zmp build``
-----------------------------------

.. warning::

   As described in :ref:`tutorial-zephyr-build`, mcuboot binaries and
   Zephyr microPlatform applications are built and signed with
   development keys which are not secret. While this makes development
   and testing more convenient, it is not suitable for production.

   However, it's not currently possible to generate mcuboot images
   that trust non-dev keys without editing the mcuboot source tree.

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

.. _ref-zephyr-zmp-configure:

Configure an Application: ``zmp configure``
-------------------------------------------

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
:ref:`zmp build <ref-zephyr-zmp-build>`.

For more information on Kconfig in Zephyr, see `Configuration Options
Reference Guide
<http://docs.zephyrproject.org/reference/kconfig/index.html>`_.

.. _ref-zephyr-zmp-flash:

Flash an Application to a Device: ``zmp flash``
-----------------------------------------------

After building an application and mcuboot binary with :ref:`zmp build
<ref-zephyr-zmp-build>`, the ``zmp flash`` command can be used to
flash it to a board, usually via USB.

The ``zmp flash`` command relies on Zephyr's build system to choose a
flashing utility, and run it with the correct arguments to flash
mcuboot and the application binary to an attached board.

If you experience errors using this command, make sure you can flash
your board using Zephyr's CMake build system's ``flash`` target as
described in its `Zephyr documentation
<http://docs.zephyrproject.org/boards/boards.html>`_\ [#zephyrflash]_.

To get help, run this from the Zephyr microPlatform root directory::

  ./zmp flash -h

Basic uses:

- To flash the artifacts for ``some-application`` to the default board::

    ./zmp flash some-application

- To flash to a different board, ``96b_carbon``::

    ./zmp flash -b 96b_carbon some-application

.. rubric:: Footnotes

.. [#zephyrflash]

   If your board's Zephyr support does not include a build system
   ``flash`` target, ``zmp flash`` will not work either, but adding
   ``flash`` support to your board's build system configuration
   doesn't necessarily enable ``zmp flash``.

   This is because ``zmp flash`` currently relies on some additional
   modifications to the Zephyr CMake build system's ``flash`` target,
   which allow overridding the target binary to flash a signed blob
   which MCUBoot can chain-load. These modifications are currently
   only supported for the dfu-util and pyOCD flasher backends. This is
   a temporary measure which is being addressed in the Zephyr upstream
   repository.
