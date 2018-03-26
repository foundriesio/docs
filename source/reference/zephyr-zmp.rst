.. _ref-zephyr-zmp:

Zephyr microPlatform zmp Tool
=============================

This page describes a helper script, ``zmp``, provided by the Zephyr
microPlatform. ``zmp`` provides a higher-level interface to the Zephyr
and MCUboot build systems, which is optional, but can be easier to use.

The ``zmp`` utility is installed into the root of the Zephyr microPlatform
tree by ``repo sync``. It accepts multiple commands useful during
development; they are documented below. Run ``./zmp -h`` from the
Zephyr microPlatform installation directory for additional information.

(See :ref:`tutorial-zephyr` for details on installing the Zephyr
microPlatform.)

.. _ref-zephyr-zmp-build:

Build an Application: ``zmp build``
-----------------------------------

.. warning::

   Using the ``--signing-key`` and ``--signing-key-type`` arguments to
   ``zmp build`` must be done with care; see :ref:`howto-mcuboot-keys`
   for details.

The ``zmp build`` command builds signed Zephyr microPlatform
application images, as well as MCUboot binaries capable of loading
those images. It is a wrapper for the CMake toolchains provided by
Zephyr and MCUboot which makes interoperation easier.

To get help, run this from the Zephyr microPlatform root directory::

    ./zmp build -h

The ``zmp build`` command always builds out of tree; that is,
build artifacts are never generated in the source code directories. By
default, they are stored under ``outdir`` in the Zephyr microPlatform top-level
directory.

Examples:

- To build the Zephyr "Hello World" application, sign it for loading
  by MCUboot, and MCUboot itself, with all binaries targeting the BLE
  Nano 2::

      ./zmp build -b nrf52_blenano2 zephyr/samples/hello_world

  This generates artifacts under ``outdir`` like so::

    outdir/
    └── zephyr
        └── samples
            └── hello_world
                └── nrf52_blenano2
                    ├── app
                    └── mcuboot

  The application build for ``nrf52_blenano2`` is in
  ``outdir/zephyr/samples/hello_world/nrf52_blenano2/app``. The
  MCUboot build is in ``mcuboot``, next to ``app``.

- To build the same application for another board,
  e.g. ``frdm_k64f``, use the ``-b`` option::

      ./zmp build -b frdm_k64f zephyr/samples/hello_world

  The ``-b`` option can be used in any ``zmp build`` command to
  target other boards.

  Running this after building for BLE Nano 2 as in the above
  example results in a parallel set of build artifacts, like so::

    outdir/
    └── zephyr
        └── samples
            └── hello_world
                ├── frdm_k64f
                │   ├── app
                │   └── mcuboot
                └── nrf52_blenano2
                    ├── app
                    └── mcuboot

- To build or incrementally compile the application image only, not
  updating the MCUboot image, use ``-o``::

      ./zmp build -b nrf52_blenano2 -o app zephyr/samples/hello_world

- Similarly, to build or incrementally compile MCUboot only::

      ./zmp build -b nrf52_blenano2 -o mcuboot zephyr/samples/hello_world

.. _ref-zephyr-zmp-configure:

Configure an Application: ``zmp configure``
-------------------------------------------

The Zephyr RTOS uses a configuration system called Kconfig, which is
borrowed from the Linux kernel. The ``zmp configure`` command lets
you change the configuration database for an application build, using
any of the Kconfig front-ends supported on your platform.

.. important::

   This command can only be run after using ``zmp build`` to
   create the build directory, which contains the configuration
   database.

To get help, run this from the Zephyr microPlatform root directory::

    ./zmp configure -h

Example uses:

- To change the application configuration (not the MCUboot
  configuration) for ``zephyr/samples/hello_world`` for the
  ``nrf52_blenano2`` board::

      ./zmp configure -o app -b nrf52_blenano2 zephyr/samples/hello_world

- To change the MCUboot (not application) configuration for another
  board, ``frdm_k64f``::

      ./zmp configure -o mcuboot -b frdm_k64f zephyr/samples/hello_world

If you don't specify ``-o``, then ``zmp configure`` will sequentially
run the application and MCUboot configuration interfaces, in that
order.

Note that ``zmp configure`` accepts many of the same options as
:ref:`zmp build <ref-zephyr-zmp-build>`.

For more information on Kconfig in Zephyr, see `Configuration Options
Reference Guide
<http://docs.zephyrproject.org/reference/kconfig/index.html>`_.

.. _ref-zephyr-zmp-flash:

Flash an Application to a Device: ``zmp flash``
-----------------------------------------------

After building an application and MCUboot binary with :ref:`zmp build
<ref-zephyr-zmp-build>`, the ``zmp flash`` command can be used to
flash it to a board, usually via USB.

The ``zmp flash`` command relies on Zephyr's build system to choose a
flashing utility, and run it with the correct arguments to flash
MCUboot and the application binary to an attached board.

If you experience errors using this command, make sure you can flash
your board using Zephyr's CMake build system's ``flash`` target as
described in its `Zephyr documentation
<http://docs.zephyrproject.org/boards/boards.html>`_\ [#zephyrflash]_.

To get help, run this from the Zephyr microPlatform root directory::

  ./zmp flash -h

Basic uses:

- To flash the artifacts for ``zephyr/samples/hello_world`` to
  ``nrf52_blenano2`` board::

    ./zmp flash -b nrf52_blenano2 zephyr/samples/hello_world

- To re-flash just the "Hello world" application, not re-flashing
  MCUboot::

    ./zmp flash -o app -b nrf52_blenano2 zephyr/samples/hello_world

- To flash to a different board, ``frdm_k64f``::

    ./zmp flash -b frdm_k64f zephyr/samples/hello_world

.. _ref-zephyr-zmp-clean:

Clean Up A Build: ``zmp clean``, ``zmp pristine``
-------------------------------------------------

The ``clean`` and ``pristine`` commands can be used to delete build
artifacts. These ``zmp`` commands run the Zephyr build system targets
with the same names. The main differences between the two are:

- ``clean`` deletes object files and other build artifacts, but not
  the build system generated by CMake.
- ``pristine`` deletes all generated files, including the build system
  itself.

Example uses:

- To delete the application and MCUboot object files and other outputs
  after building ``zephyr/samples/hello_world`` for the
  ``nrf52_blenano2`` board::

    ./zmp clean -b nrf52_blenano2 zephyr/samples/hello_world

- To just delete the application's files for the same board::

    ./zmp clean -b nrf52_blenano2 -o app zephyr/samples/hello_world

- To just delete the MCUboot files for the same board::

    ./zmp clean -b nrf52_blenano2 -o mcuboot zephyr/samples/hello_world

- To completely remove all artifacts generated for the same
  application for the same board::

    ./zmp pristine -b nrf52_blenano2 zephyr/samples/hello_world

- To completely remove just the application artifacts for the same board::

    ./zmp pristine -b nrf52_blenano2 -o app zephyr/samples/hello_world

- To completely remove just the MCUboot artifacts for the same board::

    ./zmp pristine -b nrf52_blenano2 -o mcuboot zephyr/samples/hello_world

.. rubric:: Footnotes

.. [#zephyrflash]

   If your board's Zephyr support does not include a build system
   ``flash`` target, ``zmp flash`` will not work either, but adding
   ``flash`` support to your board's build system configuration
   doesn't necessarily enable ``zmp flash``.

   This is because ``zmp flash`` currently relies on some additional
   modifications to the Zephyr CMake build system's ``flash`` target,
   which allow overridding the target binary to flash a signed blob
   which MCUboot can chain-load. These modifications are currently
   only supported for the dfu-util and pyOCD flasher backends. This is
   a temporary measure which is being addressed in the Zephyr upstream
   repository.
